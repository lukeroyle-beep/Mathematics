# Independent mathematical and computational review

26 November 2026. **PASS for the reported partial results and their stated
limits. The global-U objective remains unresolved.** No full witness has
been verified, and no complete `{5,7}` exclusion is claimed.

The exact reviewed implementation is
`1c929356a00862a3ad8b6126b8279ad1428a95cf`, based on
`aab83fc4ed706cd4aca4d51dc6e533d60cb87477`. The reviewer was separate from
the proof/checker authors, did not modify implementation files, and did
not commit, publish, or merge. The review artifacts were added after the
implementation commit. Draft-PR publication and its unmerged state are
the publishing agent's separate responsibility.

[`independent-review.json`](independent-review.json) binds all twelve
implementation files, including the repository README and `verify.py`,
to the reviewed commit and exact SHA-256 values. The independent checker
refuses a current-file versus committed-byte mismatch.

## Mathematical review

| Obligation | Finding |
| --- | --- |
| Original decimal predicate | PASS. The word has two fives and `L-2` sevens, `n=F/9`, sum `S=7L-4`, and product `25*7^(L-2)`. Full divisibility is exactly `225S*7^(L-2)|F`. |
| Factor nine and composite S | PASS. `v5(F)=2`, `gcd(25,9S)=1`, and `7∤S` justify the integral cofactor on the eligible domain. Nine is never cancelled modulo a multiple of three. |
| Uniform qualitative bound | PASS. The primitive tuple `(A,-V,-1,-W)` has no proper zero subsum, exact height A, and only W contributes outside `{2,3,5,7}`. The Evertse application proves uniform little-o, with no effective last exception. |
| First ineffective implication | PASS. Theorem 4 of Evertse 1984, p.231, supplies unspecified subspaces; the coefficient tuples after (22), p.232, enter the induction constants and the later height bound. Their effective determination is absent. |
| Quantitative replacements | PASS as a scoped applicability audit. Explicit counts, a computable distinguished exceptional subspace, and interval counts do not bound the unknown largest exterior solution or interval endpoint. The review makes no claim that every possible future method is impossible. |
| Signed effective estimate | PASS. Bugeaud's auxiliary real and p-adic logarithm theorems apply to the separately reduced multiplicative forms, with the stated signs, heights, nonzero exponents and form, and minimal last-exponent valuation. They give `L<10^16 log(max(F/7^t,25))` for `t>=L/2`. The resulting global saving has insufficient exponent. |
| Seven-free quotient family | PASS. For full witnesses, `F/7^t=225S q0` exactly. If `q0<=L^d`, then `L<=10^18(d+1)^2-1`, including `d=0`. No fixed prime support or bound on q itself is assumed. There is no proved d covering all witnesses. |
| Unique actual position and lift index | PASS. The order `6*7^(k-1)` gives at most one actual depth-K position. The first nonzero lift digit has index t; exclusion needs an index at most `L-3`, inclusively. The same-position sum premise is preserved. |
| Composite-S CRT argument | PASS. Prime-power orders give `v7(ord_S(10))<=K-1`; the CRT gcd stabilizes. This prevents the proposed later-incompatibility mechanism but does not control the bounded representative. |
| Decimal-height cutoff | PASS only as a conditional implication. The largest integer satisfying the derived strict inequality is `444444444445`. For `B<L<=3301587301587`, the exact digit count is `d=L-14`, so inequality failure is exactly a full witness on the eligible domain. |
| Moving centres `b<=4K` | PASS. The root's actual global degree, height parameter, derivative loss and every logarithm-maximum branch are retained before bounding them. The polynomial `R(K)` yields `U=902265864195<B`; K<=14, K=15, and K>=16 are all covered. The inherited certificate closes this defined subfamily. |
| Moving centres `b<=K^2` | PASS. The degree-ten polynomial estimate excludes every K>=20, while K=19 gives the tighter `U=1721427606158403`. K<=18 lies below that U. The remaining finite range is explicitly unexhausted. |
| Fixed-depth control | PASS as an inherited theorem with its quantifiers preserved. Fixed t may occur at infinitely many sum-compatible pairs; it cannot be set equal to the simultaneously varying `L-2`. A universal ceiling of 21 is not asserted. |
| Global reporting and coverage | PASS. The unrestricted domain above B has no effective upper endpoint in this work. Position-subfamily bounds and archive row tests are not presented as new whole-length coverage. Both conjectures remain open. |

The key source statements were independently reopened:

- [Bugeaud–Laurent, Corollary 1, printed p.4](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf): unit bases, multiplicative independence, positive exponents, global degree factor, normalized heights and all maximum branches match the polynomial-root application.
- [Bugeaud, Theorems 2.2 and 2.3, printed pp.4–5](https://arxiv.org/pdf/1609.07926): normalized real exponent bound and signed rational p-adic input match the signed estimate. The ordinary-digit Theorem 1.2 is not directly applied to F.
- [Evertse 1984, Corollary 1 and proof, pp.227, 231–235](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf): tuple hypotheses and the specific coefficient dependence agree with the effectivity diagnosis.
- [Evertse 2010, Theorem C and discussion, pp.8–11](https://arxiv.org/pdf/1008.2268), and [Evertse–Ferretti 2013, Theorems 2.1 and 2.3, pp.520, 522](https://annals.math.princeton.edu/wp-content/uploads/annals-v177-n2-p04-p.pdf): computable distinguished subspace and quantitative interval claims do not determine the remaining heights.

The further S-unit, recurrence and probabilistic source statements cited
in ROUTE1 were also checked for the stated applicability limitations.
The mathematical review did not find a sufficient replacement theorem.
This is a result of the investigation, not a theorem of impossibility.

## Independent computation

[`independent_review.py`](independent_review.py) imports no implementation
program. It evaluates the original word as a repunit with the two digit
changes, modulo m:

```
R_L mod m = ((10^L mod(9m))-1)/9,
n mod m = (7R_L-2-2*10^i) mod m.
```

The division is exact in the integers because the residue modulo `9m`
is one modulo nine. This method is valid for `3|m` and differs from the
implementation's concatenation monoid. It independently checks all
74,601 retained pairs modulo S and `7^28`. Every sum residue is nonzero;
the valuation histogram is `63974,9161,1272,162,29,3` at depths 22–27.
The full recomputed row digest agrees with the implementation:
`51fcd6c2c3c4af80ab68c031b84d6c40654e90cc1584eda6a617325beed73625`.

The independent review also checked:

- 9,900 literal pairs for odd `5<=L<=201`, including 27 eligible sum
  passes, 17 with `3|S`.
- Original product-times-sum positive control 135 and negative control
  137; prime and composite sum-positive controls.
- Factor-nine negative `(L,i,S)=(313,51,2187)`, where `n mod S=1944`.
- Independent expanded coefficients for both moving-centre polynomials,
  their exact starting comparisons and induction growth constants.
- Rational logarithm bounds for the Bugeaud–Laurent coefficient below 63,
  the signed-estimate constants, quotient cutoffs and decimal endpoints.

Both implementation programs were freshly run normally and under `-O`,
matching their receipts byte-for-byte. The independent reviewer was run
in both modes at the exact implementation commit, also byte-identically.
The aggregate `verify.py` passed five source bindings, twelve reviewed
artifact bindings and six checker runs. `git diff --check` passed.

One reproduction issue was found and repaired before the reviewed
commit: the old `log_bounds.py` command did not itself assert the needed
coefficient below 63. The new `checks.py` does so with exact rational
enclosures, and MOVING_CENTRES now points to that command. No unresolved
must-fix finding remains.

The two complete archive enumerators, the adjacent million-odd-length
scan and any Lean build were **not rerun**. Completeness for omitted
pairs and consecutive coverage through B remain inherited from the
specified certificates; matching row arithmetic and hashes alone would
not establish them. The new bounds above B leave their stated finite
subfamily ranges unexhausted. No new global U, new consecutive interval,
or verified full witness is supplied by this passing review.

From the repository root:

```sh
python3 research/a398769/five-seven/explicit-length/independent_review.py --commit 1c929356a00862a3ad8b6126b8279ad1428a95cf > /tmp/a398769-independent-review.json
cmp /tmp/a398769-independent-review.json research/a398769/five-seven/explicit-length/independent-review.json
python3 research/a398769/five-seven/explicit-length/verify.py
```
