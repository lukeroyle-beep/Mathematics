# Independent mathematical and computational review

Reviewed 25 November 2026 by the separate `independent_review` workstream,
starting from the merged PR #9 commit
`4dc97536a57d1b216f79e4856c333ea2c8e6d1ae`. The reviewer did not write
the primary proof notes or Route B checker. The reviewed file hashes and
executed-command provenance are in [review.json](review.json).

**Accepted outcome: new partial results, with the complete `{5,7}`
subclass still unresolved.** No mathematical or implementation finding
requiring correction remains in the reviewed content. In particular,
the all-length conclusion applies to the strip `|L-2i|<=47`, not to the
whole subclass. No global maximum length or full witness is established.

## Published hypotheses and qualitative conclusion

The reviewer independently opened Evertse's original paper and visually
inspected printed pp. 226--227. Corollary 1 requires a common gcd of one,
not pairwise coprimality. The tuple `(U,-V,-1,-W)` is integral, primitive,
nonzero, and has zero sum; `U=V+1+W` with `V,W>0` verifies every proper
subsum and the exact height `h=U`. Only `W` contributes outside primes.
The inequalities `U<49^L` and `U<10^L` justify respectively `c=1,d=3/4`
at the half-length threshold and the stated general epsilon choice.
The pair-to-tuple map is injective.

Thus `v_7(F)=o(L)` holds uniformly for all `L>=5,3<=i<L`, without a
digit-sum assumption. This is a checked corollary of the existing
published method. It supplies no computable exceptional-height bound.
The effectivity discussion correctly locates the unspecified exceptional
subspaces in Evertse's Theorem 4 and the constants depending on their
coefficient tuples in the proof of Theorem 2.

The conditional cutoff calculation also passes: for an integer `B`
rounded upward as stated, `L>B` gives the necessary strict inequality.
The endpoint `B` remains a finite-verification obligation. This conditional
calculation is not used as though the global valuation constants existed.

## Effective strip proof

The reviewer independently opened the Bugeaud--Laurent primary source,
checked its definitions on printed pp. 2--3 and visually inspected the
Corollary 1 formula on printed p. 4. The source hashes match those recorded
in [ROUTE_A.md](ROUTE_A.md).

For every odd offset, the primitive quadratic factorization and chosen
local root have been checked. The argument treats degree one and degree
two separately; it does not assume unproved irreducibility at arbitrary
positive offsets.
The simple root is `6 mod 7`; the other root has valuation `-1`, exactly
cancelling the leading coefficient's valuation. For a quadratic root,
multiplicative independence follows by taking the norm and then its
7-adic valuation. A rational dependent root would have to equal
`+10^k` or `-10^k`. Its real size forces `k<0`; comparison of the three
5-adic valuations after clearing denominators gives the stated
contradiction. Negative odd offsets are always irreducible by their odd
2-adic discriminant valuation.

The real-root locations give the asserted absolute logarithmic height
in degree two. In degree one, the rational-root denominator bound gives
the larger permitted height; the half-height formula is not reused.
The application uses local `e=f=1` and global parameter `D` equal to one
or two. It retains the factor `D^4` and the maximum term `10 log(7)/D`.
With the degree-dependent choice of `log A_2`, the coefficient is bounded
by `63*D^3*(|d|+2)<=504*(|d|+2)`. This proves the variable-offset bound
on the whole stated domain, with all its offset dependence displayed.
On `|d|<=47` the coefficient is at most `24696`.

The inherited real-variable comparison
`24948*max(log L+2,20)^2<L-3` for `L>=10,000,000` is stronger than
needed because `24696<24948`. It excludes the necessary seven-power
valuation in the strip above that boundary. The exact inherited
certificate closes the remaining finite lengths. Although the finite
seven-power search uses `i=3 mod 6`, any pair with `v_7(F)>=1` necessarily
has that residue: modulo 7, `4*10^i+4=0`, so `10^i=-1`, which is the
third power in the order-six cycle. There is consequently no uncovered
position class when the strip estimate is stated on its broader domain.

The positive-offset modular nonsquare table was reproduced exactly. The
reviewer also certified all 48 discriminants by independently enumerating
square residues modulo small primes, rather than using integer square
roots. The largest prime in these separate certificates is 43. The
negative-offset odd 2-adic discriminant valuation is also valid. These
48 finite certificates are additional controls; the general proof no
longer requires arbitrary positive-offset discriminants to be nonsquares.

The auxiliary literature checks correctly distinguish an applicable
fixed-recurrence theorem with inadequate/uncontrolled uniform saving
from inapplicable unsigned-digit and fixed-S-unit hypotheses. In
particular the unrestricted cofactor is never declared to be an S-unit.

## Quotient refinements and factor nine

The adjustable split has a nonempty exact integer domain containing the
merged half-length split. Its low branch uses the strict remainder bound;
its high branch uses the full `A=9*7^(L-2)*(7L-4)` and the inverse modulo
`10^t/25`. The `t=L-1` endpoint correctly has an empty high-position
branch on the residual domain. Inverse lifting alone does not exclude a
small unchanged residue.

The digit-sum exponent congruence follows from the integer repunit
identity, inverting only 2 modulo the odd digit sum. Thus it preserves
`S|n` exactly, including when `3|S`. Its combination with the seven-power
class uses the generalized CRT with the correct gcd. Stabilization of
that gcd for a fixed length does not establish existence or nonexistence
of a position below `L`. The full equality `Hq=F` remains indispensable.

The Route B checker has meaningful positive CRT controls and explicitly
synthetic quotient controls. Its enlarged high-branch control has a
different quotient from `floor(X)`. The actual `(313,51)` control verifies
that `S|F` can hold while `S` does not divide `n`; it protects the factor
nine. None of these controls is reported as a full witness.

## Executed verification and provenance

The reviewer wrote [independent_checks.py](independent_checks.py), which
imports no primary implementation. Its normal and optimized outputs
match [independent.json](independent.json). It checks:

- 48 separate quadratic nonresidue certificates;
- 11,352 direct decimal pairs for all odd offsets `-47..47` and
  `max(3,2-d)<=i<=250`, with 90,816 comparisons to roots modulo
  `7^1` through `7^8`;
- the `d=1` specialization for every `3<=i<=1000`, with 11,976
  comparisons modulo `7^1` through `7^12`;
- exact rational logarithm enclosures, the analytic coefficient and
  cutoff inequalities, and the inherited `(23,15)` regression.

The valuation controls include zero and positive values through five.
They check proof identities and constants; they are not new exhaustive
coverage beyond the inherited interval. Both scripts retain their checks
under Python `-O`.

The reviewer also reran the Route B checker and the inherited global
primary and independent checkers under `-O`; their outputs matched the
corresponding normal/recorded receipts. The inherited `certificates.py`
and `log_bounds.py` passed. The primary workstream reran both unchanged
ten-million search programs during this investigation. The reviewer
inspected those current receipts and independently compared them with
the merged records: the fixed-modulus receipt matches exactly, and the
lifting receipt differs only in elapsed time. The relevant source files
are unchanged from the starting commit. The review does not attribute
those large-program executions to the reviewer.

Reproduce the new independent checks from the repository root:

```sh
python3 research/a398769/five-seven/effective/independent_checks.py > /tmp/a398769-effective-independent.json
cmp /tmp/a398769-effective-independent.json research/a398769/five-seven/effective/independent.json
python3 -O research/a398769/five-seven/effective/independent_checks.py > /tmp/a398769-effective-independent-optimized.json
cmp /tmp/a398769-effective-independent-optimized.json research/a398769/five-seven/effective/independent.json
python3 -O research/a398769/five-seven/effective/route_b_checks.py > /tmp/a398769-effective-route-b.json
cmp /tmp/a398769-effective-route-b.json research/a398769/five-seven/effective/route_b_checks.json
git diff --check
```

## Exact remaining gap

Any full witness still has to lie above the unchanged complete interval,
obey all inherited restrictions and now satisfy `|L-2i|>=49` and
`L-2<=504*(|L-2i|+2)*max(log L+2,20)^2`. The
explicit estimates retain a factor growing with the position, gap or
offset outside the excluded regions. Taking their minimum does not give
the required global sublinear valuation estimate. Neither exact quotient
function has been uniformly rejected over the remaining lengths.

The next missing statement is a uniform effective valuation bound or
other global reduction, or uniform rejection of the two exact quotient
candidates with their full equality. No finite range left by a global
cutoff has been silently treated as checked, because no such cutoff was
obtained. No Lean source changed and no fresh Lean build is claimed.
The ordinary proofs and exact finite computations have the scope stated
above. Branch publication, draft PR preparation and the owner's eventual
merge decision are separate from this mathematical review.
