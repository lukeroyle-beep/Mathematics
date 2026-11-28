# Individual certificates

The two first previously unchecked members are excluded: a=1573 is a class
miss, and a=1579 is an actual sum-compatible position with exact valuation
one. No full witness was found. Both methods recover the representatives
from their definitions, without using the pilot values to select a branch.

`root_log.py` explicitly reuses the inherited Newton seventh-root and
modular-logarithm implementation in `../power-three/individuals.py`, at
precisions 1580 and 1586. Its receipt binds that source. The independent
`independent_decimal.py` imports no project code. It constructs the all-seven
word by binary decimal-block concatenation, solves
`10^s=(all_sevens-2)/2 mod3^a` by checking all three children at each ternary
digit, and independently constructs each actual word as
`7^(L-s-1) | 5 | 7^(s-1) | 5`, where the powers in this display mean
repeated decimal digits. There is no expansion of an astronomical word.

Both enforce the unique odd representative in `[0,2d)`, the actual range
`3<=s<L`, and the **same-position** condition `9S|F`. For actual positions
`n mod25S=0` is checked. A first nonzero residue modulo `7^m` disproves
`PS|n` only with `m<=L-2`. Equality `t=L-2` would already qualify as a witness.
The computation never treats its valuation resource guard as an exclusion.

## Exact new representatives

### a=1573

Exact `L=(3^1573+4)/7`:

```text
464125717923892807756853161310606300163299476834836958807704915681166843480876930485217018846877757099316453380660941153068093999371326871640792285458849695311038962438636029524127485631381623373847919982226747387114674495937599398933414387443578764852015658031975678893616126187618938706457995468725170325454253070213862977747280820499749944959642255758379305493722580798067242271853328823735660213932019071669132677111106238540829287907506914455937908670459126877433634133175797169269287008032995676718485713834879198152294049153248867179507198005066902699642540121551898071231187272785074413630145700436168233784851271659823915291316619265009597281782483685605473934905970935928847969735225608309659622904749490253386497153614493892324168033772561
```

Exact odd representative `s_a`:

```text
622999831843714708523928990354154511559702139459551976763245311248958405422829349948803081411872587671419978644742769834884748307256871907610896515555790280470668431112322955603106101179839102538182775015163661096765249883378771330747149128508121896719792309884301080478452356649250389963785211151425337944827938941868359705597002452453910116936102375763672086270843242491837325180327678563765587474953007847736219605736375869551963409321421549703361933924249949529777578074846726783204419868298954141728348907193330737121887410232503255252340448792228102371475384580434297672899094527663041563010662561971461446789913782997684951692377895474392723942704155672315055464745548230593053504212464509922292223913728847113806760816358021475231231400735727
```

The range test fails: `s_a>=L`. More precisely `134L<100s_a<135L`;
`s_a<2d` and `s_a mod126=123`. There is no actual word at this position,
so no original-word residue or witness valuation is credited to this row.
The unique joint class cannot hide a second actual representative because
`L<2d`. Thus the entire specified length is excluded.

### a=1579

Exact `L=(3^1579+4)/7`:

```text
338347648366517856854745954595431992819045318612596142970816883531570628897559282323723206739373884925401694514501826100586640525541697289426137576099501427881747403617765665523088937025277203439535133667043298845206597707538509961822459088446368919577119414705310269913446155990774206317007878696700649167256150488185906110777767718144317709875579204447858513704923761401791019616181076712503296295956441903246797721613996447896264550884572540638378735420764703493649119283085156136397310228856053848327776085385626935453022361832718424173860747345693772068039411748611333693927535521860319247536376215617966642429156577040011634247369815444191996418419430606806390498546452812292130169936979468457741865097562378394718756424984966047504318496620196553
```

Exact odd representative `s_a`:

```text
148627534325351754515431548208291941341411868641235337729886923978465496270991361626901341313694001796009000112255509559757710279217891107641952436434100082007435315342099590148297093185853756778420797258236359772321111450254591024101735959346627128021751452148969878683220483707589956399689834877289340763950795306887844664831674330767374170342955355045380183949269044008097724582982444759021692789028830200702226306640055809715349747442048626492874672809948438187111392018320906490761299276874376464384178793207871475036797878640212975344717413590408007074368596512230872904832177702626903437909512680367727331553736930412297089050145566483316342079355562842082060632484760724465681239408667741826447083083539399627915945297580091073805271482170429997
```

The range test is `3<=s_a<L`; the exact certificate gives
`43L<100s_a<44L`. Here **g=1, p=s_a, q=L** (the exact q is the L above),
so `q^4>L`. The original word has `n modS=n mod25S=0` and `F mod9S=0`.
Its residues modulo `[7,49]` are `[0,14]`; equivalently `F mod49=28`.
Thus `t=1`, with first failure at `m=2<=L-2`, and **PS does not divide n**.
This is a direct exclusion in the region left by the common-factor theorem.

## Retained controls and finite range

| a | Actual | g | Exact t | First nonzero n residue |
|---:|---|---:|---:|---|
|25|yes|1|2|294 modulo 343|
|1231|yes|1|4|14406 modulo 16807|
|1567|yes|1|1|7 modulo 49|

The exact L and s for these controls are retained in both JSON receipts.
In particular a=1231 passes depths two, three and four at the **actual**
ternary position. The unique fixed-s index class genuinely contains its
u=200 at those depths; first mismatch occurs at depth five. The positive
sum control a=25 is outside the requested a>=31 family and adds no family
coverage. The original literal 313-digit word at (L,s)=(313,51) gives
`F modS=0`, `F mod9S=17496`, `n modS=1944`. Its product and sum are
calculated from the digits and both full predicates are independently false.

The independent checker also compares 2,015 literal words (every
`3<=L<=64,1<=s<L`) with its decimal-block residues, and completely enumerates
the small a=7 case. All twelve admissible exponents below the analytic
cutoff, `31,37,43,49,55,61,67,73,79,85,91,97`, are freshly reconstructed
by both methods and compared with the inherited certificates. At a=97 the
first failure is 2058 modulo 2401 (t=3). There is no missing finite obligation
in the **common-factor** theorem. No cutoff for all remaining positions
has been proved.

With the 257 inherited named members, this gives **259 excluded family
lengths**, all `a=31+6u` for `0<=u<=258`, through **a=1579**.
There are 85 class misses and 174 actual candidates, with valuation histogram
`{1:152,2:18,3:3,4:1}`. The next unchecked individual exponent is **1585**.
Only the explicitly listed 17 exponents are newly recomputed by each new
individual program; coverage of other rows is inherited, and their two
256-row receipts are cross-compared by the aggregate verifier.

These isolated lengths do not extend consecutive whole-length exclusion:
it remains **1 through 1,000,002,000,000 inclusive**. No historical trillion
scan or Lean build is rerun. The universal individual family, unrestricted
{5,7} subclass and wider digit-1 assertion remain open.
