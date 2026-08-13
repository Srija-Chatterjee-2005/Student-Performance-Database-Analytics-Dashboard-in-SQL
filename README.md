# EduPulse — Student Performance Intelligence & Analytics

A complete portfolio-ready academic analytics project with a **light premium Streamlit UI**, bundled sample data, CSV upload mode, live KPI recalculation, SQLite database sync, SQL query lab, student risk analytics, and course performance views.

## What the project does

The application starts with a realistic sample dataset so the dashboard works immediately. A user can then upload a CSV from the sidebar and the application automatically switches to the uploaded dataset for the current session. Calculated metrics such as average score, grade, performance category, risk status, course completion, and Student Performance Index (SPI) can be derived automatically.

## Main features

- Executive academic overview
- Student-level performance explorer
- Course and department analytics
- Early-warning / at-risk student center
- Student Performance Index (SPI)
- Attendance vs marks analytics
- Grade distribution and pass-rate analytics
- CSV upload with instant dashboard refresh
- Downloadable CSV template
- Download current live dataset
- Read-only SQL Lab connected to the active dataset
- SQLite database refreshed from the current dataset
- Light, non-dark UI with pastel cards and charts
- GitHub-ready project structure

## Run on Windows

1. Extract the ZIP.
2. Open the project folder.
3. Double-click `run_windows.bat`.
4. If Windows asks for permission, allow Python/network access.
5. Streamlit will open the project in your browser.

Alternative:
```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Run on macOS/Linux

```bash
chmod +x run_mac_linux.sh
./run_mac_linux.sh
```

## CSV upload format

Minimum required columns:

`student_id, student_name, department, course_code, course_name, attendance_pct, assignment_marks, quiz_marks, midterm_marks, final_exam_marks`

The application can derive:
- average_score
- grade
- performance_category
- risk_status
- course_completion_status
- SPI

See `data/upload_template.csv`.

## Project structure

```text
student_performance_analytics_project/
├── app/
│   └── app.py
├── data/
│   ├── student_performance_sample.csv
│   └── upload_template.csv
├── database/
│   └── schema.sql
├── sql/
│   └── analytics_queries.sql
├── assets/
├── docs/
├── screenshots/
├── requirements.txt
├── run_windows.bat
├── run_mac_linux.sh
└── README.md
```

## Analytics logic

**Average Score**
- Assignment: 15%
- Quiz: 10%
- Midterm: 30%
- Final exam: 45%

**Student Performance Index (SPI)**
- Academic score: 70%
- Attendance: 20%
- Feedback score: 10%

**Risk classification**
- Critical: attendance < 60 and average score < 40
- High Risk: attendance < 70 or average score < 50
- Medium Risk: attendance < 80 or average score < 60
- Low Risk: otherwise

## Portfolio talking point

> This project centralizes student assessment and attendance data, generates academic KPIs, identifies at-risk students using rule-based early-warning logic, and presents actionable insights through a live interactive dashboard. It also supports user-uploaded CSV data so the analytics can be regenerated for new academic datasets without modifying the source code.

## Recommended GitHub repository name

`student-performance-intelligence-dashboard`

## Suggested repository description

`SQL + Streamlit academic analytics system for student performance, attendance, course outcomes, SPI scoring and early-risk detection with live CSV upload.`


## V3 update
- EduPulse product branding
- Functional SQL example-query selector
- Example SQL automatically loads into the editor
- Custom Query mode
- Read-only SQL execution and CSV result download
