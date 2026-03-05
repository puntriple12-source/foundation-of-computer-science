-- ============================================================
-- schema.sql
-- Task 3: College Club Membership Management
-- Foundation of Computer Science | ST4015CMD
-- Data Systems and Security Assignment
-- Normalized 3NF Schema
-- ============================================================

-- Drop tables in reverse dependency order (safe re-run)
DROP TABLE IF EXISTS Membership;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Club;

-- ──────────────────────────────────────────────────────────────
-- Student Table
-- Stores one record per student.
-- StudentID uniquely identifies each student (Primary Key).
-- ──────────────────────────────────────────────────────────────
CREATE TABLE Student (
    StudentID   INT          PRIMARY KEY,
    StudentName VARCHAR(100) NOT NULL,
    Email       VARCHAR(150) UNIQUE NOT NULL
);

-- ──────────────────────────────────────────────────────────────
-- Club Table
-- Stores one record per club.
-- ClubID uniquely identifies each club (Primary Key).
-- ──────────────────────────────────────────────────────────────
CREATE TABLE Club (
    ClubID     VARCHAR(10)  PRIMARY KEY,
    ClubName   VARCHAR(100) NOT NULL,
    ClubRoom   VARCHAR(50),
    ClubMentor VARCHAR(100)
);

-- ──────────────────────────────────────────────────────────────
-- Membership Table  (Junction / Associative Table)
-- Resolves the Many-to-Many relationship between Student and Club.
-- Each row records one student joining one club on a specific date.
-- MembershipID is the surrogate Primary Key.
-- StudentID and ClubID are Foreign Keys enforcing referential integrity.
-- ──────────────────────────────────────────────────────────────
CREATE TABLE Membership (
    MembershipID VARCHAR(10)  PRIMARY KEY,
    StudentID    INT          NOT NULL,
    ClubID       VARCHAR(10)  NOT NULL,
    JoinDate     DATE         NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
    FOREIGN KEY (ClubID)    REFERENCES Club(ClubID)
);
