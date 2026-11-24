# Independent pre-run review

On 24 November 2026, a separate reviewer checked the C++ interval search and
Python driver. The review found no missed-candidate defect in the interval
endpoints, odd-quotient selection, recursive partition, or arithmetic exclusions.
It additionally compared 248 generic cases at lengths 2,5,9,11 and divisors
3,7,19,27,81,99,333,1001 against direct enumeration: all agreed, with 1,454
positive hits. The committed `validate` command supplies the repeatable test
suite; this review is additional evidence, not a substitute for that suite.

Operational findings were addressed before the initial push:

- Added a per-directory advisory lock to prevent concurrent writers from
  replacing each other's completed-case records.
- Refuse Python optimized mode so validation assertions cannot be disabled.
- Stop on any retained witness before retrying a limited case, preserving it
  in the current result rather than hiding it in attempt history.
- Added coverage tests requiring both missing and limited cases to remain
  unfinished, along with the completed-case resume test.

An independently derived work recurrence also predicts the exact node and leaf
counts for each complete search. The runner checks these counts both on new
results and when loading saved results.
