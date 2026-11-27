# Independent review of the adjacent-pair theorem

**PASS: no unresolved mathematical or computational finding.**

Reviewed implementation commit:
`0a978f53b10122ebeb2059a098005ac02b1bf5c3`.
Base and publication-time main:
`42e6a151c5279905a3e02b859c6fae737178fd7d`.
The base contains the requested PR #28 merge, whose first parent is
`0a47180b889b392c2323bc1614a473af51f38d78`.
The root agent fetched main again before publication and observed no later
commit. Merging remains Luke's decision; this is a draft handoff.

Reviewer context: `/root/eliminant_review`. Builder context: `/root`.
The reviewer independently authored the finite-difference modular checker,
then reviewed the root agent's separate recurrence/automatic-differentiation
checker and pair proof. The logarithm specialist `/root/logarithm_review`
authored the separate logarithm proof; the final reviewer independently
reviewed that proof, its source application and exact bounds. The individual
specialist authored the fresh decimal-block and ternary-lift calculation.
This separation distinguishes independent authorship from review of one's
own code. The independently written implementations share no arithmetic
imports, except the explicitly identified reuse of the inherited Newton/log
method in `root_log_check.py`.

## Mathematical findings

- The original predicate is retained exactly: `PS|n` iff
  `225*S*7^(L-2)|F`, with **9S|F** at the same actual position. Once the
  other factors pass, `v7(F)=L-2` is already sufficient for a witness.
- Full-sum compatibility and the odd position class give `s'-s=2dk`.
  Actuality proves `0<=k<=468`. The period-seven transition test modulo
  343 includes all 3,283 start/increment combinations and leaves precisely
  the nine k values congruent to 42 modulo 49.
- The exact eliminant identity and positivity hold, including the extreme
  allowed increments. Only a **pair** of full witnesses forces divisibility
  by `7^(L-2)`. The smaller length's threshold is used throughout.
- The restriction `w=4 mod6` and period 294 make the derivative test
  complete. All 441 eligible cases give residue **49 modulo 343**.
  Automatic differentiation, finite differences and expanded differentiation
  agree on every case, rather than just their counts.
- The rescaled polynomial `H(x+343Y)/7^5` gives a simple Hensel problem
  when `v7(H(x))>=5`. Taylor expansion proves the exact equality
  `v7(H(x))=2+v7(x-alpha)`; the root's derivative has valuation two.
  Positivity excludes a zero polynomial value, and taking sixth powers
  preserves the distance valuation.
- The minimal-polynomial/Mahler-measure argument bounds absolute
  logarithmic height without assuming H is monic or irreducible.
  Its degree is at most 6561 and its coefficient norm is below `10^4688`.
  The proposed height parameters 15 and 70000 meet all source conditions.
- The reviewer independently reopened Bugeaud--Laurent's primary PDF,
  checking printed pages 2--4 and Corollary 2 on page 5. The explicit
  208 estimate, actual D, principal-unit and independence hypotheses,
  positive exponents and b-prime denominators are used correctly.
  There is no hidden asymptotic exponent threshold. The logarithm
  specialist separately downloaded and hashed the primary source, recorded
  in `SOURCES.md`; the reviewer inspected the formula through the web tool.
- In the dependent case the place above two gives
  `-4687e<=r<0`, `e<=6561`. The torsion identity in Q_7 gives
  `alpha^(6e)=10^(6r)`. The positive integer `ew-r` proves nonvanishing,
  and lifting the exponent gives the sharper equality
  `v7(x-alpha)+v7(e)=1+v7(ew-r)`. This case does not misuse the independent
  logarithm bound.
- Independent exact integer arithmetic confirms
  `C=1618798436980968297600000`, `C+2<10^30`, and the strictly positive
  crossover gap at a=100. The induction polynomial
  `2a^2+78a+759` proves the comparison for every integer a>=100.
  All twelve smaller admissible starts are excluded individually, including
  a=97 in the cutoff-crossing pair `(97,103)`.

The proposed adjacent-pair theorem is therefore proved for every `u>=0`.
No false or unsupported step remains in this proof. It is not an argument
for individual emptiness: if both neighbours fail, both pair statements
are already satisfied and impose no condition on the middle member.

## Exact computations and source binding

The reviewer ran the new aggregate verifier at the frozen implementation
commit normally and under `python3 -O`. Both runs passed and their
outputs were byte-identical. Every source file used by these runs was
compared with its exact bytes at the reviewed commit. The five programs are:

1. `pair_checks.py`: complete recurrence transitions, dual-number
   derivatives, eliminant identities, degree and coefficient-norm checks.
2. `independent_modular.py`: independent complete transition enumeration
   and finite-difference derivatives, with no primary arithmetic imports.
3. `logarithm_checks.py`: expanded derivatives, rational exponential
   inequalities, exact constants/cutoff and nine nonzero strong-Hensel
   controls, including controls with valuations six and seven.
4. `individual_check.py`: all-three-lift ternary enumeration and original
   decimal-block verification at every finite start, a=103 and a=1567.
5. `root_log_check.py`: explicitly declared reuse of PR #28's separately
   derived Newton/root/log calculation, at two precisions, independently
   agreeing on the new a=1567 representative and valuation.

All three derivative tables agree in full. The individual methods give an
actual unique candidate at **a=1567** with **`v7(F)=1`** and original-word
residue **`n mod49=7`**. The full sum and five factors pass at that same
position. The independent review checker adds a repunit calculation,
using exact division modulo `9m`, to check every actual newly reported
original word, its non-seven factors and its first failing seven power.
It imports no implementation arithmetic.

The retained **a=25 sum-positive** control has residues `[0,0,294]` modulo
`[7,49,343]`; it is not a full witness. The **(313,51) lost-factor-nine**
negative gives `F modS=0`, `F mod9S=17496`, and `n modS=1944`.
The aggregate's nine corrupted-receipt tests all reject: missing transition,
lost increment endpoint, missing/false derivative, false cutoff, omitted
crossing start, false a=1567 residue, lost factor nine and false Hensel loss.
Every check uses explicit exceptions and remains active under optimization.

`review_check.py` and `review-checks.json` bind **all 20 changed
implementation paths**, including the root README, against `git show` at
the reviewed commit. They also verify the complete 1,045-file base archive
and confirm all 1,044 inherited files other than the root README remain
unchanged. The review record, review checker and its receipt are added
subsequently and are not presented as files inside that implementation
commit. No historical hash binding is rewritten.

The root agent additionally reported fresh normal and optimized runs of
PR #28's aggregate and source-bound review checker **before** adding the
new root README entry. Those runs passed, including all 256 inherited
individual cases, the complete three-length computations and 25,440 literal
word controls. This is root-observed evidence; the final reviewer did not
rerun those historical programs. The trillion archive and adjacent interval
remain inherited evidence, and their large searches were not rerun.
No GitHub workflow files are configured in this base. No hosted CI run is
claimed by this local mathematical review.

## Reproduction and scope

From the repository root:

```sh
pp=research/a398769/five-seven/power-three-pair
PYTHONDONTWRITEBYTECODE=1 python3 "$pp/verify.py" --run
PYTHONDONTWRITEBYTECODE=1 python3 -O "$pp/verify.py" --run
python3 "$pp/review_check.py" --check "$pp/review-checks.json"
python3 -O "$pp/review_check.py" --check "$pp/review-checks.json"
git diff --check
```

The pair theorem is universal in the stated family. The individual
certificates exclude **257 specified lengths**, through a=1567; the next
unchecked exponent is **1573**. Individual emptiness remains open.
Consecutive whole-length coverage remains **1–1,000,002,000,000 inclusive**;
its first unproved odd length is **1,000,002,000,001**. The unrestricted
`{5,7}` subclass and wider digit-1 conjecture remain open. No Lean theorem,
Lean formalization or Lean build was performed in this work.
