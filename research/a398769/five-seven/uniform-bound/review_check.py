import hashlib, json, math, sys
from fractions import Fraction

def req(c, msg):
    if not c: raise ValueError(msg)

def valuation(n):
    req(n != 0, 'valuation zero')
    d=0
    while n%7==0:
        n//=7;d+=1
    return d

def log_interval(n,N=120):
    z=Fraction(n-1,n+1)
    lo=sum((2*z**(2*k+1)/ (2*k+1) for k in range(N)),Fraction(0))
    return lo,lo+2*z**(2*N+1)/((2*N+1)*(1-z*z))

l7,u7=log_interval(7);l10,u10=log_interval(10)
req(168*u10*u10 < 63*l7**4, 'coefficient 63')
req(l10>2 and u7<2,'simple log inequalities')
cutoff=[]
for k in (9,10):
    lower=10_000_001 if k==9 else 6*7**(k-2)+1
    B=100_000*k*k
    D=1+252*(k+1)**3
    req(B<lower-2,'target cutoff')
    req(2*D<lower-2,'strong Hensel cutoff')
    req(D+k+1<lower-2,'dependent cutoff')
    cutoff.append(dict(K=k,least_odd_L=lower,target_margin=lower-2-B,hensel_margin=lower-2-2*D,dependent_margin=lower-2-D-k-1))
# Independently enumerate all reduced centres with b<=25, odd lengths b..101.
# Direct integral Q evaluations are compared with original expressions.
counts=dict(cases=0,snegative=0,positive_t=0,singular=0,high_derivative=0,strong_hensel=0)
maxd=0
for b in range(2,26):
  for a in range(1,b):
    if math.gcd(a,b)!=1: continue
    for L in range(max(5,b),102):
      if L%2==0:continue
      q,r=divmod(L,b);x=10**q
      for i in range(3,L):
        s=i-a*q;m=min(0,s);w=max(0,r,s)-m
        Cb,Ca,C0=7*10**(r-m),-18*10**(s-m),-25*10**(-m)
        F=7*10**L-18*10**i-25
        Q=Cb*x**b+Ca*x**a+C0
        deriv=b*Cb*x**(b-1)+a*Ca*x**(a-1)
        req(Q==10**(-m)*F,'Q identity')
        req(x*deriv==10**(-m)*(a*F+7*(b-a)*10**L+25*a),'derivative identity')
        req(w<=L-1,'span bound')
        req(F>0 and deriv>0,'nonzero')
        t,d=valuation(F),valuation(deriv)
        counts['cases']+=1;counts['snegative']+=s<0
        if t:
          counts['positive_t']+=1
          if a%7:
            req(d==0,'unit derivative')
          elif a%49==0:
            req(d==1,'7^2 derivative')
          else:
            counts['singular']+=1
            req(d==1+valuation(b*10**(L-i)-18*(a//7)),'singular formula')
            counts['high_derivative']+=d>1
          maxd=max(maxd,d)
          counts['strong_hensel']+=t>2*d
controls=[]
for a,b,L,i in [(7,9,11,9),(14,15,15,3),(49,50,51,3),(7,12,23,15)]:
 q,r=divmod(L,b);s=i-a*q;m=min(0,s);x=10**q
 F=7*10**L-18*10**i-25
 d=valuation(b*7*10**(r-m)*x**(b-1)-a*18*10**(s-m)*x**(a-1))
 controls.append(dict(a=a,b=b,L=L,i=i,t=valuation(F),d=d))
# Original-source Theorem 4 table, independently read from printed p. 5.
table=[(mu,nu,c) for nu,cs in [(5, ['53.8','36.1','28.1','24','18.6']), (10,['51.7','34.8','27.3','23.2','18'])] for mu,c in zip([4,6,8,10,15],map(Fraction,cs))]
req(7*l10*l10/Fraction(u7**4)>Fraction(7,4),'table coefficient lower bound')
req(min(c*nu**2 for mu,nu,c in table)==465,'table floor minimum')
req(Fraction(7,4)*465>800,'envelope floor 800')
# Rational witnesses for the envelope obstruction: every potentially small-enough
# denominator is checked directly at these actual rational positions, without
# replacing the rational point by its irrational limit.
coverage=[]
M=16_031_730
for k in [1,2,3,10,100]:
 L=1+M*k
 i=39+42*((math.isqrt(2*L*L)-L-18)//42)
 req(L%2==1 and 3<=i<L and i%42==39,'rational family domain')
 req(Fraction(41,100)<Fraction(i,L)<Fraction(42,100),'ratio interval')
 bmax=1
 while 1600*(bmax+1)**3<L-2:bmax+=1
 n=0
 for b in range(2,bmax+1):
  for a in range(1,b):
   if math.gcd(a,b)!=1:continue
   dist=abs(Fraction(i,L)-Fraction(a,b))
   req(dist>Fraction(1,800*b**3),'actual rational centre escape')
   req(800*b**3*max(2,L*dist)>L-2,'actual envelope insufficient')
   n+=1
 coverage.append(dict(L=L,i=i,denominators_through=bmax,centres_checked=n))
# Independently lift with modular Newton iteration, not a transformed polynomial
# or seven-way Hensel digit enumeration. Derivative divisions retain precision.
newton=[]
for a,b,L,i in [(5,12,23,15),(7,12,17,15),(7,9,233,183),(49,50,101,15)]:
 q,r=divmod(L,b);s=i-a*q;m=min(0,s);x=10**q
 terms={b:7*10**(r-m),a:-18*10**(s-m),0:-25*10**(-m)}
 def ev(z):return sum(c*z**e for e,c in terms.items())
 def dv(z):return sum(e*c*z**(e-1) for e,c in terms.items() if e)
 t,d=valuation(ev(x)),valuation(dv(x))
 req(t>2*d,'Newton hypothesis')
 N=t+d+5;fm=7**N;rm=7**(N-d);root=x%rm;steps=0
 while ev(root)%fm:
  f=ev(root)%fm;fp=dv(root)%fm
  req(valuation(fp)==d and f%7**d==0,'Newton divided quantities')
  correction=(f//7**d)*pow(fp//7**d,-1,rm)%rm
  root=(root-correction)%rm;steps+=1
  req(steps<=N,'Newton termination')
 req(valuation((root-x)%rm)==t-d,'Newton exact distance')
 req(valuation(dv(root))==d,'Newton derivative retained')
 newton.append(dict(a=a,b=b,L=L,i=i,t=t,d=d,distance=t-d,root_precision=N-d,polynomial_precision=N,iterations=steps))
# Retained actual zero run is checked from original modular F and exhaustive
# next representative at depth12, without the linearized digit formula.
L,i=69489,40323
period=6;K=1
while period<=L:period*=7;K+=1
req(K==6,'zero-run K')
def fmod(L,i,M):return(7*pow(10,L,M)-18*pow(10,i,M)-25)%M
req(fmod(L,i,7**12)==5*7**11,'zero-run depth certificate')
digits=[]
for k in range(6,12):
 period=6*7**(k-1)
 hits=[j for j in range(7) if fmod(L,i+j*period,7**(k+1))==0]
 req(len(hits)==1,'zero-run unique next digit')
 digits.append(hits[0])
req(digits==[0,0,0,0,0,4],'zero-run endpoint')
S=7*L-4
repunit=((pow(10,L,9*S)-1)//9)%S
nres=(7*repunit-2-2*pow(10,i,S))%S
req(9*nres==2218743,'independent full-sum rejection')
zero_run=dict(L=L,i=i,K=K,exact_depth=11,digits_a6_through_a11=digits,F_mod_9S=9*nres)
# Mutation controls use the same guards, and run under -O.
rejects=0
for op in [lambda:req(False,'mutated comparison'),lambda:valuation(0),lambda:req(controls[0]['d']==1,'bad universal d1'),lambda:req(controls[1]['t']>2*controls[1]['d'],'bad Hensel')]:
 try:op()
 except ValueError:rejects+=1
req(rejects==4,'failure guard count')
print(json.dumps(dict(source_sha256=hashlib.sha256(open(__file__,'rb').read()).hexdigest(),cutoff=cutoff,polynomial_controls=counts,largest_derivative=maxd,examples=controls,negative_controls_rejected=rejects,coefficient63_verified=True,theorem4_table_floor=465,theorem4_envelope_lower_bound=800,rational_coverage_controls=coverage,modular_newton_controls=newton,zero_run=zero_run),indent=2,sort_keys=True))
