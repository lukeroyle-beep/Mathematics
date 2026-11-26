// Exhaustive bounded line lifting. No dependency on independent.cpp.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using U=uint64_t; using W=__uint128_t; using I=__int128_t;
U mul(U a,U b,U m){return W(a)*b%m;}
U power(U a,U n,U m){U r=1;for(;n;n>>=1,a=mul(a,a,m))if(n&1)r=mul(r,a,m);return r;}
U norm(I x,U m){I r=x%m;return r<0?r+m:r;}
U inverse(U a,U m){for(U x=1;x<m;x++)if(a*x%m==1)return x;throw std::runtime_error("inverse");}
U residue(U x,U y,U m){return norm(I(7)*x-I(18)*y-25,m);}
struct Root{U u,x,y;};
struct Pair{U L,i;bool operator<(const Pair&o)const{return L<o.L||(L==o.L&&i<o.i);}};
int main(int argc,char**argv){try{
 int K=0,b=0,depth=22,at=13; U lo=0,hi=0; std::string pairs,pairs22,json;
 for(int j=1;j<argc;j+=2){if(j+1==argc)throw std::runtime_error("missing argument");std::string k=argv[j],v=argv[j+1];
  if(k=="--K")K=stoi(v);else if(k=="--b")b=stoi(v);else if(k=="--lo")lo=stoull(v);else if(k=="--hi")hi=stoull(v);
  else if(k=="--pairs")pairs=v;else if(k=="--pairs22")pairs22=v;else if(k=="--json")json=v;
  else if(k=="--depth")depth=stoi(v);else if(k=="--at")at=stoi(v);else throw std::runtime_error("unknown argument");}
 if(K<1||K>19||b<2||b>361||lo<5||lo>hi||hi>2000000000000000ULL||depth<1||depth>22||at<1||at>depth||pairs.empty()||pairs22.empty()||json.empty())throw std::runtime_error("invalid domain or output");
 U p7[23];p7[0]=1;for(int k=1;k<=22;k++)p7[k]=p7[k-1]*7;
 U mod=p7[depth],numerators=0,raw=0,compatible=0,phases=0,roots_at=0,np=0,nfive=0,nsum=0,n22=0,nfive22=0,nsum22=0,singular=0;
 std::ofstream out(pairs),out22(pairs22);if(!out||!out22)throw std::runtime_error("stream open");
 U stepL=6*b,baseLpow=power(10,lo,mod);std::vector<U> ltable(stepL);ltable[0]=baseLpow;
 for(U j=1;j<stepL;j++)ltable[j]=mul(ltable[j-1],10,mod);
 for(int a=1;a<b;a++){if(std::gcd(a,b)!=1)continue;numerators++;
  U stepI=6*a,g=std::gcd(a,3),period=3*b/g,inv=inverse(a/g,period),step=2*period;
  U iorigin=U(W(a)*lo/b)-4; // lo>=5 needs a separate safe floor for small controls.
  if(W(a)*lo/b<4)iorigin=0;
  std::vector<U> itable(6*a+20);itable[0]=power(10,iorigin,mod);
  for(U j=1;j<itable.size();j++)itable[j]=mul(itable[j-1],10,mod);
  U shiftsL[23][7]{},shiftsI[23][7]{};
  U sl=power(10,stepL,mod),si=power(10,stepI,mod);
  for(int k=1;k<depth;k++){shiftsL[k][0]=shiftsI[k][0]=1;
   for(int c=1;c<7;c++){shiftsL[k][c]=mul(shiftsL[k][c-1],sl,mod);shiftsI[k][c]=mul(shiftsI[k][c-1],si,mod);}
   sl=power(sl,7,mod);si=power(si,7,mod);}
  for(int h=-K*K;h<=K*K;h++){raw++; I rhs=I(3)*b-a-h;
   if(rhs%(2*g))continue;compatible++;if(a%7==0)singular++;
   U ell=mul(norm(rhs/(2*g),period),inv,period),Lr=2*ell+1;
   std::vector<Pair> current,deep;
   for(U phase=0;phase<g;phase++){phases++;U start=Lr+step*phase;
    if(start<lo)start+=((lo-start+stepL-1)/stepL)*stepL;
    if(start>hi)continue;
    I ii=(I(a)*start+h)/b;
    if(I(a)*start+h!=ii*b||start%2!=1||norm(ii,6)!=3)throw std::runtime_error("parametrization");
    // Enforce 3<=i<L by moving to the first eligible term; both inequalities persist.
    if(ii<3){U jump=U((3-ii+stepI-1)/stepI);start+=jump*stepL;ii+=jump*stepI;}
    if(ii>=I(start)){U jump=U((ii-I(start))/(stepL-stepI)+1);start+=jump*stepL;ii+=jump*stepI;}
    if(start>hi)continue;
    U istart=U(ii),last=(hi-start)/stepL;
    U x=start-lo<ltable.size()?ltable[start-lo]:power(10,start,mod);
    U y=istart>=iorigin&&istart-iorigin<itable.size()?itable[istart-iorigin]:power(10,istart,mod);
    std::vector<Root> roots{{0,x,y}};
    if(residue(x,y,7)!=0)throw std::runtime_error("depth one");
    for(int k=1;k<=depth;k++){
     if(k==at){roots_at+=roots.size();for(const auto&r:roots)for(U u=r.u;u<=last;u+=p7[k-1])current.push_back({start+stepL*u,istart+stepI*u});}
     if(k==depth){for(const auto&r:roots)for(U u=r.u;u<=last;u+=p7[k-1])deep.push_back({start+stepL*u,istart+stepI*u});break;}
     std::vector<Root> next;
     for(const auto&r:roots){U f=residue(r.x,r.y,p7[k+1]);if(f%p7[k])throw std::runtime_error("parent not root");
      int first=0,stop=7;
      if(a%7){U coefficient=norm(-3*a,7);first=norm(-I(f/p7[k])*inverse(coefficient,7),7);stop=first+1;}
      else if(f)continue; // All seven children or none. Never invert a singular derivative.
      for(int c=first;c<stop;c++){U u=r.u+c*p7[k-1];if(u>last)continue;
       Root nr{u,mul(r.x,shiftsL[k][c],mod),mul(r.y,shiftsI[k][c],mod)};
       if(residue(nr.x,nr.y,p7[k+1]))throw std::runtime_error("child not root");next.push_back(nr);}
     }roots.swap(next);if(roots.empty())break;
    }
   }
   std::sort(current.begin(),current.end());std::sort(deep.begin(),deep.end());
   auto process=[&](const std::vector<Pair>&v,std::ofstream&stream,U&count,U&five,U&sum){
    for(size_t j=0;j<v.size();j++){const auto&p=v[j];if(j&&v[j-1].L==p.L&&v[j-1].i==p.i)throw std::runtime_error("duplicate pair on line");
     if(p.L<lo||p.L>hi||p.i<3||p.i>=p.L||p.L%2!=1||p.i%6!=3||I(b)*p.i-I(a)*p.L!=h)throw std::runtime_error("actual bounds");
     count++;stream<<a<<','<<h<<','<<p.L<<','<<p.i<<'\n';U S=7*p.L-4;
     if(S%5){five++;U m=9*S;if(residue(power(10,p.L,m),power(10,p.i,m),m)==0)sum++;}
    }};
   process(current,out,np,nfive,nsum);process(deep,out22,n22,nfive22,nsum22);
  }
 }
 out.close();out22.close();if(!out||!out22)throw std::runtime_error("stream write");
 std::ofstream result(json);result<<"{\n\"K\":"<<K<<",\"b\":"<<b<<",\"lo\":"<<lo<<",\"hi\":"<<hi
 <<",\"depth\":"<<depth<<",\"at\":"<<at<<",\"reduced_numerators\":"<<numerators<<",\"raw_lines\":"<<raw
 <<",\"compatible_lines\":"<<compatible<<",\"phase_lines\":"<<phases<<",\"roots13\":"<<roots_at
 <<",\"pairs13\":"<<np<<",\"fivefree13\":"<<nfive<<",\"sum13\":"<<nsum<<",\"pairs22\":"<<n22
 <<",\"fivefree22\":"<<nfive22<<",\"sum22\":"<<nsum22<<",\"singular_lines\":"<<singular<<"\n}\n";
 result.close();if(!result)throw std::runtime_error("json write");return 0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
