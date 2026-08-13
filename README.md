🎓 EduPulse — Student Performance Database & Analytics Dashboard

A SQL-powered academic analytics system for monitoring student performance, attendance, course outcomes, SPI scores, and early-risk indicators through an interactive Streamlit dashboard.

📌 Project Overview

EduPulse is a portfolio-ready Student Performance Database & Analytics Dashboard designed to transform academic records into clear, actionable insights. The project combines SQL, Python, SQLite, Pandas, Plotly, and Streamlit to analyze student marks, attendance, course performance, grades, pass rates, and academic risk.

The application launches with a realistic sample dataset and also supports CSV upload, allowing users to analyze their own compatible student dataset without modifying the source code. Dashboard KPIs and visualizations are recalculated automatically from the active data.

🎯 Project Objectives

Centralize student academic and attendance information in a structured database.

Track student, course, and department-level performance.

Calculate academic KPIs such as average score, attendance, pass rate, grade, and Student Performance Index (SPI).

Identify low-performing and at-risk students using rule-based early-warning analytics.

Provide an interactive dashboard for easier academic monitoring and decision-making.

Demonstrate practical SQL analytics through an integrated SQL Lab.

🛠️ Tools & Technologies Used

Technology

Purpose

SQL / SQLite

Database storage, querying, aggregation, filtering, ranking, and analytics

Python

Application logic and data processing

Pandas

Data cleaning, transformation, aggregation, and CSV processing

Streamlit

Interactive web application and dashboard UI

Plotly

Interactive charts and data visualizations

CSV

Sample dataset and real-time user data upload

Git & GitHub

Version control, documentation, and project hosting

✨ Key Features

📊 Executive Overview — students, courses, average score, attendance, pass rate, and at-risk KPIs.

👩‍🎓 Student Explorer — individual student performance, attendance, SPI, grades, course results, and assessment profile.

📚 Course Analytics — course averages, attendance, pass rates, SPI, student counts, and performance comparisons.

⚠️ Early Warning Center — identifies Critical, High Risk, Medium Risk, and Low Risk students with intervention indicators.

🎯 Student Performance Index (SPI) — combines academic performance, attendance, and feedback into a single analytical score.

🧪 SQL Analytics Lab — ready-to-run example queries plus a custom read-only SQL editor.

📁 Real-Time CSV Upload — upload a compatible dataset and refresh dashboard analytics automatically.

🔄 Automatic Calculations — derives average score, grade, performance category, risk status, completion status, and SPI when applicable.

🔍 Interactive Filters — filter analytics by department, course, and semester.

⬇️ Download Options — download active datasets and SQL query results as CSV files.

🎨 Light Responsive UI — clean pastel dashboard design with readable KPI cards, charts, tables, and navigation.

📈 Analytics Logic

Weighted Average Score

Assessment

Weight

Assignment

15%

Quiz

10%

Midterm

30%

Final Exam

45%

Student Performance Index (SPI)

Academic Score: 70%

Attendance: 20%

Feedback: 10%

Early-Risk Classification

🔴 Critical: Attendance below 60% and average score below 40.

🟠 High Risk: Attendance below 70% or average score below 50.

🟡 Medium Risk: Attendance below 80% or average score below 60.

🟢 Low Risk: Student does not meet the above risk conditions.

📁 Project Structure

Student-Performance-Database-Analytics-Dashboard-in-SQL/
├── .streamlit/
│   └── config.toml
├── app/
│   └── app.py
├── data/
│   ├── student_performance_sample.csv
│   └── upload_template.csv
├── database/
│   └── schema.sql
├── docs/
│   └── data_dictionary.csv
├── images/
├── sql/
│   └── analytics_queries.sql
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── run_windows.bat
└── run_mac_linux.sh

📤 How to Upload Your Own CSV

Launch the EduPulse dashboard.

Open the CSV Upload option in the sidebar.

Download data/upload_template.csv if you need the expected structure.

Prepare your student dataset using the required column names.

Upload the CSV file.

EduPulse validates the data and switches from the example dataset to the uploaded dataset.

Dashboard KPIs, charts, risk analysis, and student/course analytics update automatically.

Minimum Required Columns

student_id, student_name, department, course_code, course_name,
attendance_pct, assignment_marks, quiz_marks, midterm_marks,
final_exam_marks

🧪 SQL Analytics Included

The SQL portion demonstrates practical concepts including:

SELECT, WHERE, ORDER BY

GROUP BY and HAVING

Aggregate functions: AVG, COUNT, SUM, MIN, MAX

CASE statements

Common Table Expressions (CTEs)

Window functions such as DENSE_RANK()

Student ranking

Department and course performance analysis

Pass-rate analysis

Low-attendance and at-risk student identification

The SQL Lab also lets users select prepared analytics queries or write custom read-only queries and download the results.

🖼️ Screenshots / Output

Add dashboard screenshots to the images/ folder and display them here after uploading them to GitHub.

Suggested screenshots:

📊 Executive Overview

👩‍🎓 Student Explorer

📚 Course Analytics

⚠️ Early Warning Center

🧪 SQL Analytics Lab

📁 CSV Upload & Live Data View

![Executive Overview](images/executive_overview.png)
![Student Explorer](images/student_explorer.png)
![Course Analytics](images/course_analytics.png)
![Early Warning Center](images/early_warning_center.png)
![SQL Lab](images/sql_lab.png)

💡 Project Outcome

EduPulse demonstrates how raw academic records can be converted into a structured database and then into meaningful analytical insights. The system helps identify performance trends, compare courses and departments, monitor attendance, rank students, and highlight learners who may require early academic intervention.

From a portfolio perspective, the project demonstrates SQL querying, database concepts, data analysis, KPI design, Python-based analytics, interactive visualization, and dashboard development in one end-to-end application.

🚀 How to Run the Project

Windows

Download or clone the repository.

Open the project folder.

Double-click run_windows.bat.

Wait for the required packages to install.

EduPulse will open automatically in your browser.

Alternative command:

pip install -r requirements.txt
streamlit run app/app.py

macOS / Linux

chmod +x run_mac_linux.sh
./run_mac_linux.sh

🎥 Project Run & Demo Video

A screen recording showing how to launch and use the complete project will be added here.

🎥 Video:
[Paste screen-recording/video link here]

⬆️ GitHub Upload Steps

Open Command Prompt or Terminal inside the project folder and run:

git init
git branch -M main
git add .
git commit -m "Add Student Performance Database and Analytics Dashboard"
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git pull origin main --rebase
git push -u origin main

Replace YOUR_GITHUB_REPOSITORY_URL with your repository URL.

For future updates:

git add .
git commit -m "Update project"
git push

👩‍💻 Author

Srija Chatterjee

LinkedIn:

GitHub: https://github.com/Srija-Chatterjee-2005
