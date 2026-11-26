# A398769 on digits 5 and 7

26 November 2026

**Every length through one trillion is excluded.** The largest seven-adic valuation attained in the reduced family is exactly 27. The digit-sum condition alone excludes all positions for a set of lengths of natural density one. Explicit intervals of position ratios can also be excluded at every length. The complete subclass remains open.

## The finite theorem

Let \(L\) be the decimal length, and number positions from zero at the units digit. The elementary reduction leaves an odd length \(L\ge5\), with fives at positions \(0,i\), where \(3\le i<L\), and sevens everywhere else. Define
\[
F(L,i)=7\cdot10^L-18\cdot10^i-25,\qquad S=7L-4.
\]
The number is \(F/9\). Its digit product times its digit sum divides it precisely when \(225S7^{L-2}\mid F\). In particular, the exponent \(v_7(F)\) of seven in \(F\) must reach \(L-2\). [Audited reduction and exact divisor](https://github.com/lukeroyle-beep/Mathematics/blob/37bd10a930d6dc7c9a7bcfd8db7588451dc26da2/research/a398769/five-seven/settlement/README.md).

For every odd \(5\le L\le10^{12}\) and every \(3\le i<L\), exhaustive modular enumeration gives \(v_7(F)\le27\). Two independent implementations produced the same 74,601 pairs for which \(7^{22}\mid F\). One enumerated points of an integer lattice. The other used recursive lifting and sums of integer floors. Their retained lists matched pair for pair. I checked the complete list again using the decimal formula
\[
n=7(10^L-1)/9-2(10^i+1).
\]

| Exact exponent of seven | 22 | 23 | 24 | 25 | 26 | 27 | 28 or more |
|---|---:|---:|---:|---:|---:|---:|---:|
| Number of pairs | 63,974 | 9,161 | 1,272 | 162 | 29 | 3 | 0 |

| Length \(L\) attaining 27 | Position \(i\) | \((F/7^{27})\bmod 7\) |
|---:|---:|---:|
| 206,013,221,471 | 70,699,701,213 | 5 |
| 636,442,113,223 | 552,133,548,915 | 4 |
| 778,826,473,305 | 776,307,582,249 | 1 |

For \(L\ge30\), the required \(L-2\) exceeds 27. Directly constructing all 182 reduced decimal words at the smaller odd lengths through 29 excluded them as well. The elementary reduction then establishes the result for the original digit subclass at every length from 1 through \(10^{12}\). One trillion was the chosen search limit.

A separate test concerns the project's stronger early-rejection statement (E). Write \(K(L)\) for the first \(k\) with \(6\cdot7^{k-1}>L\). For every odd \(5\le L\le1,694,851,493\) with \(5\nmid S\), the condition \(9S\mid F\) implies \(v_7(F)<K(L)\). Two independent searches covered the interval above the prior certificate, finding zero full-sum passes among 385,825,287 eligible positions that reached \(K(L)\). The larger trillion-length calculation tests the valuation needed to be a full witness. [Earlier (E) certificate and definition](https://github.com/lukeroyle-beep/Mathematics/blob/37bd10a930d6dc7c9a7bcfd8db7588451dc26da2/research/a398769/five-seven/early-rejection/README.md).

## Three results valid at arbitrarily large lengths

**Almost every length fails the digit-sum condition alone.** The set of lengths \(L\) for which \(S\mid F(L,i)\) for *any* nonnegative exponent \(i\) has natural density zero. In other words, the proportion of such lengths up to \(X\) tends to zero. For primes \(p\equiv1\pmod{40}\), the number \(18\cdot10^i\) is always a nonzero square modulo \(p\). If \(p\mid S\) and \(7\cdot10^L-25\) is a quadratic nonresidue, the whole length is excluded. The multiplicative order theorem of Erdős and Murty and classical bounds for Jacobi sums show that successive finite sets of primes exclude at least one eighteenth of each remaining arithmetic progression. This drives the upper density to zero. The project already gives infinitely many exceptional lengths passing the digit-sum condition at an actual position. [Order theorem, Lemma 2.3(i)](https://www.cs.uleth.ca/~akbary/Akbary-Yazdani.pdf) · [Jacobi sums](https://kconrad.math.uconn.edu/blurbs/gradnumthy/Gauss-Jacobi-sums.pdf) · [Known exceptional lengths](https://github.com/lukeroyle-beep/Mathematics/blob/37bd10a930d6dc7c9a7bcfd8db7588451dc26da2/research/a398769/five-seven/fixed-depth/README.md).

**Closed intervals around rational position ratios are excluded at every length.** For every reduced fraction \(0<a/b<1\) with \(b\le55\), a full witness must satisfy
\[
|bi-aL|>\frac{L}{100000b^2}.
\]
The result includes equality at the centre and both boundaries in the excluded region. For \(L>10^{12}\), the contrary assumption makes \(L/(51000b^3)\) an allowed height parameter in the merged estimate. The resulting bound is \(v_7(F)<169L/170-1<L-2\). The finite theorem covers every earlier length. [Merged estimate, equation (13)](https://github.com/lukeroyle-beep/Mathematics/blob/37bd10a930d6dc7c9a7bcfd8db7588451dc26da2/research/a398769/five-seven/uniform-bound/ANALYTIC.md).

**Two possible witness lengths must be separated.** If \(m<M\) both reach the required valuation at some position and \(m\ge105\), then \(M>5m/4\). The underlying elementary inequality for any two distinct lengths is \(25\cdot7^{3v}<10^{2M}\), where \(v\) is the smaller of the two attained valuations. This leaves room for an isolated witness.

## What remains open

The project already proves that only finitely many pairs can attain \(v_7(F)\ge L-2\), without specifying their largest possible length. A single exceptional pair above one trillion could still satisfy \(225S7^{L-2}\mid F\). No such pair or proof of its impossibility emerged. The all-length early-rejection implication, the complete \(\{5,7\}\) subclass, and the wider digit-1 conjecture remain open. [Qualitative valuation theorem](https://github.com/lukeroyle-beep/Mathematics/blob/37bd10a930d6dc7c9a7bcfd8db7588451dc26da2/research/a398769/five-seven/effective/QUALITATIVE.md) · [Starting merged investigation](https://github.com/lukeroyle-beep/Mathematics/pull/20).

The accompanying evidence archive contains the full proofs, both complete enumerations, the sorted candidate list and reproduction commands. The arguments and computations are available for independent audit. No new Lean formalization is claimed.
