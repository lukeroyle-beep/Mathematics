# Independent finite result through 75 digits

**No positive integer of at most 75 decimal digits, all 3 or 9, satisfies P(n)S(n) | n in this exhaustive search.** Every length from 1 through 75 is covered; no cases are unfinished. This is a finite computational result for the {3,9} subclass, not a general proof of A398769. The earlier cloud result was neither used nor validated by assumption.

The separate branch is `research/a398769-stage4-search`, created directly from verified proof commit `7c7e44ff8fe622c40b8c5a27a86641b90fe2c797`. The validated implementation and reproduction commands were committed, pushed and remotely read back at **`501989af60a1a8139df346d22f5bbab1792e6c1a` before benchmarks or the full run**. The search sources remained identical throughout.

See [coverage proof and reproduction commands](README.md), [validation evidence](validation.json), [independent review](REVIEW.md), [reproducible final audit](independent-audit.json), [benchmarks](benchmarks.json), [machine-readable coverage](coverage.json), and [run receipt](run-receipt.json).

## Completed computation

All **2,925** (length, number-of-nines) pairs were accounted for: **2,797** excluded by exact necessary conditions and **128** searched to exhaustion. The engine traversed **2,085,772,536 nodes**, covering **1,042,886,332 terminal intervals** and checking **256,817,010 possible interval multiples**. Every completed case matched its independently calculated exact node and leaf counts. The sum of measured C++ search times was **69.118 seconds**; this excludes Python, process launch and checkpoint-writing overhead.

Machine: Apple M4, 10 logical CPUs, 16 GiB RAM; macOS 26.6.2 arm64, Apple clang 21.0.0, GMP 6.3.0. Each case ran on one CPU thread. The 120-second per-case and 1,800-second overall limits were never reached. Every completed result is saved by length and b in [results/](results/). A second driver invocation skipped all completed cases and left all 75 length files byte-identical.

## Benchmarks and feasibility

| Length | Nines b | Benchmark status | Nodes visited | Seconds | Estimated complete seconds |
|---:|---:|---|---:|---:|---:|
| 27 | 18 | complete | 15 | 0.000038 | 0.000038 |
| 51 | 15 | complete | 262,107 | 0.006412 | 0.006412 |
| 75 | 3 | complete | 14,351 | 0.000597 | 0.000597 |
| 75 | 12 | limited | 95,608,832 | 3.000033 | 18.937752 |
| 75 | 21 | limited | 93,323,264 | 3.000020 | 8.622740 |
| 75 | 39 | complete | 524,287 | 0.015206 | 0.015206 |
| 75 | 66 | complete | 63 | 0.000139 | 0.000139 |

The two `limited` benchmark records are three-second samples, not exclusion evidence. Their work estimates were used only to assess feasibility; the corresponding full runs below exhausted both cases. The middle-range case b=39 also completed during the benchmark.

## All seven surviving length-75 cases

| Nines b | Status | Terminal intervals | Interval candidates checked | Seconds | Witnesses |
|---:|---|---:|---:|---:|---:|
| 3 | complete | 7,176 | 488 | 0.000602 | 0 |
| 12 | complete | 301,766,029 | 52,673,860 | 19.303198 | 0 |
| 21 | complete | 134,116,144 | 19,956,109 | 8.873786 | 0 |
| 39 | complete | 262,144 | 77,224 | 0.015549 | 0 |
| 48 | complete | 16,384 | 2,183 | 0.000943 | 0 |
| 57 | complete | 512 | 322 | 0.000168 | 0 |
| 66 | complete | 32 | 16 | 0.000141 | 0 |

## Coverage of every requested length

Every row covers every b from 0 through L. Listed b values were searched to exhaustion; the other count cases were excluded by the proved necessary conditions in the search note. Empty search lists mean the whole length is excluded mathematically. The per-case JSON files retain each exclusion reason.

| Length L | Excluded count cases | Exhausted b values | Coverage | Witnesses |
|---:|---:|---|---|---:|
| 1 | 2 | none | complete | 0 |
| 2 | 3 | none | complete | 0 |
| 3 | 4 | none | complete | 0 |
| 4 | 5 | none | complete | 0 |
| 5 | 5 | 2 | complete | 0 |
| 6 | 7 | none | complete | 0 |
| 7 | 7 | 1 | complete | 0 |
| 8 | 9 | none | complete | 0 |
| 9 | 9 | 0 | complete | 0 |
| 10 | 11 | none | complete | 0 |
| 11 | 11 | 8 | complete | 0 |
| 12 | 13 | none | complete | 0 |
| 13 | 13 | 7 | complete | 0 |
| 14 | 15 | none | complete | 0 |
| 15 | 15 | 6 | complete | 0 |
| 16 | 17 | none | complete | 0 |
| 17 | 17 | 5 | complete | 0 |
| 18 | 19 | none | complete | 0 |
| 19 | 19 | 4 | complete | 0 |
| 20 | 21 | none | complete | 0 |
| 21 | 21 | 3 | complete | 0 |
| 22 | 23 | none | complete | 0 |
| 23 | 22 | 2, 20 | complete | 0 |
| 24 | 25 | none | complete | 0 |
| 25 | 24 | 1, 19 | complete | 0 |
| 26 | 27 | none | complete | 0 |
| 27 | 26 | 0, 18 | complete | 0 |
| 28 | 29 | none | complete | 0 |
| 29 | 28 | 17, 26 | complete | 0 |
| 30 | 31 | none | complete | 0 |
| 31 | 30 | 16, 25 | complete | 0 |
| 32 | 33 | none | complete | 0 |
| 33 | 32 | 15, 24 | complete | 0 |
| 34 | 35 | none | complete | 0 |
| 35 | 33 | 14, 23, 32 | complete | 0 |
| 36 | 37 | none | complete | 0 |
| 37 | 35 | 13, 22, 31 | complete | 0 |
| 38 | 39 | none | complete | 0 |
| 39 | 37 | 12, 21, 30 | complete | 0 |
| 40 | 41 | none | complete | 0 |
| 41 | 38 | 11, 20, 29, 38 | complete | 0 |
| 42 | 43 | none | complete | 0 |
| 43 | 40 | 10, 19, 28, 37 | complete | 0 |
| 44 | 45 | none | complete | 0 |
| 45 | 42 | 9, 18, 27, 36 | complete | 0 |
| 46 | 47 | none | complete | 0 |
| 47 | 44 | 8, 17, 26, 35 | complete | 0 |
| 48 | 49 | none | complete | 0 |
| 49 | 46 | 7, 16, 25, 34 | complete | 0 |
| 50 | 51 | none | complete | 0 |
| 51 | 48 | 6, 15, 24, 33 | complete | 0 |
| 52 | 53 | none | complete | 0 |
| 53 | 49 | 5, 14, 23, 32, 50 | complete | 0 |
| 54 | 55 | none | complete | 0 |
| 55 | 51 | 4, 13, 22, 31, 49 | complete | 0 |
| 56 | 57 | none | complete | 0 |
| 57 | 53 | 3, 12, 21, 30, 48 | complete | 0 |
| 58 | 59 | none | complete | 0 |
| 59 | 54 | 2, 11, 20, 29, 47, 56 | complete | 0 |
| 60 | 61 | none | complete | 0 |
| 61 | 56 | 1, 10, 19, 28, 46, 55 | complete | 0 |
| 62 | 63 | none | complete | 0 |
| 63 | 57 | 0, 9, 18, 27, 45, 54, 63 | complete | 0 |
| 64 | 65 | none | complete | 0 |
| 65 | 60 | 8, 17, 26, 44, 53, 62 | complete | 0 |
| 66 | 67 | none | complete | 0 |
| 67 | 62 | 7, 16, 25, 43, 52, 61 | complete | 0 |
| 68 | 69 | none | complete | 0 |
| 69 | 63 | 6, 15, 24, 42, 51, 60, 69 | complete | 0 |
| 70 | 71 | none | complete | 0 |
| 71 | 65 | 5, 14, 23, 41, 50, 59, 68 | complete | 0 |
| 72 | 73 | none | complete | 0 |
| 73 | 67 | 4, 13, 22, 40, 49, 58, 67 | complete | 0 |
| 74 | 75 | none | complete | 0 |
| 75 | 69 | 3, 12, 21, 39, 48, 57, 66 | complete | 0 |

## Validation and limits of the conclusion

Direct enumeration using the original actual-digit product and sum checked all 131,070 strings at lengths 1–16. It agreed with the reduced engine and the parity exclusions. The generic search controls covered 176 cases with 654 nonzero hits, plus an explicit five-hit control and 75-digit arithmetic controls. An always-zero implementation would fail. Independent review and a separate build reproduced the validation suite. Resource-limit and incomplete-coverage controls passed.

The finite search implementation is justified by the interval partition argument and tested independently at small lengths; its 75-digit output is not a Lean kernel certificate. The original Lean reduction is unchanged. No witness appeared, so there is no candidate integer or quotient to report. No work remains within the requested range.
