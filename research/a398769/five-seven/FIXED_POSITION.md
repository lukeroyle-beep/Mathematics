# Independent audit of the fixed-position deduction

**Verdict: valid.** The stated bound follows from the cited corollary, and it combines with two exact modular certificates to exclude `i = 3` at every admissible length. This conclusion uses only the necessary 7-power condition, not the full product-times-sum condition. These arguments are ordinary mathematical proofs; they have not been checked by Lean.

## Setup

Replacing two sevens in the all-seven length-L number by fives gives

$$
n=7\sum_{j=0}^{L-1}10^j-2(1+10^i)
 =\frac{7(10^L-1)-18(1+10^i)}9=F/9.
$$

The actual digit product is `P=25*7^(L-2)` and digit sum `S=7L-4`. Since `F=9n`, the equivalence `PS | n` iff `9PS | F` gives exactly

$$
225\,7^{L-2}(7L-4)\mid F.
$$

The factor 9 cannot simply be dropped in claiming equivalence. Only `7^(L-2) | F` is used below. For `i=3`,

$$
F=7\cdot10^L-18025=7(10^L-2575),
$$

so the necessary condition becomes `v_7(10^L-2575) >= L-3`.

## Corollary and substitutions

Source: Y. Bugeaud and M. Laurent, *Minoration effective de la distance p-adique entre puissances de nombres algébriques*, supplied PDF, Corollary 1 and Theorem 3, p. 4; definitions and hypotheses on pp. 2–4. These are the page numbers printed in the supplied 29-page PDF, not inferred journal pagination: [Original paper](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).

For `Lambda=alpha_1^b_1-alpha_2^b_2`, that corollary gives

$$
v(\Lambda)\leq \frac{24p(p^f-1)D^4}{(p-1)(\log p)^4}
\left(\max\left\{\log b'+\log\log p+0.4,\frac{10\log p}{D},10\right\}\right)^2
\log A_1\log A_2,
$$

where `D=[Q(alpha_1,alpha_2):Q]/f`, the numbers are multiplicatively independent p-adic units, the exponents are positive integers,
`log A_j >= max(h(alpha_j), log p/D)`, and
`b'=b_1/(D log A_2)+b_2/(D log A_1)`.

Use

$$
p=7,\quad\alpha_1=10,\quad\alpha_2=2575=5^2\cdot103,
\quad b_1=L,\ b_2=1,
\quad e=f=D=1,\quad A_1=10,\ A_2=2575.
$$

Both numbers are rational and prime to 7, so the local field is `Q_7`, and its ramification and residual degrees are both 1. Their logarithmic heights are `log 10` and `log 2575`, each exceeding `log 7`. If `10^r 2575^s=1` for integers r,s, the 2-adic valuation gives r=0, and the 103-adic valuation then gives s=0; thus multiplicative independence holds. It also ensures `Lambda != 0`. (The auxiliary g in Theorem 3 is 6, because 10 has order 6 modulo 7; Corollary 1 already replaces g by `p^f-1=6`.)

Consequently the prefactor is

$$
C=\frac{168\log10\log2575}{(\log7)^4}<212.
$$

For a rigorous numerical check one may use the logarithm bounds
`log10 < 2.30258510`, `log2575 < 7.85360482`, and
`log7 > 1.94591014`. Substitution gives the rational upper bound

$$
C<\frac{18987773111811191100000000000000000}
        {89613025871743458570754642928401}<212.
$$

These logarithm bounds can, for example, be certified with the positive series
`log x = 2 sum_{k>=0} z^(2k+1)/(2k+1)`, `z=(x-1)/(x+1)`, and tail bound
`2*z^(2N+1)/((2N+1)*(1-z^2))` after terms `k=0,...,N-1` (range reduction makes it fast). The value of C to ordinary floating precision is 211.8863022334191; that decimal alone is not the rigorous certificate. The exact rational enclosures are reproduced by [log_bounds.py](log_bounds.py).

Since `log2575>7` and `log10>2`, for L>=5,
`b'=L/log2575+1/log10 < L/7+1/2 < L`.
Also `log log7+0.4<2`, `10 log7<20`, and `10<20`. All logarithms are natural. Hence

$$
\boxed{v_7(10^L-2575)\leq212\max\{\log L+2,20\}^2.}
$$

## Cutoff, including the switch of maximum

Let `B(x)=212 max(log x+2,20)^2` and `x_0=e^18`. The transition is at x_0, not at 100000. Because e>2, `x_0>2^18>100000`.

For `100000 <= x <= x_0`, `B(x)=212*400=84800<99997<=x-3`.
For `x>=x_0`, put `g(x)=x-3-212(log x+2)^2`. Then

$$
g'(x)=1-424\frac{\log x+2}{x}.
$$

The ratio `(log x+2)/x` is decreasing on this interval: its derivative is
`-(log x+1)/x^2<0`. Thus
`g'(x)>=1-8480/e^18>1-8480/100000>0`, and
`g(x_0)=e^18-84803>0`. Therefore `B(x)<x-3` throughout `x>=100000`, including the transition. This contradicts the necessary valuation bound at every such length.

## Orders and exact modular certificates

The powers of 10 modulo 7 from exponent 0 through 5 are `1,3,2,6,4,5`; hence its order is 6. Furthermore

$$
10^6-1=999999=7\cdot142857,\qquad142857\equiv1\pmod7.
$$

Thus `v_7(10^6-1)=1`. Here is an elementary order-lifting proof, without presupposing a primitive-root theorem. For `s>=1` and `7` not dividing c, the binomial expansion gives
`(1+7^s*c)^7 = 1+7^(s+1)*c (mod 7^(s+2))`; raising to a positive exponent prime to 7 leaves the valuation of the difference from 1 equal to s. Decomposing m into its 7-power and coprime parts therefore gives

$$
v_7(10^{6m}-1)=1+v_7(m).
$$

An exponent giving 1 modulo 7^k must first be divisible by 6, and the displayed identity then makes its quotient divisible by 7^(k-1). Hence

$$
\operatorname{ord}_{7^k}(10)=6\cdot7^{k-1}.
$$

This equals the number of units modulo 7^k, so each unit, including 2575, has exactly one exponent class modulo that period. Exact successive lifting gives:

| k | modulus 7^k | period | least exponent solving 10^L=2575 |
|---:|---:|---:|---:|
| 1 | 7 | 6 | 3 |
| 2 | 49 | 42 | 39 |
| 3 | 343 | 294 | 81 |
| 4 | 2401 | 2058 | 1551 |
| 5 | 16807 | 14406 | 1551 |
| 6 | 117649 | 100842 | 30363 |
| 7 | 823543 | 705894 | 30363 |
| 8 | 5764801 | 4941258 | 2853939 |

In particular `10^39 mod49 = 27 =2575 mod49`, and
`10^2853939 mod5764801 =2575`. Order checks by exact powers also yield:

- Modulo 49: the 42nd power is 1; powers 21,14,6 are 48,30,8.
- Modulo 5764801: the 4941258th power is 1; powers obtained by dividing that exponent by 2,3,7 are respectively 5764800,2387947,823544.

The latter tests separately certify minimality because 2,3,7 are the only prime divisors of the purported orders. They are reproducible finite certificates in addition to the general proof above.

For every remaining length `5<=L<100000`, the necessary valuation is at least 2. Thus `L=39 (mod42)`, whose least nonnegative representative is 39. This already excludes `5<=L<39`. Any surviving length is at least 39, so its required valuation `L-3` is at least 8. The second congruence forces `L=2853939 (mod4941258)`, whose least nonnegative representative exceeds 100000. This excludes all the other lengths below the cutoff. The lifts, order witnesses, residue table and finite coverage are reproduced by [certificates.py](certificates.py). Together with the analytic argument, no admissible length remains for i=3.

## Is 15 the next permitted position?

Write `i=3+6a`. Since `10^6=1+7 (mod49)` and `10^3=20 (mod49)`,
`10^i=20+42a (mod49)`, and

$$
F\equiv7(10^L+1-3a)\pmod{49}.
$$

For odd L its possible classes modulo 6 are 1,3,5. Using respectively `10^L=3,6,5 (mod7)` gives the necessary table

| L mod6 | a mod7 | i mod42 |
|---:|---:|---:|
| 1 | 6 | 39 |
| 3 | 0 | 3 |
| 5 | 2 | 15 |

Thus i=9 is impossible under these restrictions. After eliminating i=3, **i=15 is indeed the smallest position permitted by the modulo-49 restrictions**, requiring `L=5 (mod6)` and `L>15`. For example `(L,i)=(23,15)` passes this table (and the additional excluded length residue classes in the preserved notes). This is only compatibility with necessary congruences, not an existence result for candidates satisfying the growing 7-power condition or the full divisibility.
