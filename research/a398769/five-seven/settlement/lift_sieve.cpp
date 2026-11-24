// Exact, bounded congruence sieve. This is not an all-length certificate.
// C++17; unsigned __int128 intermediates, no floating-point arithmetic.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using U = std::uint64_t;
using Wide = unsigned __int128;

static void require(bool b, const char* message) {
    if (!b) throw std::runtime_error(message);
}
static U mul(U a, U b, U m) { return static_cast<U>(Wide(a) * b % m); }
static U power(U a, U b, U m) {
    U r = 1;
    for (; b; b >>= 1, a = mul(a, a, m)) if (b & 1) r = mul(r, a, m);
    return r;
}
struct Lift {
    U i, period;
    unsigned k;
};
struct Sieve {
    unsigned cap;
    std::array<U, 21> modulus{}, period{}, inverse{};
    std::array<std::array<U, 7>, 21> factors{};
    explicit Sieve(unsigned k) : cap(k) {
        require(1 <= cap && cap <= 20, "power must be in 1..20");
        modulus[0] = 1;
        for (unsigned j = 1; j <= cap; ++j) {
            modulus[j] = 7 * modulus[j-1];
            period[j] = 6 * modulus[j-1];
            require(power(10, period[j], modulus[j]) == 1, "order identity");
            for (U q : {U(2), U(3), U(7)}) if (period[j] % q == 0)
                require(power(10, period[j]/q, modulus[j]) != 1, "order minimality");
        }
        for (unsigned j = 1; j < cap; ++j) {
            U z = power(10, period[j], modulus[j+1]);
            require(z % modulus[j] == 1, "lifting identity");
            U c = (z - 1) / modulus[j];
            require(1 <= c && c < 7, "nonzero lifting coefficient");
            // 18*10^i = 3 (mod 7) because i = 3 (mod 6).
            for (U v = 1; v < 7; ++v) if ((3*c*v) % 7 == 1) inverse[j] = v;
            require(inverse[j] != 0, "lifting inverse");
            factors[j][0] = 1;
            U factor = power(10, period[j], modulus[cap]);
            for (unsigned t = 1; t < 7; ++t)
                factors[j][t] = mul(factors[j][t-1], factor, modulus[cap]);
        }
    }
    Lift solve(U L, U tenL, bool prune) const {
        U i = 3, tenI = 1000 % modulus[cap];
        unsigned k = 1;
        unsigned end = static_cast<unsigned>(std::min<U>(cap, L-2));
        for (; k < end; ++k) {
            U m = modulus[k+1];
            U y = mul(18, tenI % m, m);
            U target = (mul(7, tenL % m, m) + m - (25 % m)) % m;
            U difference = (target + m - y) % m;
            require(difference % modulus[k] == 0, "previous lift is not a solution");
            U t = mul(difference / modulus[k], inverse[k], 7);
            i += t * period[k];
            tenI = mul(tenI, factors[k][t], modulus[cap]);
            require(mul(18, tenI % m, m) == target, "new lift is not a solution");
            if (prune && i >= L) return {i, period[k+1], k+1};
        }
        return {i, period[k], k};
    }
};

int main(int argc, char** argv) try {
    U bound = 10000000;
    unsigned cap = 20;
    bool residues = false;
    for (int a = 1; a < argc; ++a) {
        std::string option(argv[a]);
        if (option == "--residues") residues = true;
        else if ((option == "--max" || option == "--power") && a+1 < argc) {
            std::string value(argv[++a]);
            require(!value.empty() && value.find_first_not_of("0123456789") == std::string::npos,
                    "expected a nonnegative decimal argument");
            U parsed = std::stoull(value);
            if (option == "--max") bound = parsed;
            else { require(parsed <= 20, "power exceeds 20"); cap = unsigned(parsed); }
        } else throw std::runtime_error("unknown or incomplete argument");
    }
    require(5 <= bound && bound <= 100000000, "max must be in 5..100000000");
    require(!residues || bound <= 10000, "residue output is limited to max 10000");
    Sieve s(cap);
    U tenL = power(10, 5, s.modulus[cap]);
    U count = 0;
    std::array<U, 21> rejected{};
    std::vector<std::array<U, 2>> survivors;
    std::cout << "{\"method\":\"successive_unique_exponent_lifting\",\"max_length_inclusive\":"
              << bound << ",\"power_cap\":" << cap << ",\"modulus\":" << s.modulus[cap];
    if (residues) std::cout << ",\"residues\":[";
    for (U L = 5; L <= bound; L += 2) {
        Lift r = s.solve(L, tenL, !residues);
        if (residues) {
            if (count) std::cout << ',';
            std::cout << '[' << L << ',' << r.i << ',' << r.period << ']';
        } else if (r.i >= L) ++rejected[r.k];
        else for (U i = r.i; i < L; i += r.period) survivors.push_back({L, i});
        ++count;
        tenL = mul(tenL, 100, s.modulus[cap]);
    }
    require(count == (bound-3)/2, "length coverage count");
    if (residues) std::cout << ']';
    std::cout << ",\"odd_lengths_checked\":" << count;
    if (residues) {
        std::cout << ",\"mode\":\"residues_only_no_exclusion_claim\"}\n";
        return 0;
    }
    std::cout << ",\"mode\":\"bounded_sieve\",\"rejected_at_power\":{";
    bool first = true;
    for (unsigned k = 1; k <= cap; ++k) if (rejected[k]) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << '\"' << k << "\":" << rejected[k];
    }
    std::cout << "},\"truncated_7_power_survivors\":[";
    for (std::size_t j = 0; j < survivors.size(); ++j) {
        if (j) std::cout << ',';
        std::cout << '[' << survivors[j][0] << ',' << survivors[j][1] << ']';
    }
    std::cout << "]}\n";
    return 0;
} catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
