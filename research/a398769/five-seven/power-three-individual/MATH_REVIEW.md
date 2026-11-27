# Independent mathematical review

**Verdict: PASS, with no unresolved mathematical findings.** This is a
review of implementation commit
`561cd96effccc9362255ac6c766445fafaec3145`, based on
`a9edeb0a96bd56d55f3c96767f5154e69cb8ceda` (PR #29's merge).
Reviewer context: `/root/final_math_review`. This reviewer authored none
of the implementation documents or arithmetic programs and made no
implementation edits. The review is an ordinary mathematical audit,
not a Lean verification.

## Common-factor theorem

The exact predicate retains `225*S*7^(L-2)|F`, including `9S|F` at the
same actual position and the inclusive threshold `t=L-2`. Reduction
modulo 49 gives precisely `s=39 mod42`. It follows that `7` divides
neither s nor p, so the polynomial derivative is a unit. Simple Hensel
lifting and factorization give the equality `t=v7(10^g-alpha)`.
Positivity of the actual F proves nonvanishing; the sixth-power cofactor
is a unit, so taking sixth powers preserves this valuation exactly.

At a place above two, the odd leading and constant coefficients force
alpha to be a unit. A multiplicative dependence with ten therefore
forces alpha to be torsion. At a complex embedding, triangle equality
then requires `alpha^q=1` and `alpha^p=-1`, contradicting odd q. The
argument does not assume that alpha is rational or real.

The minimal-polynomial/Mahler-measure argument correctly keeps the
degree factor: for `D=[Q(alpha^6):Q]`, one has `D<=q` and
`D*h(alpha^6)<=6*log50<25`. The local field is Q_7, hence local residue
degree one. I independently reopened the primary
[Bugeaud--Laurent text](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf),
checked its definitions on printed pages 2--4, and inspected the rendered
Corollary 2 on printed page 5. The height choices `15,25/D`, principal
units, positive exponents `(g,1)`, independence and nonvanishing meet
all its hypotheses. It has no omitted large-exponent condition.

All three entries in the maximum are bounded before replacing D by q.
The resulting strict constant is exactly `208*15*25*4=312000`.
The comparison at a=100 and the ratio induction with
`3*20^8>21^8` are valid exact integer arguments. Together with all
twelve smaller admissible exponents, they exclude every actual position
with `q^4<=L` at every admissible exponent. There is no finite gap in
this theorem. Its scope is independent of both neighbouring lengths.
The comparison with earlier rational centres correctly concerns exact
ratios; it does not discard their separate nonzero-offset results.

## Fixed-position index theorem and the remaining gap

The length difference loses exactly one factor of seven on division by
seven. Consequently
`v7(F(L_u,s)-F(L_v,s))=2+v7(u-v)` for distinct indices. For fixed
`s=39 mod42`, dividing F by 49 gives a well-defined permutation of the
classes modulo every `7^j`. The explicit digit slope is 2 modulo seven,
and the lift digit is `-4*z_m mod7`. The depth-three formula
`s=123+126u mod294` agrees with direct modular arithmetic.

The same-position ternary relation `7q*kappa=4p mod3^(a-2)` is correct.
The displayed three-adic logarithm estimate with exponents `(4p,7q)`
gives a lower size constraint on q. It supplies no upper bound on q
or on a, and does not force a seven-adic index mismatch. The manuscript
correctly identifies the missing implication: for each remaining actual
candidate, some mismatch must occur at a depth `m<=L-2`. Uniqueness of
the fixed-s index class and a large residue modulus do not imply this.
A first failure at depth L-1 would leave the qualifying valuation L-2.

The actual a=1231 control survives through depth four and first misses
at five; it is a valid positive control for the distinction. The
pair theorem and ineffective qualitative finiteness cannot close the
remaining individual gap. No universal cutoff or full witness is proved.

## Computational checks supporting the reviewed claims

I independently reran `math_checks.py --check` and `index_lift.py` in
both ordinary and optimized Python. The retained outputs match exactly.
At the immutable implementation commit I also ran both aggregate
commands below successfully:

```sh
pt=research/a398769/five-seven/power-three-individual
python3 "$pt/verify.py" --run
python3 -O "$pt/verify.py" --run
```

They reproduced all four source-bound arithmetic receipts and rejected
the nine corrupted-receipt controls. I independently read back the exact
ternary relations and every retained seven-power residue for a=97,
1231,1573,1579. The new a=1573 representative misses the actual range;
a=1579 has `g=1`, `q=L`, `n mod25S=0`, and `n mod49=14`, so it is
excluded directly. The original-block method is independent of the
explicitly reused Newton/logarithm method. The factor-nine control
detects the incorrect weakened sum test.

The combined coverage is correctly limited to 259 named family lengths,
through a=1579, with a=1585 next. Consecutive whole-length coverage
remains 1--1,000,002,000,000 inclusive; the unrestricted {5,7} subclass
and wider digit-1 assertion remain open. Historical large searches and
Lean builds were not performed by this review. The base and source
manifest verifies 1,067 inherited files, with only the root README
addition changed.
