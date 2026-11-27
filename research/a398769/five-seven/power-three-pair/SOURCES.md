# Primary source readback

On 27 November 2026 the primary PDF was reopened through the web tool,
including the rendered printed page 5, and downloaded afresh for hashing:

- Y. Bugeaud and M. Laurent, [*Minoration effective de la distance p-adique
  entre puissances de nombres algebriques*](https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf).
- 29 PDF pages; definitions on printed pp.2--4; **Corollary 2 on printed p.5**
  (zero-based PDF page 4).
- Downloaded bytes: **271382**.
- SHA-256: `554bb384df62538fa11fcf6ab74976e772156c9d3ca4022e2128d48e3632128d`.
- The byte hash agrees with the inherited primary-source record, but this
  audit made its own live download. The PDF itself is not vendored.

The normalization is `v(p)=1`. For two principal units and positive integer
exponents, use the multiplicative-independence hypothesis of Theorem 3,
the height and b-prime definitions on printed p.4, and Corollary 2's
explicit bound on p.5. There is no unmentioned asymptotic threshold.
The proof in [LOGARITHMS.md](LOGARITHMS.md) verifies these hypotheses and
specializes the bound; all subsequent numerical simplifications are
independently checked with exact integer or rational arithmetic.

The strong Hensel step is proved directly in that note using the rescaled
polynomial and simple-root lifting, followed by Taylor expansion for the
exact valuation. It does not depend on an uninspected external lemma.

Reproduce source acquisition and byte verification separately from the
offline arithmetic checks:

```sh
curl --fail --location --output /tmp/logpadicdef.pdf \
  https://irma.math.unistra.fr/~bugeaud/travaux/logpadicdef.pdf
shasum -a 256 /tmp/logpadicdef.pdf
wc -c /tmp/logpadicdef.pdf
```

No network access is required by any arithmetic verifier.
