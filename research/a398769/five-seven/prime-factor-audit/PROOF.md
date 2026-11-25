# Independent proof audit of the prime-factor obstruction

25 November 2026. The three proposed statements are **verified as written**
on their stated domains. The integer-divisibility and composite-multiplicity
steps below supply the requested justifications; no hypothesis or conclusion
has been corrected. The exact finite calculation supporting the line theorem
is documented separately in [COMPUTATION.md](COMPUTATION.md).

## Domain and the divisor actually used

Let L be odd, L >= 5, 3 <= i < L an integer of either parity, S = 7L-4,
and 5 not divide S. Set

```
F = 7*10^L - 18*10^i - 25.
```

The number with fives at decimal positions 0 and i and sevens elsewhere is
n = F/9. Its digit sum is S and its digit product is 25*7^(L-2), so its
full witness condition is exactly

```
225*S*7^(L-2) divides F.
```

The full digit-sum condition is **9S divides F**, not merely S divides F.
This audit uses only that necessary condition. In fact, the resultant
obstruction already follows from the weaker S divides F. The factor nine
is retained in the line theorem's final rejection and all reported controls.
No seven-adic depth condition and no odd-position restriction is assumed.

## Prime divisor and the common root

Let p be any prime divisor of S, c = S/p, b >= 1 and 0 <= a <= b integers.
For h = bi-aL, h_plus = max(h,0), h_minus = max(-h,0), put

```
P(X) = X^7 - 10^(c+4),
Q(X) = 10^h_minus*(7X-25)^b - 18^b*10^h_plus*X^a,
R = Res_X(P,Q).
```

Here c is a positive integer. Since S is odd and five-free, p is neither
2 nor 5. Fermat's little theorem and 7L=cp+4 give, for X0=10^L,

```
X0^7 = 10^(cp+4) = 10^(c+4)*(10^(p-1))^c
      = 10^(c+4) (mod p).
```

If 9S divides F then 7X0-25 = 18*10^i (mod p). Therefore the two terms
in Q(X0) agree, because their exponents of ten satisfy the exact equality

```
bi+h_minus = aL+h_plus.
```

All exponents in this modular calculation are nonnegative. There is no
cancellation of 18, 7X0-25, a leading coefficient, or any other nonunit.
In particular p=3 causes no difficulty. Thus X0 is a common root modulo
p, and the integral identity proved below implies **p divides R**.

## Nonvanishing of the resultant

Suppose x is a common algebraic root. The monic polynomial P makes x an
algebraic integer, x != 0; hence y=7x-25 is an algebraic integer. The Q
equation, over the number field containing x, gives

```
y^b = 18^b*10^h*x^a,
m := y^(7b) = 18^(7b)*10^e,
e = 7h+a(c+4).
```

Negative h or e is legitimate in this rational equality. Its nonzero
right side implies y != 0. Since m is both rational and an algebraic
integer, m is an ordinary nonzero integer. This standard fact follows
directly from a monic integer equation: a reduced rational root's
denominator must divide its numerator's highest power, hence is one.

Write

```
B = 7^7*10^(c+4) - 25^7
  = (7x)^7 - 25^7
  = y * sum_{j=0}^6 (7x)^(6-j)*25^j
  = y*z.
```

The displayed z is an algebraic integer. B is an odd integer, because
c+4 >= 5. The passage to ordinary integer divisibility is justified by

```
B^(7b)/m = z^(7b).
```

The left side is rational; the right side is an algebraic integer. Their
common value is therefore an ordinary integer. Thus **m divides B^(7b)
in Z**, so m is odd. The rational 2-adic valuation of the displayed formula
for m is 7b+e; oddness forces e=-7b. Consequently

```
m = (18/10)^(7b) = (9/5)^(7b),
```

which is not an integer, since b >= 1. This contradiction proves R != 0.

This argument does not assume P is irreducible or x has degree seven.
It applies when 7 divides c+4, when P has a rational root. It applies to
h=0 and h<0 as well as h>0, and to a=0 and a=b. On the actual-position
domain a=0 entails h=bi>0, a=b entails h=b(i-L)<0, and h=0 entails
0<a<b; no argument excludes any of these possible cases.

## All three bounds

Put t=10^((c+4)/7) and C=(7t+25)^b+18^b*t^a. Every one of P's seven
complex roots x_j has absolute value t. Monicity of P gives

```
|R| = product_{j=1}^7 |Q(x_j)|,
|Q(x_j)| <= 10^h_minus*(7t+25)^b + 18^b*10^h_plus*t^a
          <= 10^|h|*C.
```

Since R is a nonzero integer divisible by p,

```
p <= |R| <= 10^(7|h|)*C^7,
|bi-aL| >= log10(p)/7 - log10(C).
```

For the coarser bound, t>=1, 7t+25<=32t and t^a<=t^b imply

```
C <= (32t)^b+(18t)^b <= 2*32^b*t^b.
```

Hence exactly the claimed inequality follows:

```
p <= 2^7*32^(7b)*10^(7|h|+b(c+4)).
```

Finally, for **fixed a,b,c,h**, P,Q and R are fixed integers/polynomials,
and 7L=cp+4 gives

```
L <= (c*|R|+4)/7.
```

For a logarithmically widening exclusion about slope a/b as L grows,
**a,b,c must be fixed**, or one must supply uniform controls on C and
growth of p strong enough for the same conclusion. With fixed c,
p=(7L-4)/c grows with L, and fixed a,b,c makes log10(C) constant.
h is allowed to vary for this logarithmic inequality; fixing h further
gives the last, finite line bound. Merely choosing some prime divisor of
each S, allowing c or b to grow without control, yields no uniform
logarithmic exclusion or global cutoff.

## Composite sums, including repeated prime factors

Let D=gcd(S,10^(S-1)-1). Use c=1 in P and Q; h remains bi-aL.
The identity 7L=S+4 gives

```
(10^L)^7 = 10^(S+4) = 10^5*10^(S-1) = 10^5 (mod D).
```

Because D divides S, the same exponent-equality calculation proves
Q(10^L)=0 (mod D) if 9S divides F. To retain every repeated factor of
D, reduction modulo its separate primes is insufficient. Instead use
the following identity over Z.

For any monic P of degree seven, Z[X]/(P) is a free rank-seven Z-module
with basis 1,X,...,X^6. Multiplication by Q has an integer matrix M.
Over C, P has seven distinct roots (its nonzero constant is a power of
ten), and evaluation at them diagonalizes M. Thus det(M)=product Q(x_j)=R.
The adjugate identity M*adj(M)=R*I, applied to the vector for 1, gives
a polynomial U in Z[X] of degree at most six with

```
Q*U = R (mod P).
```

Division by the monic polynomial P uses only integers. Consequently
there is V in Z[X] such that **V*P+U*Q=R**. Evaluating at 10^L modulo D
now proves **D divides R**, with its full prime-power multiplicities.
This also supplies the prime-case identity used earlier. No field
division or squarefree replacement of D occurs. If the base-10 Fermat
test holds modulo S, then D=S, so **S divides R**.

## The exact line

Solving 12i-5L=-1 over the integers gives

```
L=12u+5, i=5u+2, S=84u+31.
```

L>=5 implies u>=0. The condition i>=3 then requires u>=1; for u>=1,
L-i=7u+3>0. Thus the actual-position range is exactly **integer u>=1**.
It contains both parities of i. With a=5,b=12,h=-1,c=1 the polynomials are

```
P(X)=X^7-10^5,
Q(X)=10*(7X-25)^12-18^12*X^5.
```

Suppose S passes the base-10 Fermat test and 9S divides F. The preceding
theorem forces S to divide the nonzero resultant of these fixed
polynomials. The exact computation proves the submitted factorization,
including multiplicities and deterministic primality of every factor.
S=31 (mod 84) is coprime to 2,3,7; the Fermat test implies gcd(S,10)=1
(as does five-freeness here). Therefore S can contain none of 2,3,5,7.
All fifteen remaining prime factors of the resultant occur to exponent
one. **Every eligible S is therefore a subset product of those fifteen
distinct primes.** This conclusion uses the divisibility with full
multiplicities, not just prime support.

The independently checked enumeration has 32,768 distinct products,
1,360 congruent to 31 modulo 84, and exactly one of those passing the
Fermat test: S=555700252411. It gives L=79385750345, i=33077395977,
which is an actual position. Direct modular arithmetic gives

```
10^L mod S = 79923024499,
10^i mod S = 166905216978,
F mod S   = 333668527919,
F mod 9S  = 889368780330.
```

In particular S does not divide F, contradicting the necessary condition.
Thus **for every integer u>=1 whose S=84u+31 passes the base-10 Fermat
test, its position i=5u+2 fails 9S divides F**. This covers prime S and
composite S passing the same test. It does not assert that every S on
the line passes that test. The composite control S=451=11*41, L=65,
i=27 passes it and gives F mod 9S=2241; it is rejected by the resultant
already, since 11 and 41 are absent from the factorization.

The finite computation exhausts a divisor set forced by a fixed nonzero
integer, so this is an all-length theorem for this conditional line,
not a length-bounded sample. It concerns **one position per eligible
length**, not every position of that length. Its implications for (E)
and the remaining open problems are stated in [README.md](README.md).
