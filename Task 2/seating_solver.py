"""
seating_solver.py
Task 2: Classroom Seating Arrangement Problem (P vs NP)
Foundation of Computer Science | ST4015CMD
Data Systems and Security Assignment

Demonstrates all three aspects covered in the report (Sections 2.1–2.3):

  Section 2.1 – P vs NP Understanding
    • O(n) constraint checker  →  Figure 6 (Linear Time Complexity)

  Section 2.2 – Brute-Force Approach
    • All n! permutations generated and validated  → Figures 8, 9
    • Factorial growth table  → Figure 7

  Section 2.3 – Heuristic (Smart) Approach
    • Greedy most-constrained-first with deferred insertion → Figures 11, 12
    • Comparison of steps vs brute-force  → Figure 10

Students   : Alice, Bob, Carol, Dave, Eve
Constraints:
  Friend (cannot be adjacent):
    Alice–Bob,  Carol–Dave,  Bob–Eve
  Same-city (cannot be adjacent):
    Alice–Carol,  Dave–Eve

No external libraries required — uses Python standard library only.
Compatible with Python 3.8+.
"""

from itertools import permutations
import math
import time

DIVIDER  = "=" * 65
DIVIDER2 = "-" * 65


# ─────────────────────────────────────────────────────────────────────────────
# PROBLEM DEFINITION
# ─────────────────────────────────────────────────────────────────────────────

STUDENTS = ["Alice", "Bob", "Carol", "Dave", "Eve"]

# Friends who CANNOT sit adjacent  (report Section 2.1)
FRIEND_CONSTRAINTS: set[tuple[str, str]] = {
    ("Alice", "Bob"),
    ("Carol", "Dave"),
    ("Bob",   "Eve"),
}

# Students from the same city who CANNOT sit adjacent  (report Section 2.1)
CITY_CONSTRAINTS: set[tuple[str, str]] = {
    ("Alice", "Carol"),
    ("Dave",  "Eve"),
}

ALL_CONSTRAINTS = FRIEND_CONSTRAINTS | CITY_CONSTRAINTS


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def violates_constraint(a: str, b: str) -> bool:
    """Return True if placing a and b adjacently breaks any rule."""
    return (a, b) in ALL_CONSTRAINTS or (b, a) in ALL_CONSTRAINTS


def is_valid(arrangement: list[str]) -> bool:
    """
    O(n) verification — checks each adjacent pair once.
    Report Section 2.1: 'The teacher will only have to traverse the row once
    and compare each student with the one sitting next to them.'
    → Figure 6: Linear Time Complexity Verification Diagram
    """
    for i in range(len(arrangement) - 1):
        if violates_constraint(arrangement[i], arrangement[i + 1]):
            return False
    return True


def constraint_count(student: str) -> int:
    """Count how many total constraints involve this student."""
    return sum(1 for (a, b) in ALL_CONSTRAINTS if student in (a, b))


def fmt(arrangement: list[str]) -> str:
    """Format an arrangement as 'Alice | Bob | Carol | ...'"""
    return " | ".join(arrangement)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2.1 — P vs NP: CONSTRAINT CHECKER  (O(n) verification)
# Report: "The verification of the seating arrangement will be easy if the
#          teacher checks the completed seating arrangement by ensuring that
#          the students are sitting next to each other."
# Figure 6: Linear Time Complexity Verification Diagram
# ─────────────────────────────────────────────────────────────────────────────

def demo_constraint_checker() -> None:
    print(f"\n{DIVIDER}")
    print(f"  SECTION 2.1 — CONSTRAINT CHECKER  (O(n) Verification)")
    print(f"  Figure 6: Linear Time Complexity")
    print(DIVIDER)

    print(f"\n  Constraints defined:")
    print(f"  Friend constraints (cannot be adjacent):")
    for a, b in sorted(FRIEND_CONSTRAINTS):
        print(f"    {a} ↔ {b}")
    print(f"  Same-city constraints (cannot be adjacent):")
    for a, b in sorted(CITY_CONSTRAINTS):
        print(f"    {a} ↔ {b}")

    test_cases = [
        (["Alice", "Dave", "Bob", "Carol", "Eve"],  True,  "Known valid arrangement"),
        (["Alice", "Bob",  "Carol", "Dave", "Eve"], False, "Alice–Bob adjacent (friend constraint)"),
        (["Carol", "Dave", "Alice", "Bob",  "Eve"], False, "Carol–Dave adjacent (friend constraint)"),
        (["Dave",  "Eve",  "Alice", "Carol", "Bob"],False, "Dave–Eve adjacent (city constraint)"),
    ]

    print(f"\n  {'Arrangement':<45}  {'Result':<10}  Reason")
    print(f"  {'-'*45}  {'-'*10}  {'-'*35}")
    for arr, expected, reason in test_cases:
        result   = is_valid(arr)
        symbol   = "✓ VALID  " if result else "✗ INVALID"
        assert result == expected, f"Unexpected result for {arr}"
        print(f"  {fmt(arr):<45}  {symbol}  {reason}")

    print(f"\n  Time complexity: O(n) — one pass through n-1 adjacent pairs.")
    print(f"  Verification is EASY (polynomial time) → belongs to class P.")
    print(f"  Finding the arrangement is HARD → closer to NP.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2.2 — BRUTE-FORCE SOLVER  O(n!)
# Report: "One brute force approach is to list all possible seating arrangements
#          of students and then check these arrangements against the set of rules."
# Figures 7, 8, 9
# ─────────────────────────────────────────────────────────────────────────────

def brute_force_solver(students: list[str]) -> list[list[str]]:
    """Generate ALL n! permutations and return only the valid ones."""
    return [list(p) for p in permutations(students) if is_valid(list(p))]


def demo_brute_force() -> None:
    print(f"\n{DIVIDER}")
    print(f"  SECTION 2.2 — BRUTE-FORCE SOLVER  (O(n!) Exhaustive Search)")
    print(f"  Figures 7, 8, 9: Factorial Growth & Flowchart")
    print(DIVIDER)

    total_perms = math.factorial(len(STUDENTS))
    start       = time.perf_counter()
    solutions   = brute_force_solver(STUDENTS)
    elapsed_ms  = (time.perf_counter() - start) * 1000

    print(f"\n  Students           : {', '.join(STUDENTS)}")
    print(f"  Total permutations : {len(STUDENTS)}! = {total_perms}")
    print(f"  Valid solutions    : {len(solutions)}")
    print(f"  Time taken         : {elapsed_ms:.3f} ms\n")

    print(f"  All valid arrangements:")
    for i, sol in enumerate(solutions, 1):
        print(f"    {i:>2}. ✓  {fmt(sol)}")

    # Figure 7 — Factorial growth table
    print(f"\n  Figure 7 — Factorial Growth (why brute-force does not scale):")
    print(f"  {'Students (n)':<15}  {'n!':<25}  {'Feasible?'}")
    print(f"  {'-'*15}  {'-'*25}  {'-'*15}")
    thresholds = [
        (5,  "Yes  — checked in <1 ms"),
        (8,  "Yes  — ~40,000 checks"),
        (10, "Borderline — 3.6 million"),
        (12, "No   — 479 million"),
        (15, "No   — 1.3 trillion"),
        (20, "No   — 2.4 × 10¹⁸"),
    ]
    for n, note in thresholds:
        f = math.factorial(n)
        print(f"  {n:<15}  {f:<25,}  {note}")

    print(f"\n  Brute-force guaranteed correct — but impractical for n ≥ 12.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2.3 — HEURISTIC (SMART) APPROACH
# Report: "A heuristic method involves the use of a more intelligent approach
#          rather than examining all possible solutions to seating."
# Figures 10, 11, 12
# ─────────────────────────────────────────────────────────────────────────────

def heuristic_solver(students: list[str]) -> tuple[list[str], int]:
    """
    Greedy heuristic — most-constrained-first with deferred insertion.

    Algorithm (matches report Section 2.3):
      1. Start with students sorted by total constraint count (most
         constrained first). Students who have many constraints are
         placed first — they are the hardest to accommodate later.
      2. Try to insert each student at the first valid position in the
         growing arrangement.
      3. If no valid position exists yet (because not enough neighbours
         have been placed), defer the student to the back of the queue
         and try again once more students are in position.

    This dramatically reduces the search space compared to checking
    all n! permutations (Figure 12).
    """
    queue      = sorted(students, key=lambda s: (-constraint_count(s), s))
    placed: list[str] = []
    steps      = 0
    max_defers = len(students) ** 2   # safety cap

    defers = 0
    while queue and defers < max_defers:
        student = queue.pop(0)
        found   = False

        for pos in range(len(placed) + 1):
            steps += 1
            trial  = placed[:pos] + [student] + placed[pos:]
            if is_valid(trial):
                placed = trial
                found  = True
                break

        if not found:
            queue.append(student)   # defer — more neighbours needed first
            defers += 1

    if len(placed) == len(students):
        return placed, steps
    return [], steps


def demo_heuristic() -> None:
    print(f"\n{DIVIDER}")
    print(f"  SECTION 2.3 — HEURISTIC SOLVER  (Greedy Most-Constrained-First)")
    print(f"  Figures 10, 11, 12: Heuristic Strategy & Search Space Reduction")
    print(DIVIDER)

    # Figure 11 — Constraint counts (drives the ordering)
    print(f"\n  Figure 11 — Constraint count per student:")
    print(f"  (Students with more constraints are placed first)")
    print(f"  {'Student':<12}  {'Friend constraints':<22}  {'City constraints':<20}  Total")
    print(f"  {'-'*12}  {'-'*22}  {'-'*20}  {'-'*5}")
    for s in STUDENTS:
        fc = sum(1 for (a, b) in FRIEND_CONSTRAINTS if s in (a, b))
        cc = sum(1 for (a, b) in CITY_CONSTRAINTS   if s in (a, b))
        print(f"  {s:<12}  {fc:<22}  {cc:<20}  {fc+cc}")

    # Run the heuristic
    start      = time.perf_counter()
    result, steps = heuristic_solver(STUDENTS)
    elapsed_ms = (time.perf_counter() - start) * 1000

    total_perms = math.factorial(len(STUDENTS))

    print(f"\n  Result:")
    if result:
        print(f"    Arrangement : {fmt(result)}")
        print(f"    Valid       : {is_valid(result)}  ✓")
        print(f"    Steps taken : {steps}  (heuristic)")
        print(f"    Brute-force : {total_perms}  (all permutations)")
        reduction = round((1 - steps / total_perms) * 100, 1)
        print(f"    Reduction   : {reduction}% fewer steps  → Figure 12")
        print(f"    Time taken  : {elapsed_ms:.4f} ms")
    else:
        print(f"    No arrangement found (backtracking required).")

    # Figure 10 — Side-by-side comparison
    print(f"\n  Figure 10 — Brute-Force vs Heuristic Comparison:")
    print(f"  {'Metric':<30}  {'Brute-Force':<20}  Heuristic")
    print(f"  {'-'*30}  {'-'*20}  {'-'*20}")
    print(f"  {'Permutations evaluated':<30}  {total_perms:<20}  {steps}")
    print(f"  {'Guarantees optimal?':<30}  {'Yes':<20}  Not always")
    print(f"  {'Practical for large n?':<30}  {'No (O(n!))':<20}  Yes (much faster)")
    print(f"  {'Good enough for real use?':<30}  {'Yes (small n)':<20}  Yes (all n)")

    print(f"\n  Report conclusion (Section 2.3.3):")
    print(f"  Although heuristic approaches may not always deliver the absolute")
    print(f"  best outcome, they are highly valuable due to their speed, simplicity,")
    print(f"  and ability to provide realistic solutions in complex situations.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(DIVIDER)
    print("  Classroom Seating Arrangement Solver")
    print("  Task 2 — P vs NP Demonstration")
    print("  Foundation of Computer Science | ST4015CMD")
    print(DIVIDER)
    print(f"\n  Students   : {', '.join(STUDENTS)}")
    print(f"  Friend constraints  : {len(FRIEND_CONSTRAINTS)} pairs")
    print(f"  City constraints    : {len(CITY_CONSTRAINTS)} pairs")
    print(f"  Total constraints   : {len(ALL_CONSTRAINTS)} pairs")

    demo_constraint_checker()
    demo_brute_force()
    demo_heuristic()

    print(f"\n{DIVIDER}")
    print("  All three demonstrations complete.")
    print(DIVIDER)
