#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string_view>
#include <vector>

// Generate the positive base-ten integers below 10^D divisible by the
// product of their digit sum and digit product. Supports D = 1,...,14.
using Int = std::uint64_t;
using Counts = std::array<unsigned, 10>;

class Enumerator {
    std::array<Int, 15> powers{};
    std::array<Int, 10000> plain{}, padded{};
    Counts counts{};
    std::vector<Int> values;

    // Four bits suffice for each digit's multiplicity in at most 14 places.
    static Int digit_unit(unsigned digit) { return Int{1} << (4 * digit); }

    Int signature(Int n) const {
        Int value = 0;
        while (n >= 10000) {
            value += padded[n % 10000];
            n /= 10000;
        }
        return value + plain[n];
    }

    void prefixes(unsigned places, unsigned tail, Int prefix, Int step,
                  Int residue, Int expected) {
        if (places > 0) {
            for (unsigned d = 1; d <= 9; ++d) {
                if (counts[d] == 0) continue;
                --counts[d];
                prefixes(places - 1, tail, 10 * prefix + d, step, residue, expected);
                ++counts[d];
            }
            return;
        }
        // The interval consists of all possible tails for this prefix.
        const Int width = powers[tail];
        const Int low = prefix * width;
        const Int rem = low % step;
        const Int offset = residue >= rem ? residue - rem : step - (rem - residue);
        if (offset < width) {
            const Int n = low + offset;
            if (n > 0 && signature(n) == expected) values.push_back(n);
        }
    }

    void fixed_digits(unsigned length, Int sum, Int product, Int expected) {
        const Int modulus = sum * product;
        if (modulus >= powers[length]) return;
        // A last digit must be a nonzero multiple of gcd(modulus,10).
        const unsigned g10 = std::gcd(modulus, Int{10});
        bool possible_last = false;
        for (unsigned d = g10; d <= 9; d += g10)
            possible_last = possible_last || counts[d] > 0;
        if (!possible_last) return;

        // Decimal digit sum gives the additional necessary condition n = sum mod 9.
        const Int g9 = std::gcd(modulus, Int{9});
        if (sum % g9 != 0) return;
        const Int step = modulus * (9 / g9);
        Int residue = 0;
        while (residue % 9 != sum % 9) residue += modulus;

        // Tail width at most 'step' gives at most one candidate per prefix.
        unsigned tail = 0;
        while (tail < length && powers[tail + 1] <= step) ++tail;
        prefixes(length - tail, tail, 0, step, residue, expected);
    }

    void multisets(unsigned length, unsigned digit, unsigned left,
                   Int sum, Int product, Int expected) {
        if (digit == 10) {
            if (left == 0) fixed_digits(length, sum, product, expected);
            return;
        }
        for (unsigned count = 0; count <= left; ++count) {
            counts[digit] = count;
            multisets(length, digit + 1, left - count, sum, product, expected);
            sum += digit;
            product *= digit;
            expected += digit_unit(digit);
        }
    }

public:
    Enumerator() {
        powers[0] = 1;
        for (unsigned i = 1; i < powers.size(); ++i) powers[i] = 10 * powers[i-1];
        for (unsigned i = 0; i < plain.size(); ++i) {
            unsigned n = i;
            for (unsigned place = 0; place < 4; ++place) {
                const Int unit = digit_unit(n % 10);
                padded[i] += unit;
                if (n > 0) plain[i] += unit;
                n /= 10;
            }
        }
    }

    std::vector<Int> run(unsigned limit) {
        for (unsigned length = 1; length <= limit; ++length) {
            auto initial_size = values.size();
            multisets(length, 1, length, 0, 1, 0);
            std::cerr << length << " digits: " << values.size() - initial_size << '\n';
        }
        std::sort(values.begin(), values.end());
        if (std::adjacent_find(values.begin(), values.end()) != values.end())
            throw std::logic_error("duplicate result");
        return values;
    }
};

int main(int argc, char** argv) {
    if (argc != 2) { std::cerr << "usage: parent max-digits (1-14)\n"; return 2; }
    const std::string_view arg(argv[1]);
    unsigned limit = 0;
    const auto parsed = std::from_chars(arg.data(), arg.data() + arg.size(), limit);
    if (parsed.ec != std::errc{} || parsed.ptr != arg.data() + arg.size() ||
        limit < 1 || limit > 14) return 2;
    auto terms = Enumerator().run(limit);
    for (std::size_t i = 0; i < terms.size(); ++i)
        std::cout << (i + 1) << ' ' << terms[i] << '\n';
}
