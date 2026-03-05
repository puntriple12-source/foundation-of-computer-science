# Data Systems & Security – Assignment Repository

> **Module:** Data Systems and Security
> **Course:** Foundation of Computer Science | ST4015CMD

## Overview

This repository contains all practical files, scripts, diagrams, and SQL code supporting the written report submitted for the Data Systems and Security module.

---

## Repository Structure

```
├── sql/
│   ├── schema.sql          # Normalized 3NF schema (Student, Club, Membership tables)
│   └── queries.sql         # Seed data + Task 4 & 5 SQL queries (INSERT, SELECT, JOIN)
│
├── scripts/
│   ├── encoding_demo.py    # Task 1: Base64, URL, Hex encoding demonstrations
│   └── seating_solver.py   # Task 2: Brute-force and heuristic seating arrangement solver
│
├── diagrams/
│   ├── er_diagram.svg      # Task 3: Entity-Relationship diagram (Student–Membership–Club)
│   └── encoding_flow.svg   # Task 1: Data flow of Base64 in TLS/SMTP email transmission
│
└── README.md               # This file
```

---

## Task 1 – Encoding Formats & Secure Protocols

**Files**
- `scripts/encoding_demo.py`
- `diagrams/encoding_flow.svg`

**How to Run**
```bash
python3 scripts/encoding_demo.py
```

**What It Does**

Demonstrates the four encoding schemes from the report (Sections 1.1–1.8):

1. **ASCII / UTF-8** — character encoding basics and limitations with non-English characters.
2. **Base64** — HTTP Basic Auth headers, MIME email attachments, and OAuth JWT tokens (Base64URL).
3. **URL (percent) encoding** — REST API query parameters, OAuth redirect URIs, and XSS prevention.
4. **Hexadecimal** — SHA-256 hash output, HMAC-SHA256 API request signing, and hex dumps for binary analysis.
5. **Simulated TLS email flow** — full step-by-step walkthrough of the Figure 5 diagram:
   `Sender → Base64 Encode → TLS Encrypt → SMTP Server → TLS Decrypt → Base64 Decode → Recipient`

**Diagram**
`diagrams/encoding_flow.svg` — visual reproduction of **Figure 5** from the report (Section 1.8): *The Workflow of Encoding and Encryption in Email Transmission*.

---

## Task 2 – Classroom Seating Arrangement (P vs NP)

**Files**
- `scripts/seating_solver.py`

**How to Run**
```bash
python3 scripts/seating_solver.py
```

**What It Does**

Models the seating arrangement problem with 5 students (Alice, Bob, Carol, Dave, Eve):

**Constraints:**
- Friend constraints (cannot sit adjacent): Alice–Bob, Carol–Dave, Bob–Eve
- Same-city constraints (cannot sit adjacent): Alice–Carol, Dave–Eve

Demonstrates all three sections of the report:

| Section | Report Reference | What It Shows |
|---------|-----------------|---------------|
| 2.1 | Figure 6 | O(n) constraint checker — verification is easy (P) |
| 2.2 | Figures 7, 8, 9 | Brute-force: all 5! = 120 permutations, factorial growth table |
| 2.3 | Figures 10, 11, 12 | Heuristic: most-constrained-first, 90%+ fewer steps vs brute-force |

**Sample Output**
```
[Brute Force]  Valid solutions found : 10
               Total permutations    : 120

[Heuristic]    Arrangement : Carol | Bob | Dave | Alice | Eve
               Steps taken : 11  (vs 120 for brute-force)
               Reduction   : 90.8% fewer steps
```

---

## Task 3 – College Club Membership Database (Normalization & SQL)

**Files**
- `sql/schema.sql`
- `sql/queries.sql`
- `diagrams/er_diagram.svg`

**How to Run (MySQL / MariaDB)**
```bash
# Create a database first, then run both files in order:
mysql -u root -p your_database < sql/schema.sql
mysql -u root -p your_database < sql/queries.sql
```

**Or run in SQLite**
```bash
sqlite3 club.db < sql/schema.sql
sqlite3 club.db < sql/queries.sql
```

> Note: SQLite does not enforce foreign key constraints by default. Run `PRAGMA foreign_keys = ON;` first if needed.

**Schema Summary (3NF)**

| Table | Primary Key | Foreign Keys | Purpose |
|-------|-------------|--------------|---------|
| Student | StudentID | — | Stores student name & email |
| Club | ClubID | — | Stores club name, room, mentor |
| Membership | MembershipID | StudentID, ClubID | Links students to clubs with join date |

All three tables are confirmed in **Third Normal Form (3NF)**:
- Student attributes depend only on `StudentID`
- Club attributes depend only on `ClubID`
- Membership attributes (including `JoinDate`) depend only on `MembershipID`
- No redundancy, partial dependencies, or transitive dependencies remain

**ER Diagram**
`diagrams/er_diagram.svg` shows:
- `Student` entity: `StudentID` (PK), `StudentName`, `Email`
- `Club` entity: `ClubID` (PK), `ClubName`, `ClubRoom`, `ClubMentor`
- `Membership` junction table: `MembershipID` (PK), `StudentID` (FK), `ClubID` (FK), `JoinDate`
- **1:N** — one student → many membership records
- **N:1** — many membership records → one club
- **M:N** — Student and Club share a many-to-many relationship resolved via Membership

**Key SQL Queries**

```sql
-- Task 5: All students with their clubs and join dates
SELECT s.StudentName, c.ClubName, m.JoinDate
FROM Membership m
INNER JOIN Student s ON m.StudentID = s.StudentID
INNER JOIN Club    c ON m.ClubID    = c.ClubID
ORDER BY m.JoinDate;
```

---

## Requirements

- **Python 3.8+** — no external libraries; uses `base64`, `urllib.parse`, `hashlib`, `hmac`, `itertools`, `math`, `time` (all stdlib)
- **MySQL 8.0+** or **MariaDB 10.3+** or **SQLite 3** for SQL files
- Any SVG viewer or web browser for diagrams

---

## References

See full reference list in the submitted report (APA 7th edition).
