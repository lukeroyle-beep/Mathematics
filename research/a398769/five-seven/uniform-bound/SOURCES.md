# Primary sources and exact normalisations

Read directly on 25 November 2026, including the rendered formula pages.
The PDF files were downloaded for inspection, not added to this repository.
The retained identifiers make the source versions unambiguous.

| Source | Relevant pages | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| [Y. Bugeaud and M. Laurent, *Minoration effective de la distance p-adique entre puissances de nombres algébriques*](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf) | printed 2–5, PDF 2–5 | 271382 | `554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d` |
| [Keith Conrad, *Hensel's Lemma*](https://kconrad.math.uconn.edu/blurbs/gradnumthy/hensel.pdf) | printed/PDF 1, 5–6 | 459665 | `3243fe15855aa549d42ed96f476bfd9f5241cdeb8d33f72beee33fd2e6bfdebf` |
| [J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio Mathematica 53 (1984), 225–244](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf) | printed 226–228, PDF 3–5 | 1228674 | `5b02e0e31c546f7f8c6c34071b2caa4d7137be24f16d11d483cdcc65377b2f6d` |

## Bugeaud–Laurent: Corollary 1 and Theorem 4

Write `v(p)=1`, `Lambda=alpha1^b1-alpha2^b2`, with algebraic p-adic
units `alpha1,alpha2` multiplicatively independent and positive integers
`b1,b2`. Let `f` be the residue degree of `Q_p(alpha1,alpha2)`,
`D=[Q(alpha1,alpha2):Q]/f`, and `g` the least positive integer with
both `alpha_j^g` principal units. Use absolute logarithmic height and
natural logarithms, with

```
log A_j >= max(h(alpha_j),log(p)/D),
b' = b1/(D*log A2)+b2/(D*log A1).
```

Corollary 1 (printed p. 4) states

```
v(Lambda) <= 24*p*(p^f-1)*D^4*log A1*log A2 / ((p-1)*(log p)^4)
             *max(log b'+log log p+0.4, 10*log p/D, 10)^2.
```

Theorem 4 (printed p. 5) replaces `24*(p^f-1)` by `c*g`,
and the last two maximum entries by `mu*log p/D,nu`, for each entry:

| `nu \ mu` | 4 | 6 | 8 | 10 | 15 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 5 | 53.8 | 36.1 | 28.1 | 24 | 18.6 |
| 10 | 51.7 | 34.8 | 27.3 | 23.2 | 18 |

The decimal constants are exact terminating decimals. These statements
have no additional unspecified large-exponent threshold. The paper's
separate asymptotic Theorem 2 is not substituted for them.

## Strong Hensel lifting

Conrad, Theorem 4.1, printed p. 6: for `Q in Z_p[X]`, `x in Z_p`,
and finite `d=v_p(Q'(x))`, the hypothesis `v_p(Q(x))>2d` gives a
unique root `alpha` in the ball `v_p(alpha-x)>d`. Moreover,

```
v_p(alpha-x)=v_p(Q(x))-d,
v_p(Q'(alpha))=d.
```

The uniqueness is within that ball. It does not imply a unique root
modulo every power of p. The simple-root case is Theorem 2.1, p. 1.
The torsion description used in the dependent case is Theorem 3.1,
printed pp. 4–5: the roots of unity in `Q_p`, for odd p, have order
dividing `p-1`. Its application here can also be obtained by the
binomial argument given in [ANALYTIC.md](ANALYTIC.md).

## Evertse's finite-tuple conclusion

Corollary 1, printed p. 227, equations (9)–(12), fixes `n>=1`, a finite
prime set `S0`, `c>0`, and `0<=d<1`. It gives finiteness of primitive
integer `(n+1)`-tuples with zero sum, no nonempty proper zero subsum, and

```
product_j (|x_j| * product_(p in S0) |x_j|_p)
    <= c*(max_j |x_j|)^d.
```

Here `|u|_p=p^(-v_p(u))`. For `K=Q`, the height on p. 226 is the
maximum absolute coordinate of a primitive tuple. Common gcd one suffices;
pairwise coprimality is not required. The integer/projective passage is
explained on p. 228. The conclusion supplies no numerical largest
tuple or length. The inherited application with `c=1,d=1/2` is checked
in [FINITE_PAIRS.md](../FINITE_PAIRS.md); the additional asymptotic
deduction in [ANALYTIC.md](ANALYTIC.md) remains ineffective.
