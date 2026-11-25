# A398769 prime-factor obstruction: independent audit

25 November 2026. **Mathematical verdict: all three proposed statements are
verified as written. Computational verdict: the exact factorization, all
multiplicities, divisor counts and reported residues are verified.**

| Claim | Verdict | What is established |
| --- | --- | --- |
| General prime-factor bound | Verified as written | p divides a nonzero resultant; all three bounds hold with the stated fixed-parameter qualifications. |
| Composite extension | Verified as written | D divides R with every repeated prime factor; the Fermat hypothesis gives S divides R. |
| Exact line exclusion | Verified as written | Every actual position on 12i-5L=-1 fails 9S divides F when S passes the base-10 Fermat test. |

The proof has no first unsupported step on the stated domain. In particular,
the proposed passage from algebraic-integer divisibility to ordinary integer
divisibility is valid: both the divisor and quotient are rational algebraic
integers. [PROOF.md](PROOF.md) expands that justification and the integral
resultant identity needed for composite multiplicities. It includes both
position parities, negative/zero h, a=0, a=b and reducible P.

## Starting point and preservation

The audit freshly cloned `https://github.com/lukeroyle-beep/Mathematics.git`
and branched from the exact current main commit
**43da3bfcd17f53dc26925b00175042c8d16db78d**, the merge of
[pull request #16](https://github.com/lukeroyle-beep/Mathematics/pull/16).
The audited research commit **a75b08e1e21561fc1877e312f5fca0cf25174a18**
is an ancestor and the second parent of that merge. Main had not advanced
beyond the supplied merge, so there was no later work to reconcile.

The separate branch is `audit/a398769-prime-factor-obstruction` in the
new `a398769-prime-factor-audit` checkout. Existing checkouts were not
modified. No applicable AGENTS.md was found. This change only adds this
audit directory and a navigation link from the inherited early-rejection
report; it preserves the earlier proof, programs, receipts and Lean sources.
The exact baseline readback and final inherited-file comparison are in
[verification.json](verification.json).

The supplied proposal is audited as stated in the task, not treated as an
already established repository theorem. Definitions and coverage were read
from [the PR #16 report](../early-rejection/README.md). That report's full
witness divisor is 225*S*7^(L-2), and its full digit-sum divisor is 9S.

## Exact finite evidence for the infinite conditional line

[COMPUTATION.md](COMPUTATION.md) gives the signed resultant, complete
factorization and deterministic recursive Lucas certificates for every
prime, including the two factors beyond 64 bits. A standard-library integer
Sylvester determinant independently agrees with SymPy's resultant. Two
complete divisor enumerations agree entry for entry:

| Filter | Count |
| --- | ---: |
| Distinct subset products | 32,768 |
| Products congruent to 31 modulo 84 | 1,360 |
| Of those, base-10 Fermat survivors | 1 |

The sole survivor is S=555700252411, L=79385750345, i=33077395977.
All submitted residues reproduce; independently, **F mod 9S=889368780330**,
so it fails even S divides F. The composite control S=451, L=65, i=27
passes the Fermat test and gives **F mod 9S=2241**, as claimed.

The [standalone checker](checker.py) verifies the retained
[certificates](primality_certificates.json) without SymPy. It and the
symbolic cross-check pass normally and under `python3 -O`; essential
checks use exceptions, never removable Python assertions. Stable receipts
are [results.json](results.json) and [results-sympy.json](results-sympy.json).
[REVIEW.md](REVIEW.md) records the fresh independent proof, computation
and scope review. Exact commands and software versions are in the
computation report.

## What this adds, and what remains open

The new general obstruction gives a fixed-parameter effective bound when
a prime divisor has controlled cofactor c. The new composite extension
preserves multiplicities. The new line theorem excludes **one position**
i=5u+2 at each length L=12u+5 with integer u>=1 and S=84u+31 passing the
base-10 Fermat test. It includes both prime S and passing composite S.
It is valid at every such length, including lengths beyond prior finite
coverage; it does not exclude the other positions at those lengths.

The unchanged PR #16 certificates establish broad (E) for **every odd L
from 5 through 9,999,999 inclusive**, and consecutive full-witness exclusion
for **every length from 1 through 10,000,000 inclusive**. This audit adds
no consecutive length interval and does not freshly rerun those large
computations. It checks their retained integrity and preserves their scope.

For precision, with K(L)=min{k>=1:6*7^(k-1)>L}, broad (E) is

```
odd L>=5, 5 does not divide S, 3<=i<L:
9S divides F(L,i)  ==>  v_7(F(L,i)) < K(L).
```

Its equivalent remaining obligation is uniform rejection of 9S divides F
at every actual representative r_K(L) with 3<=r_K<L. This audit rejects
that representative when it lies on this particular line and S passes the
Fermat test; it does not show that every representative does. It also does
not provide uniformly fixed a,b,c for arbitrary lengths and positions.

Consequently **broad all-length (E), the all-length {5,7} subclass, and the
wider digit-1 conjecture remain open**. Subclass closure would follow from
(E) together with the inherited complementary cases, or from the weaker
full-witness-domain bound v_7(F)<=L-3 with an appropriate global argument,
or from an effective global cutoff with its finite obligation discharged.
None is supplied here. Other digit sets are outside this audit. These are
ordinary mathematical proofs and exact Python computations; no new Lean
theorem or Lean build is claimed.

Delivered for owner review as a draft pull request. Merging remains with
the owner.
