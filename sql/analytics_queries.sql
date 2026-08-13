-- 1. Top 10 students by SPI
SELECT student_id, student_name, ROUND(AVG(spi),2) AS avg_spi
FROM student_performance
GROUP BY student_id, student_name
ORDER BY avg_spi DESC
LIMIT 10;

-- 2. At-risk students
SELECT student_id, student_name,
       ROUND(AVG(attendance_pct),2) AS attendance,
       ROUND(AVG(average_score),2) AS avg_score,
       MAX(risk_status) AS risk_status
FROM student_performance
WHERE risk_status IN ('High Risk','Critical')
GROUP BY student_id, student_name
ORDER BY avg_score ASC;

-- 3. Course-wise performance
SELECT course_code, course_name,
       ROUND(AVG(average_score),2) AS avg_score,
       ROUND(AVG(attendance_pct),2) AS avg_attendance,
       ROUND(100.0 * AVG(CASE WHEN grade <> 'F' THEN 1 ELSE 0 END),2) AS pass_rate
FROM student_performance
GROUP BY course_code, course_name
ORDER BY avg_score DESC;

-- 4. Department comparison
SELECT department,
       ROUND(AVG(average_score),2) AS avg_score,
       ROUND(AVG(attendance_pct),2) AS attendance,
       ROUND(AVG(spi),2) AS avg_spi
FROM student_performance
GROUP BY department
ORDER BY avg_spi DESC;

-- 5. Low attendance students
SELECT student_id, student_name, department,
       ROUND(AVG(attendance_pct),2) AS avg_attendance
FROM student_performance
GROUP BY student_id, student_name, department
HAVING AVG(attendance_pct) < 75
ORDER BY avg_attendance;

-- 6. Student ranking using window function
WITH student_perf AS (
  SELECT student_id, student_name, ROUND(AVG(spi),2) AS avg_spi
  FROM student_performance
  GROUP BY student_id, student_name
)
SELECT *,
       DENSE_RANK() OVER (ORDER BY avg_spi DESC) AS student_rank
FROM student_perf
ORDER BY student_rank;