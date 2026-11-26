// Independent exhaustive rational-centre enumerator. No search-code imports.
// Standard C++17; integer-only arithmetic; unsigned __int128 products.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using U = uint64_t;
using I = int64_t;
using W = unsigned __int128;
static U mul(U a,U b,U m){return U(W(a)*b%m);}
static U power(U a,U e,U m){U z=1;for(;e;e>>=1,a=mul(a,a,m))if(e&1)z=mul(z,a,m);return z;}
static I floor_div(I a,I b){I q=a/b,r=a%b;return q-(r<0);}
static I ceil_div(I a,I b){return -floor_div(-a,b);}
static I mod(I a,I m){I r=a%m;return r<0?r+m:r;}
static I inverse(I a,I m){for(I x=1;x<m;++x)if(a*x%m==1)return x;throw std::runtime_error("noninvertible numerator");}
static U F(U x,U y,U m){return U((W(7)*x+W(18)*m-W(18)*y+m-25)%m);}
// Original decimal word: n=7R_L - 2 - 2*10^i. Computing R_L modulo S
// via modulo 9S and exact division retains all factors of 3 in S.
static bool original_sum(U L,U i){U S=7*L-4,m=9*S;U t=power(10,L,m);if(t%9!=1)throw std::runtime_error("repunit invariant");U R=(t-1)/9;U p=power(10,i,S);return (W(7)*R+W(3)*S-2-W(2)*p)%S==0;}
struct Node{U r,x,y;};
struct Pair{U L,i;bool operator<(const Pair&o)const{return L<o.L||(L==o.L&&i<o.i);}};
struct Counters{U reduced=0,raw=0,compatible=0,phases=0,roots=0,pairs=0,fivefree=0,sum=0,depth22=0,fivefree22=0,sum22=0,singular_lines=0,singular_children=0;};
int main(int argc,char**argv){try{
  I K=0,b=0,lo=0,hi=0,hlim=-1;int depth=13;std::string pairs_path,pairs22_path,json_path;
  for(int j=1;j<argc;++j){std::string k=argv[j];if(j+1==argc)throw std::runtime_error("missing argument");std::string v=argv[++j];if(k=="--K")K=std::stoll(v);else if(k=="--b")b=std::stoll(v);else if(k=="--lo")lo=std::stoll(v);else if(k=="--hi")hi=std::stoll(v);else if(k=="--depth")depth=std::stoi(v);else if(k=="--h-limit")hlim=std::stoll(v);else if(k=="--pairs")pairs_path=v;else if(k=="--pairs22")pairs22_path=v;else if(k=="--json")json_path=v;else throw std::runtime_error("unknown option: "+k);}
  if(K<1||b<2||lo<3||hi<lo||hi>2000000000000000LL||depth<1||depth>22||pairs_path.empty()||pairs22_path.empty()||json_path.empty())throw std::runtime_error("invalid arguments");
  if(hlim<0)hlim=K*K; if(hlim>1000000)throw std::runtime_error("h-limit too large");
  std::array<U,23> seven{};seven[0]=1;for(int j=1;j<=22;++j)seven[j]=seven[j-1]*7;
  const U modulus=seven[depth], period=seven[depth-1], screen=seven[22];
  std::ofstream out(pairs_path),out22(pairs22_path);if(!out||!out22)throw std::runtime_error("pair output unavailable");
  // Multiplier tables are computed independently from line bases and exponent orders.
  using Shifts=std::array<std::array<U,7>,22>;
  auto shifts=[&](I step){Shifts t{};U v=power(10,U(step),modulus);for(int k=1;k<depth;++k){if(k>1)v=power(v,7,modulus);t[k][0]=1;for(int c=1;c<7;++c)t[k][c]=mul(t[k][c-1],v,modulus);}return t;};
  Shifts length_shifts=shifts(6*b);Counters c;
  for(I a=1;a<b;++a){if(std::gcd(a,b)!=1)continue;++c.reduced;I inv=inverse(a,b);auto position_shifts=shifts(6*a);const I linear=mod(4*a,7);I linear_inverse=linear?inverse(linear,7):0;
    for(I h=-hlim;h<=hlim;++h){++c.raw;I L0=mod(-h*inv,b),i0=(a*L0+h)/b;std::vector<int> phases;
      for(int t=0;t<6;++t)if(mod(L0+b*t,2)==1&&mod(i0+a*t,6)==3)phases.push_back(t);
      if(phases.empty())continue;++c.compatible;c.phases+=phases.size();if(a%7==0)++c.singular_lines;
      std::vector<Pair> actual;
      for(int t:phases){I baseL=L0+b*t,basei=i0+a*t;I first=std::max({ceil_div(lo-baseL,6*b),ceil_div(3-basei,6*a),ceil_div(basei-baseL+1,6*(b-a))});I last=floor_div(hi-baseL,6*b);if(first>last)continue;U L=U(baseL+6*b*first),i=U(basei+6*a*first),umax=U(last-first);
        std::vector<Node> nodes{{0,power(10,L,modulus),power(10,i,modulus)}};
        if(F(nodes[0].x,nodes[0].y,modulus)%7!=0)throw std::runtime_error("initial seventh-power condition");
        for(int k=1;k<depth&&!nodes.empty();++k){std::vector<Node> next;for(const Node&n:nodes){U residual=F(n.x,n.y,modulus);if(residual%seven[k])throw std::runtime_error("root invariant");I digit=I(residual/seven[k]%7);
            int first_child=0,last_child=6;if(linear){first_child=int(mod(-digit*linear_inverse,7));last_child=first_child;}else if(digit)continue;
            for(int j=first_child;j<=last_child;++j){U r=n.r+U(j)*seven[k-1];if(r>umax)continue;Node q{r,mul(n.x,length_shifts[k][j],modulus),mul(n.y,position_shifts[k][j],modulus)};if(F(q.x,q.y,modulus)%seven[k+1])throw std::runtime_error("lift invariant");next.push_back(q);if(!linear)++c.singular_children;}
          }nodes.swap(next);}
        c.roots+=nodes.size();for(const Node&n:nodes){for(U u=n.r;u<=umax;){U actualL=L+U(6*b)*u,actuali=i+U(6*a)*u;if(actualL<U(lo)||actualL>U(hi)||actuali<3||actuali>=actualL||(actualL&1)==0||actuali%6!=3)throw std::runtime_error("actual endpoint invariant");actual.push_back({actualL,actuali});if(umax-u<period)break;u+=period;}}
      }
      std::sort(actual.begin(),actual.end());for(size_t j=0;j<actual.size();++j){const auto p=actual[j];if(j&&p.L==actual[j-1].L&&p.i==actual[j-1].i)throw std::runtime_error("duplicate actual pair");out<<a<<','<<h<<','<<p.L<<','<<p.i<<'\n';++c.pairs;bool fivefree=(7*p.L-4)%5!=0;bool sum=fivefree&&original_sum(p.L,p.i);c.fivefree+=fivefree;c.sum+=sum;
        bool deep=F(power(10,p.L,screen),power(10,p.i,screen),screen)==0;if(deep){++c.depth22;c.fivefree22+=fivefree;c.sum22+=sum;out22<<a<<','<<h<<','<<p.L<<','<<p.i<<'\n';}
      }
    }
  }
  out.close();out22.close();if(!out||!out22)throw std::runtime_error("pair output write failed");
  std::ofstream js(json_path);if(!js)throw std::runtime_error("JSON output unavailable");
  js<<"{\n  \"K\": "<<K<<", \"b\": "<<b<<", \"lo\": "<<lo<<", \"hi\": "<<hi<<",\n  \"depth\": "<<depth<<", \"h_limit\": "<<hlim<<",\n  \"reduced_numerators\": "<<c.reduced<<", \"raw_lines\": "<<c.raw<<", \"compatible_lines\": "<<c.compatible<<",\n  \"phase_lines\": "<<c.phases<<", \"roots13\": "<<c.roots<<", \"pairs13\": "<<c.pairs<<", \"fivefree13\": "<<c.fivefree<<", \"sum13\": "<<c.sum<<",\n  \"pairs22\": "<<c.depth22<<", \"fivefree22\": "<<c.fivefree22<<", \"sum22\": "<<c.sum22<<",\n  \"singular_lines\": "<<c.singular_lines<<", \"singular_children\": "<<c.singular_children<<"\n}\n";js.close();if(!js)throw std::runtime_error("JSON write failed");return 0;
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
