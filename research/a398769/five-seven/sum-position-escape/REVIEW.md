# Independent review and publication record

Implementation reviewed at **`d7bd64fa6220c4c0ee810ce49553b80a5b6a8222`**.
Two separate reviewer agents inspected the final committed sources and
receipts; the independent arithmetic implementation was written by a third
agent without reading or importing the primary implementation.

Both final reviewers returned **PASS with no unresolved findings** at
that exact implementation commit. Their independently checked bindings
match [verification.json](verification.json). The implementation changes
ten files, all new and confined to this directory. All **1,016** inherited
tracked files remain byte-identical to the fetched main commit.

## Mathematical review

The independent reviewer derived the original full predicate, complete
sum subgroup and CRT conditions, exact h-period and shallow compatibility,
and c<=K. The reviewer checked the equivalence between the missing
`h_(L-2)>M` bound and escape at a lift index in `[K,L-3]`, including
why a first change at L-2 is too late. The S=3^a order, unique candidate,
factor-nine precision, recurrence and limitation of pairwise constraints
were independently derived in [MATH_REVIEW.md](MATH_REVIEW.md).

The reviewer inspected both arithmetic implementations, independently
executed the small subgroup and deadline controls, compared the complete
128-row receipts, and verified all six deliberate receipt corruptions
were rejected. The reviewed conclusion is a precise unresolved implication
and 128 finite exclusions, not an all-length theorem or effective cutoff.

## Arithmetic and evidence review

The separately implemented checker derives n from decimal blocks, obtains
each sum class from scratch, verifies the exact order and full non-seven
divisor at the actual position, and finds its first failing seven power.
It agrees on all 128 lengths with the primary's F-based recurrence lifts:
42 class misses, 86 actual positions, histogram `{1:76,2:8,3:2}`. The
inherited a=25 control is independently recovered. Both implementations
use explicit checks that remain active under optimization.

A separate evidence reviewer checked the 706 inherited input bindings,
712 inherited manifest references (with the historical README exception
explicitly bound to its actual prior Git blob), consecutive coverage,
independent arithmetic architecture, all ordered rows and failure residues,
and the six corruption controls. That reviewer also ran the inherited
PR #26 verifier normally and under -O; both passed. No large historical
enumeration was rerun. At the final implementation commit the reviewer
verified all nine verification-artifact bindings and preservation of every
inherited tracked file.

## Findings and final validation

One substantive test-coverage finding was repaired before the implementation
commit: the initial primary literal-word control range ended at L=101 and
contained no factor-nine negative. Its explicit nonvacuity check failed.
Extending through L=321 recovered the required residual-position negative
at L=313, i=51. The final suite contains 25,440 literal words, including
positive full-sum controls. No failed draft output is retained as evidence.
A minor sentence was also clarified to say the programs import no shared
arithmetic implementation; they both use Python's standard library.

Fresh final commands all passed:

```
python3 primary.py
python3 -O primary.py
python3 independent.py
python3 -O independent.py
python3 verify.py --write
python3 verify.py
python3 -O verify.py
```

The arithmetic programs' normal and optimized outputs are byte-identical
to their retained receipts. Both final verification summaries match. The
verifier reruns both arithmetic programs in both modes and compares all
128 cases, the a=25 control and 128 recurrence links. Six corrupted receipts
(missing case, duplicate exponent, false position, wrong failure residue,
bad depth and wrong control) are rejected. Git whitespace validation passes.

The follow-up commit containing this review record changes only REVIEW.md
and review.json. It does not change the reviewed proof, arithmetic, input
bindings or verification receipt. Those implementation bytes are pinned
by the reviewed commit and artifact hashes above.

## Main and scope at publication

Both the initial fetch and the final pre-publication refresh returned
**`9d958f86fc81188de68af97909614e23a186df9f`**, the actual PR #26 merge.
Git ancestry and the merge commit's parents were checked. There was no
later main work to integrate. Publication uses the separate research branch
`research/a398769-sum-position-escape`; the pull request is a draft and
must remain unmerged for Luke.

Consecutive exclusion remains 1 through 1,000,002,000,000 inclusive.
The 128 specified S=3^a lengths are excluded through a=793; a=799 is the
next unchecked exponent in this sequence. No global cutoff, witness,
infinite-family settlement, new Lean formalization or Lean build is
claimed. The unrestricted {5,7} and wider A398769 questions remain open.
