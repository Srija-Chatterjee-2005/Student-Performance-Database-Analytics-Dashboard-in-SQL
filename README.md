# **🎓 EduPulse — Student Performance Database & Analytics Dashboard**
---

A SQL-powered academic analytics system for monitoring student performance, attendance, course outcomes, SPI scores, and early-risk indicators through an interactive Streamlit dashboard.


<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/a57a0f37-d1b0-4902-b392-90ed8af36fc4" />


---

## **📌A. Project Overview**
---

EduPulse is a portfolio-ready Student Performance Database & Analytics Dashboard designed to transform academic records into clear, actionable insights. The project combines SQL, Python, SQLite, Pandas, Plotly, and Streamlit to analyze student marks, attendance, course performance, grades, pass rates, and academic risk.
The application launches with a realistic sample dataset and also supports CSV upload, allowing users to analyze their own compatible student dataset without modifying the source code. Dashboard KPIs and visualizations are recalculated automatically from the active data.


<img width="1919" height="897" alt="Screenshot 2026-08-14 012331" src="https://github.com/user-attachments/assets/8147a8fe-d916-4aaa-aab9-3c1fb108bb9f" />


---

## **🎯B. Project Objectives**
---

Centralize student academic and attendance information in a structured database.

Track student, course, and department-level performance.

Calculate academic KPIs such as average score, attendance, pass rate, grade, and Student Performance Index (SPI).

Identify low-performing and at-risk students using rule-based early-warning analytics.

Provide an interactive dashboard for easier academic monitoring and decision-making.

Demonstrate practical SQL analytics through an integrated SQL Lab.


<img width="1919" height="910" alt="Screenshot 2026-08-14 012342" src="https://github.com/user-attachments/assets/dd8f408c-3a01-4dd4-a43e-dbfcfb26bdf8" />


---

## **🛠️C. Tools & Technologies Used**
---

**SQL / SQLite** : Database storage, querying, aggregation, filtering, ranking, and analytics

**Python** : Application logic and data processing

**Pandas** : Data cleaning, transformation, aggregation, and CSV processing

**Streamlit** : Interactive web application and dashboard UI

**Plotly** : Interactive charts and data visualizations

**CSV** : Sample dataset and real-time user data upload

**Git & GitHub** : Version control, documentation, and project hosting


<img width="1919" height="918" alt="Screenshot 2026-08-14 012356" src="https://github.com/user-attachments/assets/9daa598c-1ce5-4bc3-8f3d-9c4db1d3cfba" />


---

## **✨D. Key Features**
---

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


<img width="1919" height="903" alt="Screenshot 2026-08-14 012407" src="https://github.com/user-attachments/assets/0a4bff69-cf95-4b95-b104-7dc57887e6f5" />


---

## **📈E. Analytics Logic**
---

### **Weighted Average Score**

Assessment ---------- Weight

Assignment ---------- 15%

Quiz ---------------- 10%

Midterm ------------- 30%

Final Exam --------- 45%

### **Student Performance Index (SPI)**

Academic Score: 70%

Attendance: 20%

Feedback: 10%

### **Early-Risk Classification**

🔴 Critical: Attendance below 60% and average score below 40.

🟠 High Risk: Attendance below 70% or average score below 50.

🟡 Medium Risk: Attendance below 80% or average score below 60.

🟢 Low Risk: Student does not meet the above risk conditions.


<img width="1919" height="909" alt="Screenshot 2026-08-14 012433" src="https://github.com/user-attachments/assets/d2d1a67f-a024-4532-8aa4-529c63ef706f" />


---

## **📁F. Project Structure**
---



<img width="594" height="782" alt="image" src="https://github.com/user-attachments/assets/774d19a4-812b-4625-9599-d61581af6a76" />



---

## **🧪G. SQL Analytics Included**
---

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


<img width="1912" height="924" alt="Screenshot 2026-08-14 012444" src="https://github.com/user-attachments/assets/e4b832f6-7385-4da4-b048-5ae1bd5ecd50" />


---

## **🖼️H. Output**
---

<img width="1919" height="922" alt="Screenshot 2026-08-14 012637" src="https://github.com/user-attachments/assets/8ca64e57-ae90-42e4-9066-37b80d3c91d8" />






<img width="1919" height="936" alt="Screenshot 2026-08-14 012622" src="https://github.com/user-attachments/assets/baf28870-0153-4fd5-8edb-e117ea16d86d" />






<img width="1919" height="937" alt="Screenshot 2026-08-14 012559" src="https://github.com/user-attachments/assets/5845a3f8-e3dc-44c6-a84f-845de83bb453" />






<img width="1915" height="911" alt="Screenshot 2026-08-14 012517" src="https://github.com/user-attachments/assets/70eba695-c3da-40e9-96e6-02949f497498" />






<img width="1917" height="902" alt="Screenshot 2026-08-14 012506" src="https://github.com/user-attachments/assets/d71cca59-7a67-418d-b625-f101bd04965d" />






---

## **🎥I. How to Run**
---




https://github.com/user-attachments/assets/5edd744c-16ad-4db6-8e02-4da3869e8db4




---

## **⬆️J. GitHub Upload Steps**
---

Open Command Prompt or Terminal inside the project folder and run:

git init

git branch -M main

git add .

git commit -m "Add Student Performance Database and Analytics Dashboard"

git remote add origin YOUR_GITHUB_REPOSITORY_URL

git pull origin main --rebase

git push -u origin main

---

## **💡K. Project Outcome**
---

EduPulse demonstrates how raw academic records can be converted into a structured database and then into meaningful analytical insights. The system helps identify performance trends, compare courses and departments, monitor attendance, rank students, and highlight learners who may require early academic intervention.
From a portfolio perspective, the project demonstrates SQL querying, database concepts, data analysis, KPI design, Python-based analytics, interactive visualization, and dashboard development in one end-to-end application.

---

## **👩‍💻L.  Author**
---

### **Srija Chatterjee**

LinkedIn: https://www.linkedin.com/in/srija-chatterjee-82a539308?utm_source=share_via&utm_content=profile&utm_medium=member_android

GitHub: https://github.com/Srija-Chatterjee-2005

---
