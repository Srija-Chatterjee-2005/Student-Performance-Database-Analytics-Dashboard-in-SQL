
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from pathlib import Path
import io

st.set_page_config(
    page_title="EduPulse — Student Performance Intelligence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "student_performance_sample.csv"
DB = ROOT / "database" / "student_performance.db"
SCHEMA = ROOT / "database" / "schema.sql"

REQUIRED = [
    "student_id","student_name","department","department_code","semester",
    "course_code","course_name","attendance_pct","assignment_marks","quiz_marks",
    "midterm_marks","final_exam_marks","average_score","grade",
    "performance_category","risk_status","course_completion_status",
    "feedback_rating","spi"
]

st.markdown("""
<style>
:root {
  --ink:#172033; --muted:#5d6b82; --line:#dfe6ef; --white:#ffffff;
  --blue:#526ee8; --mint:#42b883; --pink:#e9688f; --gold:#e7a73f;
}
html, body, [class*="css"] { font-family: Inter, "Segoe UI", Arial, sans-serif; }
.stApp {
  background:
    radial-gradient(circle at 8% 5%, rgba(107,137,255,.15), transparent 24rem),
    radial-gradient(circle at 92% 12%, rgba(255,183,205,.20), transparent 25rem),
    linear-gradient(180deg,#f9fbff 0%,#fffdfb 50%,#f8fff9 100%);
  color:var(--ink);
}
.block-container {max-width:1450px; padding:1.4rem 2rem 3rem;}
[data-testid="stSidebar"] {
  background:#ffffff !important; border-right:1px solid var(--line);
  box-shadow:4px 0 22px rgba(30,46,78,.05);
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] label,
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span {color:#26344c !important;}
.hero {
  padding:1.55rem 1.75rem; border-radius:24px;
  background:linear-gradient(120deg,#ffffff 0%,#f3f6ff 48%,#fff3f7 100%);
  border:1px solid #dfe6f3; box-shadow:0 12px 32px rgba(34,53,90,.08);
  margin-bottom:1.2rem;
}
.hero h1 {margin:0;color:#17233b;font-size:2.15rem;font-weight:850;letter-spacing:-.03em;}
.hero p {margin:.55rem 0 0;color:#526078;font-size:1.02rem;font-weight:500;}
.metric-card {
  background:#fff;border:1px solid #dfe6ef;border-radius:18px;padding:1rem 1.05rem;
  box-shadow:0 7px 22px rgba(35,53,86,.07);min-height:124px;
  border-top:5px solid #7086ee;
}
.metric-card:nth-child(2n){border-top-color:#52bd91;}
.metric-label {color:#53637a;font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.055em;}
.metric-value {color:#17233b;font-size:1.8rem;font-weight:850;margin-top:.28rem;}
.metric-sub {color:#68778d;font-size:.78rem;margin-top:.18rem;font-weight:500;}
.section-title {font-size:1.22rem;font-weight:850;color:#1c2b45;margin:1rem 0 .8rem;}
div[data-testid="stPlotlyChart"] {
  background:#fff;border:1px solid #dfe6ef;border-radius:18px;padding:.45rem;
  box-shadow:0 7px 22px rgba(35,53,86,.055);
}
div[data-testid="stDataFrame"] {border:1px solid #dfe6ef;border-radius:16px;overflow:hidden;background:white;}
.stButton>button,.stDownloadButton>button {
  border-radius:12px!important;border:1px solid #ccd7e7!important;
  background:#fff!important;color:#26344c!important;font-weight:750!important;
}
.stButton>button:hover,.stDownloadButton>button:hover {
  border-color:#526ee8!important;color:#4059c9!important;background:#f5f7ff!important;
}
div[data-baseweb="select"] > div, .stTextInput input, .stTextArea textarea {
  background:#fff!important;color:#172033!important;border-color:#ccd7e7!important;
}
[data-testid="stFileUploader"] section {background:#f7f9ff!important;border:1px dashed #8ea0dd!important;}
[data-testid="stFileUploader"] section * {color:#26344c!important;}
.stAlert {border-radius:14px;}
hr {border-color:#e4e9f1;}
</style>
""", unsafe_allow_html=True)

PALETTE = ["#526EE8","#42B883","#E9688F","#E7A73F","#4A9BD8","#9A72CF","#70B79B"]

def polish(fig, height=390):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="#ffffff",
        font=dict(color="#25344d", size=13),
        title_font=dict(color="#17233b", size=17),
        legend=dict(font=dict(color="#34445f")),
        margin=dict(t=62,l=35,r=25,b=45),
        hoverlabel=dict(bgcolor="white", font_color="#172033")
    )
    fig.update_xaxes(showgrid=True, gridcolor="#edf1f6", tickfont=dict(color="#4d5d75"), title_font=dict(color="#34445f"))
    fig.update_yaxes(showgrid=True, gridcolor="#edf1f6", tickfont=dict(color="#4d5d75"), title_font=dict(color="#34445f"))
    return fig

def load_sample():
    return pd.read_csv(SAMPLE)

def enrich(df):
    out = df.copy()
    # Allow slightly simpler uploaded files; derive calculated fields where possible.
    numeric = ["attendance_pct","assignment_marks","quiz_marks","midterm_marks","final_exam_marks","feedback_rating"]
    for c in numeric:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    if "average_score" not in out.columns and all(c in out.columns for c in ["assignment_marks","quiz_marks","midterm_marks","final_exam_marks"]):
        out["average_score"] = (
            .15*out["assignment_marks"] + .10*out["quiz_marks"] +
            .30*out["midterm_marks"] + .45*out["final_exam_marks"]
        ).round(2)

    if "grade" not in out.columns and "average_score" in out.columns:
        bins = [-1,49.999,59.999,69.999,79.999,89.999,101]
        labels = ["F","D","C","B","A","A+"]
        out["grade"] = pd.cut(out["average_score"], bins=bins, labels=labels)

    if "performance_category" not in out.columns and "average_score" in out.columns:
        out["performance_category"] = pd.cut(
            out["average_score"], [-1,39.999,54.999,69.999,84.999,101],
            labels=["Critical","Needs Improvement","Average","Good","Excellent"]
        )

    if "risk_status" not in out.columns and all(c in out.columns for c in ["attendance_pct","average_score"]):
        def risk(r):
            if r["attendance_pct"] < 60 and r["average_score"] < 40: return "Critical"
            if r["attendance_pct"] < 70 or r["average_score"] < 50: return "High Risk"
            if r["attendance_pct"] < 80 or r["average_score"] < 60: return "Medium Risk"
            return "Low Risk"
        out["risk_status"] = out.apply(risk, axis=1)

    if "spi" not in out.columns and all(c in out.columns for c in ["average_score","attendance_pct"]):
        fb = pd.to_numeric(out.get("feedback_rating", 4), errors="coerce").fillna(4)
        out["spi"] = (.70*out["average_score"] + .20*out["attendance_pct"] + .10*(fb*20)).round(2)

    if "course_completion_status" not in out.columns and "average_score" in out.columns:
        out["course_completion_status"] = np.where(out["average_score"] >= 40, "Completed", "Incomplete")

    # Fill friendly defaults for optional identity columns
    if "department_code" not in out.columns:
        out["department_code"] = out.get("department", "GEN").astype(str).str[:4].str.upper()
    if "semester" not in out.columns:
        out["semester"] = 1

    return out

def validate(df):
    must_have = ["student_id","student_name","department","course_code","course_name","attendance_pct",
                 "assignment_marks","quiz_marks","midterm_marks","final_exam_marks"]
    missing = [c for c in must_have if c not in df.columns]
    return missing

def sync_sqlite(df):
    DB.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB)
    df.to_sql("student_performance", con, if_exists="replace", index=False)
    try:
        con.execute("CREATE INDEX IF NOT EXISTS idx_student_id ON student_performance(student_id)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_department ON student_performance(department)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_course_code ON student_performance(course_code)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_risk_status ON student_performance(risk_status)")
        con.commit()
    except Exception:
        pass
    con.close()

def metric_card(label, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
      <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("## 🎓 EduPulse")
st.sidebar.caption("Student Performance Intelligence & Analytics")
uploaded = st.sidebar.file_uploader("Upload student CSV", type=["csv"], help="Upload a CSV with the template columns. The dashboard refreshes immediately.")
st.sidebar.download_button(
    "Download CSV template",
    data=(ROOT/"data"/"upload_template.csv").read_bytes(),
    file_name="student_performance_upload_template.csv",
    mime="text/csv"
)

if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded)
        missing = validate(raw)
        if missing:
            st.sidebar.error("Missing required columns: " + ", ".join(missing))
            df = load_sample()
            source = "Example dataset"
        else:
            df = enrich(raw)
            source = f"Uploaded: {uploaded.name}"
            st.sidebar.success("CSV loaded successfully")
    except Exception as e:
        st.sidebar.error(f"Could not read CSV: {e}")
        df = load_sample()
        source = "Example dataset"
else:
    df = load_sample()
    source = "Example dataset"

df = enrich(df)
sync_sqlite(df)

page = st.sidebar.radio(
    "Navigate",
    ["Executive Overview","Student Explorer","Course Analytics","Early Warning Center","SQL Lab","Data & Upload Guide"]
)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Data source:** {source}")
st.sidebar.caption(f"{len(df):,} course-level records • {df['student_id'].nunique():,} students")

st.markdown("""
<div class="hero">
  <h1>EduPulse <span style='font-weight:600;color:#526ee8'>• Student Performance Intelligence</span></h1>
  <p>Academic performance, attendance, course outcomes and early-warning analytics in one light, interactive dashboard.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:0 0 14px 0">
  <div style="background:#eef2ff;border:1px solid #d9e1ff;border-radius:14px;padding:11px;text-align:center;color:#314a9c;font-weight:750">📊 Live KPIs</div>
  <div style="background:#ecfbf4;border:1px solid #d2f0e2;border-radius:14px;padding:11px;text-align:center;color:#28795b;font-weight:750">📁 CSV Upload</div>
  <div style="background:#fff0f4;border:1px solid #f6d7e1;border-radius:14px;padding:11px;text-align:center;color:#9a4962;font-weight:750">⚠️ Risk Engine</div>
  <div style="background:#fff8e9;border:1px solid #f2e0b9;border-radius:14px;padding:11px;text-align:center;color:#8b6528;font-weight:750">🎯 SPI Score</div>
  <div style="background:#f2efff;border:1px solid #dfd8fb;border-radius:14px;padding:11px;text-align:center;color:#654ea0;font-weight:750">🧪 SQL Lab</div>
</div>
""", unsafe_allow_html=True)

# Global filters
with st.expander("Filters", expanded=False):
    c1,c2,c3 = st.columns(3)
    dept_sel = c1.multiselect("Department", sorted(df["department"].dropna().astype(str).unique()))
    course_sel = c2.multiselect("Course", sorted(df["course_name"].dropna().astype(str).unique()))
    sem_vals = sorted(pd.to_numeric(df["semester"], errors="coerce").dropna().astype(int).unique())
    sem_sel = c3.multiselect("Semester", sem_vals)

f = df.copy()
if dept_sel: f = f[f["department"].isin(dept_sel)]
if course_sel: f = f[f["course_name"].isin(course_sel)]
if sem_sel: f = f[f["semester"].isin(sem_sel)]

def no_data():
    if f.empty:
        st.warning("No records match the selected filters.")
        st.stop()

if page == "Executive Overview":
    no_data()
    students = f["student_id"].nunique()
    courses_n = f["course_code"].nunique()
    avg_score = f["average_score"].mean()
    attendance = f["attendance_pct"].mean()
    pass_rate = (f["grade"].astype(str) != "F").mean()*100
    at_risk = f[f["risk_status"].isin(["High Risk","Critical"])]["student_id"].nunique()

    cols = st.columns(6)
    vals = [
        ("Students", f"{students:,}", "Unique learners"),
        ("Courses", f"{courses_n:,}", "Active in current view"),
        ("Avg Score", f"{avg_score:.1f}", "Weighted academic score"),
        ("Attendance", f"{attendance:.1f}%", "Average attendance"),
        ("Pass Rate", f"{pass_rate:.1f}%", "Records above fail threshold"),
        ("At Risk", f"{at_risk:,}", "High-risk or critical students"),
    ]
    for col, item in zip(cols, vals):
        with col: metric_card(*item)

    st.markdown('<div class="section-title">Performance snapshot</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    dept = f.groupby("department", as_index=False).agg(avg_score=("average_score","mean"), avg_spi=("spi","mean"))
    fig = px.bar(dept, x="department", y="avg_score", text_auto=".1f", color="department",
                 color_discrete_sequence=PALETTE, title="Department-wise Average Score")
    fig.update_layout(showlegend=False, paper_bgcolor="white", plot_bgcolor="white", margin=dict(t=55,l=20,r=20,b=20))
    c1.plotly_chart(polish(fig), width="stretch")

    grade = f["grade"].astype(str).value_counts().rename_axis("grade").reset_index(name="count")
    fig = px.pie(grade, names="grade", values="count", hole=.58, color_discrete_sequence=PALETTE, title="Grade Distribution")
    fig.update_layout(paper_bgcolor="white", margin=dict(t=55,l=20,r=20,b=20))
    c2.plotly_chart(polish(fig), width="stretch")

    c3,c4 = st.columns(2)
    course = f.groupby(["course_code","course_name"],as_index=False)["average_score"].mean().sort_values("average_score", ascending=False)
    fig = px.bar(course.head(10), x="average_score", y="course_code", orientation="h", text_auto=".1f",
                 color="average_score", color_continuous_scale=["#edf7f2","#6ec6a6","#527a6b"], title="Top Courses by Average Score")
    fig.update_layout(coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"), paper_bgcolor="white", plot_bgcolor="white", margin=dict(t=55,l=20,r=20,b=20))
    c3.plotly_chart(polish(fig), width="stretch")

    fig = px.scatter(f, x="attendance_pct", y="average_score", color="risk_status", hover_data=["student_name","course_code"],
                     color_discrete_map={"Low Risk":"#6EC6A6","Medium Risk":"#F4BD61","High Risk":"#EF8FA9","Critical":"#B95C6D"},
                     title="Attendance vs Academic Performance")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", margin=dict(t=55,l=20,r=20,b=20))
    c4.plotly_chart(polish(fig), width="stretch")

elif page == "Student Explorer":
    no_data()
    students = f[["student_id","student_name"]].drop_duplicates().sort_values("student_name")
    choice = st.selectbox("Select a student", students["student_name"].tolist())
    sf = f[f["student_name"] == choice].copy()

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: metric_card("Average Score", f"{sf['average_score'].mean():.1f}")
    with c2: metric_card("Attendance", f"{sf['attendance_pct'].mean():.1f}%")
    with c3: metric_card("SPI", f"{sf['spi'].mean():.1f}/100")
    with c4: metric_card("Courses", f"{sf['course_code'].nunique()}")
    risk = sf["risk_status"].mode().iloc[0] if not sf["risk_status"].mode().empty else "—"
    with c5: metric_card("Risk Status", risk)

    c1,c2 = st.columns([1.3,1])
    fig = px.bar(sf, x="course_code", y="average_score", color="performance_category",
                 color_discrete_sequence=PALETTE, text_auto=".1f", title="Course Performance")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    c1.plotly_chart(polish(fig), width="stretch")

    long = sf.melt(id_vars=["course_code"], value_vars=["assignment_marks","quiz_marks","midterm_marks","final_exam_marks"],
                   var_name="Assessment", value_name="Marks")
    fig = px.line(long, x="Assessment", y="Marks", color="course_code", markers=True, title="Assessment Profile")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    c2.plotly_chart(polish(fig), width="stretch")

    st.dataframe(sf[["course_code","course_name","attendance_pct","average_score","grade","performance_category","risk_status","spi"]],
                 width="stretch", hide_index=True)

elif page == "Course Analytics":
    no_data()
    course_stats = f.groupby(["course_code","course_name"], as_index=False).agg(
        avg_score=("average_score","mean"),
        avg_attendance=("attendance_pct","mean"),
        avg_spi=("spi","mean"),
        students=("student_id","nunique"),
        feedback=("feedback_rating","mean")
    )
    course_stats["pass_rate"] = f.groupby(["course_code","course_name"])["grade"].apply(lambda s:(s.astype(str)!="F").mean()*100).values

    c1,c2 = st.columns(2)
    fig = px.bar(course_stats.sort_values("avg_score",ascending=False), x="course_code", y="avg_score",
                 color="avg_score", text_auto=".1f", color_continuous_scale=["#fff3df","#f4bd61","#bd8730"], title="Average Score by Course")
    fig.update_layout(coloraxis_showscale=False, paper_bgcolor="white", plot_bgcolor="white")
    c1.plotly_chart(polish(fig), width="stretch")
    fig = px.scatter(course_stats, x="avg_attendance", y="avg_score", size="students", color="pass_rate",
                     hover_name="course_name", color_continuous_scale=["#fce8ee","#ef8fa9","#8a4f63"], title="Course Performance Matrix")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    c2.plotly_chart(polish(fig), width="stretch")

    st.dataframe(course_stats.round(2), width="stretch", hide_index=True)

elif page == "Early Warning Center":
    no_data()
    student_risk = f.groupby(["student_id","student_name","department"], as_index=False).agg(
        attendance=("attendance_pct","mean"),
        avg_score=("average_score","mean"),
        spi=("spi","mean")
    )
    def calc_risk(r):
        if r["attendance"] < 60 and r["avg_score"] < 40: return "Critical"
        if r["attendance"] < 70 or r["avg_score"] < 50: return "High Risk"
        if r["attendance"] < 80 or r["avg_score"] < 60: return "Medium Risk"
        return "Low Risk"
    student_risk["risk_status"] = student_risk.apply(calc_risk, axis=1)
    def reason(r):
        reasons=[]
        if r["attendance"] < 75: reasons.append("Low attendance")
        if r["avg_score"] < 50: reasons.append("Low academic score")
        if r["spi"] < 60: reasons.append("Weak overall performance index")
        return " + ".join(reasons) if reasons else "Stable academic indicators"
    student_risk["risk_reason"] = student_risk.apply(reason, axis=1)

    counts = student_risk["risk_status"].value_counts()
    cols=st.columns(4)
    for col,label in zip(cols,["Critical","High Risk","Medium Risk","Low Risk"]):
        with col: metric_card(label, f"{int(counts.get(label,0))}", "students")

    c1,c2 = st.columns([1,1.4])
    rc = student_risk["risk_status"].value_counts().rename_axis("risk_status").reset_index(name="count")
    fig = px.pie(rc, names="risk_status", values="count", hole=.58,
                   color="risk_status", color_discrete_map={"Low Risk":"#6EC6A6","Medium Risk":"#F4BD61","High Risk":"#EF8FA9","Critical":"#B95C6D"},
                   title="Risk Distribution")
    fig.update_layout(paper_bgcolor="white")
    c1.plotly_chart(polish(fig), width="stretch")

    fig = px.scatter(student_risk, x="attendance", y="avg_score", color="risk_status", hover_name="student_name",
                     size="spi", color_discrete_map={"Low Risk":"#6EC6A6","Medium Risk":"#F4BD61","High Risk":"#EF8FA9","Critical":"#B95C6D"},
                     title="Early-Warning Map")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    c2.plotly_chart(polish(fig), width="stretch")

    alert = student_risk[student_risk["risk_status"].isin(["Critical","High Risk"])].sort_values(["risk_status","avg_score"])
    st.markdown('<div class="section-title">Priority intervention list</div>', unsafe_allow_html=True)
    st.dataframe(alert.round(2), width="stretch", hide_index=True)

elif page == "SQL Lab":
    st.markdown('<div class="section-title">SQL Analytics Lab</div>', unsafe_allow_html=True)
    st.caption("Choose a ready-made analytics query or write your own. The SQLite database is refreshed whenever the sample or uploaded CSV changes.")

    EXAMPLE_QUERIES = {
        "Department Performance": """SELECT department,
       ROUND(AVG(average_score),2) AS avg_score,
       ROUND(AVG(attendance_pct),2) AS avg_attendance,
       ROUND(AVG(spi),2) AS avg_spi,
       COUNT(DISTINCT student_id) AS students
FROM student_performance
GROUP BY department
ORDER BY avg_score DESC;""",

        "Top 10 Students": """SELECT student_id, student_name,
       ROUND(AVG(average_score),2) AS avg_score,
       ROUND(AVG(attendance_pct),2) AS attendance,
       ROUND(AVG(spi),2) AS avg_spi
FROM student_performance
GROUP BY student_id, student_name
ORDER BY avg_spi DESC
LIMIT 10;""",

        "At-Risk Students": """SELECT student_id, student_name, department,
       ROUND(AVG(attendance_pct),2) AS attendance,
       ROUND(AVG(average_score),2) AS avg_score,
       ROUND(AVG(spi),2) AS avg_spi
FROM student_performance
GROUP BY student_id, student_name, department
HAVING AVG(attendance_pct) < 70 OR AVG(average_score) < 50
ORDER BY avg_score ASC;""",

        "Course Performance": """SELECT course_code, course_name,
       ROUND(AVG(average_score),2) AS avg_score,
       ROUND(AVG(attendance_pct),2) AS avg_attendance,
       ROUND(AVG(spi),2) AS avg_spi,
       COUNT(DISTINCT student_id) AS students
FROM student_performance
GROUP BY course_code, course_name
ORDER BY avg_score DESC;""",

        "Low Attendance Students": """SELECT student_id, student_name, department,
       ROUND(AVG(attendance_pct),2) AS avg_attendance
FROM student_performance
GROUP BY student_id, student_name, department
HAVING AVG(attendance_pct) < 75
ORDER BY avg_attendance ASC;""",

        "Pass Rate by Course": """SELECT course_code, course_name,
       COUNT(*) AS records,
       ROUND(100.0 * AVG(CASE WHEN grade <> 'F' THEN 1 ELSE 0 END),2) AS pass_rate
FROM student_performance
GROUP BY course_code, course_name
ORDER BY pass_rate DESC;""",

        "Student Ranking": """WITH student_perf AS (
    SELECT student_id, student_name,
           ROUND(AVG(spi),2) AS avg_spi
    FROM student_performance
    GROUP BY student_id, student_name
)
SELECT student_id, student_name, avg_spi,
       DENSE_RANK() OVER (ORDER BY avg_spi DESC) AS student_rank
FROM student_perf
ORDER BY student_rank, student_name;""",

        "Attendance vs Performance": """SELECT
    CASE
        WHEN attendance_pct >= 90 THEN '90-100%'
        WHEN attendance_pct >= 80 THEN '80-89%'
        WHEN attendance_pct >= 70 THEN '70-79%'
        WHEN attendance_pct >= 60 THEN '60-69%'
        ELSE 'Below 60%'
    END AS attendance_band,
    ROUND(AVG(average_score),2) AS avg_score,
    COUNT(*) AS records
FROM student_performance
GROUP BY attendance_band
ORDER BY avg_score DESC;""",

        "Custom Query": ""
    }

    if "sql_selected_example" not in st.session_state:
        st.session_state.sql_selected_example = "Department Performance"
    if "sql_editor" not in st.session_state:
        st.session_state.sql_editor = EXAMPLE_QUERIES["Department Performance"]

    def load_example():
        selected = st.session_state.sql_example_picker
        st.session_state.sql_selected_example = selected
        if selected != "Custom Query":
            st.session_state.sql_editor = EXAMPLE_QUERIES[selected]
        else:
            st.session_state.sql_editor = ""

    picker_col, info_col = st.columns([1.1, 1.9])
    with picker_col:
        st.selectbox(
            "Choose example query",
            list(EXAMPLE_QUERIES.keys()),
            key="sql_example_picker",
            index=list(EXAMPLE_QUERIES.keys()).index(st.session_state.sql_selected_example),
            on_change=load_example
        )
    with info_col:
        st.info("Select an example and its SQL is loaded automatically into the editor. Choose **Custom Query** to write your own SELECT/WITH query.")

    q = st.text_area("SQL editor", key="sql_editor", height=245)

    b1, b2 = st.columns([1, 4])
    run = b1.button("▶ Run Query", type="primary", width="stretch")
    b2.caption("Read-only mode protects the project database from accidental changes.")

    if run:
        cleaned = q.strip()
        if not cleaned:
            st.warning("The SQL editor is empty.")
        elif not cleaned.lower().startswith(("select","with","pragma")):
            st.error("For safety, SQL Lab allows only SELECT, WITH, or PRAGMA queries.")
        else:
            try:
                con = sqlite3.connect(DB)
                out = pd.read_sql_query(cleaned, con)
                con.close()
                st.success(f"Query executed successfully • {len(out):,} rows returned")
                st.dataframe(out, width="stretch", hide_index=True)
                st.download_button(
                    "⬇ Download query result CSV",
                    out.to_csv(index=False),
                    "edupulse_sql_query_result.csv",
                    "text/csv"
                )
            except Exception as e:
                st.error(f"SQL error: {e}")

    st.markdown("---")
    st.markdown("**What this lab demonstrates:** `SELECT` • `GROUP BY` • `HAVING` • `CASE` • aggregates • CTEs • window functions • ranking")

elif page == "Data & Upload Guide":
    st.markdown('<div class="section-title">How the live CSV mode works</div>', unsafe_allow_html=True)
    st.write("The project launches with the bundled example dataset. Uploading a CSV from the sidebar replaces the example data immediately for the current session and rebuilds the analytics from the uploaded records.")
    st.markdown("**Minimum required upload columns**")
    st.code(", ".join(["student_id","student_name","department","course_code","course_name","attendance_pct","assignment_marks","quiz_marks","midterm_marks","final_exam_marks"]))
    st.write("If your CSV omits calculated fields such as `average_score`, `grade`, `performance_category`, `risk_status`, `course_completion_status` or `spi`, the app derives them automatically.")
    st.markdown("**Current dataset preview**")
    st.dataframe(df.head(30), width="stretch", hide_index=True)
    st.download_button("Download current dataset", df.to_csv(index=False), "current_student_performance_data.csv","text/csv")
