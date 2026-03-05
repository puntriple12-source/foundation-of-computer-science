-- ============================================================
-- queries.sql
-- Task 3: College Club Membership Management
-- Foundation of Computer Science | ST4015CMD
-- Data Systems and Security Assignment
-- Seed Data + Task 4 & Task 5 SQL Queries
-- ============================================================


-- ============================================================
-- STEP 2: INSERT ORIGINAL SEED DATA
-- ============================================================

-- Insert Students (7 original students)
INSERT INTO Student (StudentID, StudentName, Email) VALUES
(1, 'Asha',   'asha@email.com'),
(2, 'Bikash', 'bikash@email.com'),
(3, 'Nisha',  'nisha@email.com'),
(4, 'Rohan',  'rohan@email.com'),
(5, 'Suman',  'suman@email.com'),
(6, 'Pooja',  'pooja@email.com'),
(7, 'Aman',   'aman@email.com');

-- Insert Clubs (4 original clubs)
INSERT INTO Club (ClubID, ClubName, ClubRoom, ClubMentor) VALUES
('C01', 'Music Club',  'R101', 'Mr. Raman'),
('C02', 'Sports Club', 'R202', 'Ms. Sita'),
('C03', 'Drama Club',  'R303', 'Mr. Kiran'),
('C04', 'Coding Club', 'Lab1', 'Mr. Anil');

-- Insert Memberships (10 original enrollments)
INSERT INTO Membership (MembershipID, StudentID, ClubID, JoinDate) VALUES
('M01', 1, 'C01', '2024-01-10'),  -- Asha   → Music Club
('M02', 2, 'C02', '2024-01-12'),  -- Bikash → Sports Club
('M03', 1, 'C02', '2024-01-15'),  -- Asha   → Sports Club
('M04', 3, 'C01', '2024-01-20'),  -- Nisha  → Music Club
('M05', 4, 'C03', '2024-01-18'),  -- Rohan  → Drama Club
('M06', 5, 'C01', '2024-01-22'),  -- Suman  → Music Club
('M07', 2, 'C03', '2024-01-25'),  -- Bikash → Drama Club
('M08', 6, 'C02', '2024-01-27'),  -- Pooja  → Sports Club
('M09', 3, 'C04', '2024-01-28'),  -- Nisha  → Coding Club
('M10', 7, 'C04', '2024-01-30');  -- Aman   → Coding Club


-- ============================================================
-- TASK 4.1: INSERT A NEW STUDENT
-- Adds Priya as StudentID 8.
-- Because the schema is normalized, no club data is required here.
-- This directly resolves the Insert Anomaly of the original flat table.
-- ============================================================
INSERT INTO Student (StudentID, StudentName, Email)
VALUES (8, 'Priya', 'priya@email.com');


-- ============================================================
-- TASK 4.2: INSERT A NEW CLUB
-- Adds Art Club as ClubID C05.
-- The club can be added independently — no student enrollment required.
-- This again demonstrates how normalization eliminates Insert Anomalies.
-- ============================================================
INSERT INTO Club (ClubID, ClubName, ClubRoom, ClubMentor)
VALUES ('C05', 'Art Club', 'R404', 'Ms. Priya');


-- ============================================================
-- TASK 4.3: DISPLAY ALL STUDENTS
-- Retrieves every column and row from the Student table.
-- ============================================================
SELECT * FROM Student;


-- ============================================================
-- TASK 4.4: DISPLAY ALL CLUBS
-- Retrieves every column and row from the Club table.
-- ============================================================
SELECT * FROM Club;


-- ============================================================
-- TASK 5: SQL JOIN OPERATION
-- Combines Student, Membership, and Club tables to show
-- which student joined which club and on what date.
--
-- Two INNER JOINs are used:
--   1st JOIN: Membership → Student  (on StudentID)
--   2nd JOIN: Membership → Club     (on ClubID)
--
-- Expected output (ordered by JoinDate):
--   Asha       | Music Club   | 2024-01-10
--   Bikash     | Sports Club  | 2024-01-12
--   Asha       | Sports Club  | 2024-01-15
--   Rohan      | Drama Club   | 2024-01-18
--   Nisha      | Music Club   | 2024-01-20
--   Suman      | Music Club   | 2024-01-22
--   Bikash     | Drama Club   | 2024-01-25
--   Pooja      | Sports Club  | 2024-01-27
--   Nisha      | Coding Club  | 2024-01-28
--   Aman       | Coding Club  | 2024-01-30
-- ============================================================
SELECT
    s.StudentName,
    c.ClubName,
    m.JoinDate
FROM       Membership m
INNER JOIN Student    s ON m.StudentID = s.StudentID
INNER JOIN Club       c ON m.ClubID    = c.ClubID
ORDER BY   m.JoinDate;


-- ============================================================
-- BONUS QUERIES
-- ============================================================

-- How many members does each club have?
SELECT
    c.ClubName,
    COUNT(m.MembershipID) AS TotalMembers
FROM Club c
LEFT JOIN Membership m ON c.ClubID = m.ClubID
GROUP BY c.ClubID, c.ClubName
ORDER BY TotalMembers DESC;

-- Which clubs has a specific student joined? (e.g. Asha)
SELECT
    s.StudentName,
    c.ClubName,
    m.JoinDate
FROM Membership m
INNER JOIN Student s ON m.StudentID = s.StudentID
INNER JOIN Club    c ON m.ClubID    = c.ClubID
WHERE s.StudentName = 'Asha';

-- Which students joined after a specific date?
SELECT
    s.StudentName,
    c.ClubName,
    m.JoinDate
FROM Membership m
INNER JOIN Student s ON m.StudentID = s.StudentID
INNER JOIN Club    c ON m.ClubID    = c.ClubID
WHERE m.JoinDate > '2024-01-20'
ORDER BY m.JoinDate;

-- Students who are members of more than one club
SELECT
    s.StudentName,
    COUNT(m.MembershipID) AS ClubCount
FROM Student s
INNER JOIN Membership m ON s.StudentID = m.StudentID
GROUP BY s.StudentID, s.StudentName
HAVING COUNT(m.MembershipID) > 1
ORDER BY ClubCount DESC;
