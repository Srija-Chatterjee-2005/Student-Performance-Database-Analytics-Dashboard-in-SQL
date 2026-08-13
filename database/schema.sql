DROP TABLE IF EXISTS student_performance;

CREATE TABLE student_performance (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    student_name TEXT NOT NULL,
    department TEXT NOT NULL,
    department_code TEXT,
    semester INTEGER,
    course_code TEXT NOT NULL,
    course_name TEXT NOT NULL,
    attendance_pct REAL,
    assignment_marks REAL,
    quiz_marks REAL,
    midterm_marks REAL,
    final_exam_marks REAL,
    average_score REAL,
    grade TEXT,
    performance_category TEXT,
    risk_status TEXT,
    course_completion_status TEXT,
    feedback_rating INTEGER,
    spi REAL
);

CREATE INDEX IF NOT EXISTS idx_student_id ON student_performance(student_id);
CREATE INDEX IF NOT EXISTS idx_department ON student_performance(department);
CREATE INDEX IF NOT EXISTS idx_course_code ON student_performance(course_code);
CREATE INDEX IF NOT EXISTS idx_risk_status ON student_performance(risk_status);