# Explicit length-bound investigation

26 November 2026. **No unconditional global integer U has been proved.**
No full witness was found. The `{5,7}` subclass and the wider digit-1
conjecture remain open. The strongest new results are unconditional
explicit bounds for the precisely defined subfamilies below, one of which
is completely excluded by the inherited finite certificate. These are
ordinary proofs and exact computations, not new Lean formalizations.

The isolated branch starts at current `main`,
`aab83fc4ed706cd4aca4d51dc6e533d60cb87477` (merge of PR #22).
`decimal-height/` is absent there. Its proof and review were read at
the requested PR #23 commit
`c977422826ce674d4068c0517afb1f75fc368893`, without treating it as merged.
[`baseline.json`](baseline.json) binds all four requested inputs and the
review to their exact bytes and refs. No earlier working checkout was edited.

## Exact target and verified outcomes

Every possible residual witness has odd `L>=5`, `3<=i<L`, two fives
at positions zero and i, and sevens elsewhere. Define

```
S=7L-4, F=7*10^L-18*10^i-25, t=v7(F),
n=F/9, P=25*7^(L-2), K=min{k>=1:6*7^(k-1)>L}.
```

The full predicate is `PS|n`, equivalently `225S*7^(L-2)|F`.
On `5∤S` and **`9S|F`**, it is exactly `t>=L-2`. All conditions
refer to the same actual position i. Composite S is included throughout;
nine is never cancelled modulo S. The consecutive certified endpoint is
`B=1000002000000` inclusive, inherited from PR #22 plus PR #21.

| Scope | Proved result | Remaining obligation |
| --- | --- | --- |
| Every eligible pair | Uniform `t=o(L)` remains qualitative; inspected effective replacements supply no global U | An explicit bound on exceptional heights, or a sufficient alternative uniform estimate |
| A full witness with some reduced `0<a<b<=4K`, `|bi-aL|<=K^2` | **`L<=902265864195<B`** | None: this entire subfamily is excluded by the existing certificate |
| A full witness with some reduced `0<a<b<=K^2`, `|bi-aL|<=K^2` | **`L<=1721427606158403`** | Odd lengths in `(B,1721427606158403]`, after other certified exclusions, remain unexhausted |
| A full witness with `q=n/(PS)`, `q0=q/7^v7(q)<=L^d`, fixed integer `d>=0` | **`L<=10^18(d+1)^2-1`** | Odd lengths in `(B,10^18(d+1)^2-1]`, after other certified exclusions, remain unexhausted |
| All 74,601 retained pairs reaching `t>=22` through `10^12` | **Zero exact digit-sum passes**, independently recomputed | Completeness of the retained list is inherited, not rerun |

The quotient theorem allows arbitrary prime factors in q0. For `d=0`
its bound is `999999999999999999`; for `d=100` it is
`10200999999999999999999`. There is no proved fixed d for all witnesses.
Likewise no coverage theorem puts every possible witness in either
rational-centre subfamily. Thus none of these numbers is a global U.

The wider bounded-denominator remainder has roughly `8.6*10^14` odd
lengths before position restrictions; the other displayed remainders are
larger. They were not exhaustively scanned. The new narrower-centre
exclusion removes every pair admitting `b<=4K` from the wider family,
but does not discharge the remaining pairs. Existing all-length position
strips, isolated lengths and sampled-length certificates retain their own
scopes. PR #23's scattered checks are available at its specified commit;
they are not converted into consecutive intervals or newly rerun here.

## Where the global arguments stop

**Route 1.** [ROUTE1.md](ROUTE1.md) traces Evertse's Corollary 1 (1984,
p.227) through Theorem 4 (p.231) to dependence on unspecified exceptional
subspace coefficients after (22), p.232. The resulting height bound on
pp.234–235 is ineffective. An explicit number of exceptions, an effective
exceptional subspace, or a bounded number of intervals with unknown
locations does not bound the largest exceptional height. Newer primary
sources and the signed logarithm substitution are checked there, including
the seven-free-quotient theorem and its constants.

**Route 2.** [ROUTE2.md](ROUTE2.md) starts with a full witness and the
unique actual position `i=r_K`. The first missing implication is that
`9S|F(L,r_K)` and `5∤S` force a nonzero lift digit at an inclusive index
`K<=j<=L-3`. Exact CRT compatibility stabilizes by depth K, including
composite S, and does not supply a bound for the actual representative.
The residual quotient has unrestricted prime factors. The decimal-height
cutoff `444444444445` remains conditional. On
`B<L<=3301587301587`, failure of that inequality is exactly the witness
condition, so it cannot be used as an already proved exclusion there.

[MOVING_CENTRES.md](MOVING_CENTRES.md) supplies the new gap-free subfamily
result; ROUTE2 gives the wider denominator bound. Both keep the actual
global degree, root height, derivative valuation, and the changing
denominator in Bugeaud–Laurent's explicit bound. No fixed-parameter
constant is silently reused as a uniform one.

For calibration, if an explicit estimate
`t<=(1-delta)L+C`, `delta>0`, holds on the whole eligible domain for
`L>=L0`, then `t>=L-2` gives `delta*L<=C+2`. Every witness would satisfy
`L<=max(L0-1,floor((C+2)/delta))`. This deduction is exact, but no such
global triple is supplied here. The stronger subfamily bounds use their
own integer endpoint arguments instead.

## Evidence and inherited completeness

[ARCHIVE.md](ARCHIVE.md) records independent original decimal-block
evaluation modulo S and separate sparse evaluation modulo 9S, including
24,873 cases with `3|S`. Both methods agree on every retained pair.
The exact valuation histogram at depths 22–27 is
`63974,9161,1272,162,29,3`. Positive controls include a composite sum
and the original product-times-sum predicate; a negative control detects
the lost factor nine.

The two complete archived enumerations, the all-pattern reduction and
small-case exclusions, and PR #21's adjacent million-odd-length scan are
explicitly inherited. Fresh hash checks bind their sources and receipts;
fresh row checks do not establish omitted-pair completeness. Neither
large enumeration nor the adjacent scan was rerun. No new consecutive
length coverage is claimed.

The [fixed-depth theorem](../fixed-depth/PROOF.md) gives infinitely many
actual sum-compatible pairs at every fixed positive depth. Therefore
the finite observed ceiling of 21 on sum-compatible pairs cannot be
imposed above B. Fixing t before letting L grow does not give `t>=L-2`.

The outstanding unrestricted domain is still odd `L>B`, with all
previously certified positions and isolated lengths removed. It has no
proved effective upper endpoint. Closing this subclass would leave the
wider digit-1 conjecture open; a verified `{5,7}` witness would refute both.

## Reproduction and review

From the repository root, using Python 3 and the existing Git history:

```sh
git fetch origin c977422826ce674d4068c0517afb1f75fc368893
git show c977422826ce674d4068c0517afb1f75fc368893:research/a398769/five-seven/decimal-height/PROOF.md
python3 research/a398769/five-seven/explicit-length/checks.py
python3 -O research/a398769/five-seven/explicit-length/checks.py
python3 research/a398769/five-seven/explicit-length/archive_control.py
python3 -O research/a398769/five-seven/explicit-length/archive_control.py
python3 research/a398769/five-seven/explicit-length/verify.py
```

The normal and optimized outputs match the retained deterministic receipts.
The checks use explicit exceptions, exact integers and rational logarithm
enclosures; they do not rely on Python assertions or rounded logarithms.
The proof source, arithmetic controls, and finite coverage are separate
evidence classes. The independent mathematical/computational review and
its exact implementation-commit binding are recorded in
[REVIEW.md](REVIEW.md). No Lean build, global proof, or full witness is
claimed by a passing review.
