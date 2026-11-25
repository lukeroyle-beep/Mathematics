# Independent adversarial review

Reviewer context: `/root/adversarial_review`, 25 November 2026. This context
did not author either finite-audit implementation, the search, or the
mathematical proof. It reviewed the complete new sources, receipts and prose,
and the inherited high-depth setup. The independent review program below was
written only after that review, to cross-check the completed search.

**Verdict: no outstanding must-fix finding.** The justified primary outcome is
**no structural advance; finite evidence audited**. Neither broad (E), the
all-length `{5,7}` subclass, nor the wider digit-1 conjecture is proved.

## Mathematical assessment

The exact divisor `225*S*7^(L-2)` follows from `F=9n`. On the actual-position
domain, the suffix fixes `v_5(n)=2`; after excluding `5|S`, the separated
condition uses `9S|F`, with no invalid cancellation modulo S.

The order of 10 modulo `7^k` is `6*7^(k-1)`. Its equality with the unit-group
size gives one exponent representative. Since `T_K>L`, a position in
`3<=i<L` with depth at least K must equal `r_K`. Conversely an actual `r_K`
has that depth. This proves the precise equivalence used by the audit,
including its strict endpoints. Positive depth implies `i=3 mod6`; it is not
an assumed restriction on all full-sum positions. The integer induction
establishing `K<=L-2` is valid, so a future proof of E would indeed suffice
for the subclass after the inherited complementary cases.

The CRT argument is sound: a seven-part in the digit-sum order comes from
some `q-1`, since `7` does not divide S; `q>=2*7^e+1` and `S/q>=3` give
`T_e<=L-1`, hence `e<=K-1`. Thus compatibility already stabilizes at K.
This cannot yield a later unrestricted incompatibility. The report correctly
identifies the missing condition as one concerning the bounded representative.

The cycle-gcd reduction supplies necessary conditions involving the varying
S, but no new global valuation theorem. Its search does not cover every
divisor of each gcd, and the prose states that limitation. Fixed-depth density
and qualitative `o(L)` cannot substitute for the moving logarithmic K.
No external estimate is newly applied, no effective cutoff is claimed, and
no ordinary proof is mislabeled as Lean verification. The narrower witness
filters are stated separately and do not enter either broad finite audit.

## Finite-audit assessment

The implementations are independent in both required mechanisms. A constructs
complete power cycles and evaluates F directly modulo `9S`. B constructs
successive linearized lifts and computes the repunit by concatenation modulo
S. The target's dependence on L modulo `T_(k-1)` justifies B's cache. Its
normalization `9*(n mod S)` is exact even when S is divisible by three.
Every recovered representative is separately checked with modular powers.

The reviewer independently verified the source bindings, the overall and
prefix digests, and all 100 block endpoints, lengths and hashes. The blocks
cover exactly the 4,999,998 odd lengths without gaps or overlaps. Both
reported rows and all four category counts reproduce. The main digest is
`037a7a03e48eceea6893641af0459885380975e2234aa11b6820a0d2a6c5f08f`.
Matching totals alone was not accepted as agreement.

A separate baby-step/giant-step discrete logarithm implementation recovered
the representatives at these 19 lengths:

```
5,7,13,23,41,43,151,293,295,2057,2059,14405,14407,
100001,9999999,705893,705895,4941257,4941259.
```

They agree with B's uncached lifts. Every actual sample's normalized residue
also agrees with direct modular powers modulo `9S`. These are supplementary
review probes, not the finite certificate's coverage argument.

The mandatory controls cover both position parities, exact digit statistics,
the retained nine, the shallow `(13,12)` positive, loss-of-nine `(151,8)`,
the `(23,15)` valuation regression, and strict period boundaries including
even equality. The modular arithmetic is arbitrary precision. A's only
fixed-width storage holds exponents safely below its sentinel; unsupported
intervals fail explicitly. Essential checks remain active under `-O`.

The earlier verifier schema-integration finding (reading B's `audit` fields
at the receipt root) has been repaired. The final full four-run verification
receipt records identical normal/optimized results, and the reviewer also
executed the repaired verifier under `python3 -O` without recomputation to
check receipt agreement, unsupported inputs, ancestry and preservation.

## Independent structured-search check

The final search's optimized lifting is valid: carrying `10^r` and `10^T`
at final precision and reducing them for each next digit preserves the same
linearized congruence. The declared generator ranges and domain filters match
the loops. No full-witness position, edge, ratio or prime-divisor filter is
used. The cycle-gcd family is explicitly a selected-divisor search.

[review_smooth.py](review_smooth.py) independently rechecks **every one of
the 2,731 smooth-family lengths**, including the 333-digit maximum. It tries
all seven possible next lift digits, rather than using the linearized
quotient/inverse formula. Exactly one digit must work at each step, and the
final exponent is checked directly.

For a separate digit-sum path, put `u=10^L mod(9S)`. Since `u=1 mod9`,
the integer quotient `(u-1)//9` equals `R_L mod S`: writing
`10^L=q*(9S)+u` proves this immediately. This is exact integer division of
a known divisible residue, not inversion of nine modulo S. The reviewer
uses this quotient to compute `n mod S` and the comparison residue.

All ordered results match the search receipt, with 1,538 outside positions,
1,193 actual full-sum failures and zero passes. The independent digest is
`e5f6a9e7c6d2b1276ac71c5b560709f6000d2193ce12557062e368b79d763d2a`.
Normal and optimized runs are byte-identical; [review_smooth.json](review_smooth.json)
records their deterministic result and source bindings. Reproduce with:

```sh
python3 research/a398769/five-seven/early-rejection/review_smooth.py > /tmp/early-review-smooth.json
python3 -O research/a398769/five-seven/early-rejection/review_smooth.py > /tmp/early-review-smooth-O.json
cmp /tmp/early-review-smooth.json /tmp/early-review-smooth-O.json
cmp /tmp/early-review-smooth.json research/a398769/five-seven/early-rejection/review_smooth.json
```

The 37 cycle-gcd lengths all lie below 14,732, within the main independently
audited interval; their generation source and declared scope were reviewed.
No independent complete cycle-gcd generator reimplementation is claimed.
No counterexample certificate is needed because neither search found one.

## Reviewed source identities and limits

| Source | SHA-256 |
|---|---|
| checker_a.py | `ca74c198c634347eca2a719bd2d31ab8fc3a43e038df95ebf3d734fdeea440e8` |
| checker_b.py | `8e697625fa29102dee4a4edc8d900e0aa810825c32f8f1b4a8298d0474e98125` |
| search.py | `19719f7470cc831c7098fe649d64fe42f894978f6cedde151b7e39947914d052` |
| search_scope.json | `123d9f103395f3027490ab630c979edb167d2673eb60dc3e96e8bb2c178bc03f` |
| PROOF.md | `5cfd56a04e4d52ae06246be5e11dca21dabbbf0bb36290b3d8b415beb86f0a97` |
| ROUTES.md | `2e6f997c3263a2c7cf7da3f87e7751ebef14e12833f1923a0eb46181c6c09746` |
| review_smooth.py | `8edade557aaa5d8c066e132f8723c3883d024333bec933711a56faf1fd20260b` |

The audited result is (E) for odd `5<=L<=9,999,999`, plus the stated sparse
search observations. The inherited consecutive exclusion stays **1 through
10,000,000 inclusive**; isolated giant lengths and infinite fixed-depth
families remain separate. No source or receipt from those large inherited
certificates was changed, and they were not rerun for this review.

The remaining mathematical obligation is the uniform full-sum rejection at
an actual `r_K` for E, or the weaker depth bound `v_7(F)<=L-3` on the remaining
full-witness domain. The investigation has not discharged either obligation.
The final repository head is checked separately after this review artifact
is committed, avoiding a self-referential commit hash in this file.
