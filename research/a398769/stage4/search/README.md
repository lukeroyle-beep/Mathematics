# Independent exact {3,9} search through 75 digits

The [completed result and every-length coverage table](RESULTS.md) report zero
witnesses, with all cases through 75 digits exhausted or excluded.

This search starts from proof commit
`7c7e44ff8fe622c40b8c5a27a86641b90fe2c797`, on the separate branch
`research/a398769-stage4-search`. No earlier cloud search result is an input,
validation oracle, or evidence for this computation. The unchanged Lean theorem
proves the reduction; the C++ search and its coverage argument below are a
separate computational verification, not a kernel-checked finite Lean proof.

## Exact reduction and exclusions

For a length-L positive decimal integer n consisting only of 3 and 9, let b
count its nines. Division by 3 is digitwise, with no carries: m=n/3 has L
digits in {1,3}, exactly b of them 3. The proved reduction is

```
P(n) S(n) | n  iff  D | m,
D = 3^(L+b) (L+2b).
```

Every pair 1 <= L <= 75, 0 <= b <= L is accounted for. The following necessary
conditions exclude pairs before enumeration:

1. L must be odd: n is odd, whereas S(n)=3(L+2b) is even if L is even.
2. If L+b >= 2, then 9 divides D, so m's digit sum L+2b must be divisible
   by 9. The one remaining pair L=1,b=0 fails the analogous modulo-3 test.
3. If 5 divides L+2b, then 5 divides D; this is impossible for m ending in
   1 or 3.
4. If D is larger than the maximum arrangement (b threes followed by L-b
   ones), no positive multiple fits.

At L=75, the modulo-9 condition gives b=3,12,21,30,39,48,57,66,75. The
factor-5 test removes 30 and 75, leaving exactly **3,12,21,39,48,57,66**.
None of these filters assumes the desired conclusion.

## Why every remaining word is tested or excluded

The generic C++ engine takes L,b and any positive odd divisor D. Let
R_j=(10^j-1)/9, including R_0=0. At a recursion node, `value` is the chosen
prefix followed by all ones, r digits remain, and k must become threes.
All completions lie in the exact interval

```
lower = value + 2 R_k
upper = value + 2 * 10^(r-k) R_k
width = 2 R_k (10^(r-k)-1).
```

These endpoints put the remaining threes respectively in the least and most
significant available positions. Since m and D are odd, the possible multiples
are precisely D times the positive odd integers, spaced 2D apart.

If `width < 2D`, integer ceiling division finds the first odd multiple at least
`lower`. If it exceeds `upper`, the whole interval is excluded. Otherwise it is
the only possible multiple in that interval, and the engine checks its exact
length, allowed digits and number of threes. A low-six-digit test merely rejects
an integer with a forbidden decimal digit before converting its entire value.
For k=0 or k=r, width is zero, so the unique arrangement is tested this way.

If `width >= 2D`, the engine branches on the next digit, using 1 when k<r and
3 when k>0. These branches partition every admissible completion and strictly
decrease r. Thus the recursion terminates and leaves no admissible word
unaccounted for. The Python driver independently computes the exact tree size
by a small dynamic program and requires every completed search to have the
predicted node and leaf counts. It does not infer absence from a sample, a
timeout, a divisibility estimate, or separate divisibility by P and S.

All divisors, powers, endpoints, quotients and candidate integers use GMP
arbitrary-precision integers in C++ and Python integers in the driver. Only
bounded indices and overflow-checked work counters use fixed-width integers.
Floating point is used solely to display elapsed time and set resource limits.

## Reproduce

Requirements: Python 3.8+, a C++17 compiler, GMP headers and libraries. On this
Mac GMP 6.3.0 is already under `/opt/homebrew`; no package installation is done
by these scripts. `GMP_PREFIX` overrides that prefix, `CXX` the compiler, and
`A398769_BUILD` the temporary build directory (default
`/private/tmp/a398769-stage4-build`). Run from the repository root, without
Python's `-O` option:

```sh
python3 research/a398769/stage4/search/search.py build
python3 research/a398769/stage4/search/search.py validate --output research/a398769/stage4/search/validation.json
```

Validation enumerates **all 131,070 words over {3,9} at lengths 1 through 16**
using their original actual digit product and sum. It compares against the
reduced engine for every odd-length count, including mathematically excluded
counts; even lengths are checked against their parity exclusion. It also checks
176 generic cases at lengths 1 through 8 against direct enumeration using
divisors 1,9,17,101, and three 75-digit arithmetic cases with b=1. These controls
contain nonzero answers. In particular, L=9,b=3,D=17 must return exactly

```
111133131 111331113 113131311 133113111 311113311
```

These control integers exercise the search mechanism; they are not asserted
to satisfy the original P(n)S(n) condition. An always-zero implementation fails
the controls. Node and time limits must produce `limited`, and a second run
over completed checkpoint files must preserve them byte for byte.

**Commit and push the validated implementation and these commands before the
following benchmarks or large runs.** Record that remote commit in the result
report. Representative bounded benchmarks include the middle count L=75,b=39
and the much larger L=75,b=12 and b=21 traversals:

```sh
python3 research/a398769/stage4/search/search.py benchmark --seconds 3 --output research/a398769/stage4/search/benchmarks.json
python3 research/a398769/stage4/search/search.py run --case-seconds 120 --total-seconds 1800
python3 research/a398769/stage4/search/search.py summarize --output research/a398769/stage4/search/coverage.json
```

Repeat `run` to skip all completed cases and retry only unfinished ones.
Optional case limits bound resources and never certify exhaustion. Increase
the limit after checking timings, or use zero (the default) for no limit:

```sh
python3 research/a398769/stage4/search/search.py run --only-length 75 --b 12 --case-seconds 600
python3 research/a398769/stage4/search/search.py run
```

`--results PATH` selects a separate result directory. Each
`results/length-LL.json` contains records indexed by b, saved atomically after
each case with status `excluded`, `complete`, or `limited`. A limited case is
restarted from its beginning; completed cases are never redone on resume.
Prior limited attempts are retained when a case is retried. An abrupt process
kill can lose the current case, but previously completed cases remain reusable.
An advisory lock enforces one writer per result directory. Source hashes bind records to the exact
Python and C++ sources; incompatible records are rejected. Build/compiler
metadata and binary hashes are retained with each actual run.

The coverage report lists every length and every unfinished surviving (L,b)
pair. Pure mathematical exclusions are also reported if an interrupted run
never wrote their records. A `complete` status certifies traversal exhaustion,
not merely that no witness has appeared so far. Any witness is independently
checked from the original n's digits in Python and reported with P(n), S(n)
and the exact quotient n/(P(n)S(n)). The run stops after the case containing a
witness is recorded.

The generic engine can also be invoked directly:

```sh
/private/tmp/a398769-stage4-build/search 9 3 17
```

Its arguments are `L B ODD_DIVISOR [MAX_NODES] [MAX_MILLISECONDS]`; omitted or
zero limits mean unlimited. It prints one JSON record. Timing extrapolations
are feasibility estimates; only exhausted cases establish the finite result.
The search addresses the {3,9} subclass through 75 digits, not numbers with
digits 5 or 7 and not the unrestricted A398769 conjecture.

## Audit retained results independently

After reproducing the completed run, verify every count case, every exclusion
and every traversal count without importing the search driver:

```sh
python3 research/a398769/stage4/search/audit_results.py --output /private/tmp/a398769-independent-audit.json
```

The auditor uses a separate level-by-level count calculation and checks source
and recorded build hashes. It rejects missing, limited, extra or witness-bearing
cases; it is specifically an audit of this completed zero-witness result. The
retained receipt is [independent-audit.json](independent-audit.json).
