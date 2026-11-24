// Independently enumerate A398769 counterexamples of one exact decimal length.
// Compile with GCC or Clang: c++ -std=c++17 -O3 prefix23.cpp -o prefix23
// Usage: ./prefix23 LENGTH [--include-one | --multiset DIGITS].
// Length is 1..23. Use --include-one for small positive controls, or supply
// one multiset of odd digits with --multiset to test it at full width.

#include <algorithm>
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

namespace {
#if !defined(__SIZEOF_INT128__)
#error An unsigned 128-bit integer type is required.
#endif
using Number = __uint128_t;
using Count = std::uint64_t;
constexpr unsigned maximum_length = 23;
using DigitCounts = std::array<unsigned, 10>;

std::string decimal(Number n) {
    if (n == 0) return "0";
    std::string result;
    while (n != 0) {
        result.push_back(static_cast<char>('0' + n % 10));
        n /= 10;
    }
    std::reverse(result.begin(), result.end());
    return result;
}

struct Audit {
    Count multisets{}, viable_multisets{}, prefixes{}, tails_in_range{}, hits{};
};

class Search {
    const unsigned length;
    const std::vector<unsigned> digits;
    Audit audit;
    DigitCounts remaining{};

    // The multiset supplies the exact number of places to consume, including
    // any would-be leading zero in a padded suffix, which we must reject.
    bool matches_suffix(Number suffix, unsigned places) const {
        auto unused = remaining;
        for (unsigned i=0; i<places; ++i) {
            const unsigned digit = static_cast<unsigned>(suffix % 10);
            if (unused[digit] == 0) return false;
            --unused[digit];
            suffix /= 10;
        }
        return suffix == 0;
    }

    void prefixes(unsigned places, Number prefix, Number width, unsigned tail_length,
                  Number divisor, unsigned sum, Number product) {
        if (places > 0) {
            for (const unsigned digit : digits) {
                if (remaining[digit] == 0) continue;
                --remaining[digit];
                prefixes(places-1, 10*prefix+digit, width, tail_length, divisor, sum, product);
                ++remaining[digit];
            }
            return;
        }
        ++audit.prefixes;
        // n=prefix*width+tail. Since 0<=tail<width<=divisor, at most one
        // tail is possible. Compute the least nonnegative residue of -base.
        const Number base = prefix * width;
        const Number residue = base % divisor;
        const Number tail = residue == 0 ? 0 : divisor - residue;
        if (tail >= width) return;
        ++audit.tails_in_range;
        if (!matches_suffix(tail, tail_length)) return;

        ++audit.hits;
        const Number n = base + tail;
        std::cout << "hit " << decimal(n) << " sum=" << sum
                  << " product=" << decimal(product)
                  << " quotient=" << decimal(n / divisor) << '\n';
    }

    void process_multiset(unsigned sum, Number product) {
        ++audit.multisets;
        const Number divisor = sum * product;
        // The largest decimal value with this exact multiset occurs in
        // decreasing digit order. Nothing smaller than divisor can qualify.
        Number upper = 0;
        for (auto it=digits.rbegin(); it!=digits.rend(); ++it) {
            for (unsigned j=0; j<remaining[*it]; ++j) upper = 10*upper + *it;
        }
        if (divisor > upper) return;
        ++audit.viable_multisets;
        Number width = 1;
        unsigned tail_length = 0;
        while (tail_length < length && 10*width <= divisor) {
            width *= 10;
            ++tail_length;
        }
        prefixes(length-tail_length, 0, width, tail_length, divisor, sum, product);
    }

    void multiset(unsigned digit_index, unsigned positions, unsigned sum, Number product) {
        if (digit_index == digits.size()) {
            if (positions == 0) process_multiset(sum, product);
            return;
        }
        const unsigned digit = digits[digit_index];
        Number next_product = product;
        for (unsigned copies=0; copies<=positions; ++copies) {
            remaining[digit] = copies;
            multiset(digit_index+1, positions-copies, sum+copies*digit, next_product);
            // Avoid even one surplus power at the final iteration.
            if (copies < positions) next_product *= digit;
        }
        remaining[digit] = 0;
    }

public:
    Search(unsigned length, bool include_one) :
        length(length), digits(include_one ? std::vector<unsigned>{1,3,5,7,9}
                                         : std::vector<unsigned>{3,5,7,9}) {}

    void run(std::string_view exact_multiset) {
        if (exact_multiset.empty()) {
            multiset(0, length, 0, 1);
        } else {
            unsigned sum = 0;
            Number product = 1;
            for (const char ch : exact_multiset) {
                const unsigned digit = static_cast<unsigned>(ch - '0');
                ++remaining[digit];
                sum += digit;
                product *= digit;
            }
            process_multiset(sum, product);
        }
        std::cout << "length=" << length << " multisets=" << audit.multisets
                  << " viable_multisets=" << audit.viable_multisets
                  << " prefixes=" << audit.prefixes
                  << " tails_in_range=" << audit.tails_in_range
                  << " hits=" << audit.hits << '\n';
    }
};
} // namespace

int main(int argc, char **argv) {
    if (argc < 2 || argc > 4) return 2;
    unsigned length = 0;
    const std::string_view arg(argv[1]);
    const auto parsed = std::from_chars(arg.data(), arg.data()+arg.size(), length);
    if (parsed.ec != std::errc{} || parsed.ptr != arg.data()+arg.size()
        || length < 1 || length > maximum_length) return 2;
    const bool include_one = argc > 2;
    std::string_view exact_multiset;
    if (argc == 3 && std::string_view(argv[2]) != "--include-one") return 2;
    if (argc == 4) {
        exact_multiset = argv[3];
        if (std::string_view(argv[2]) != "--multiset" || exact_multiset.size() != length
            || exact_multiset.find_first_not_of("13579") != std::string_view::npos) return 2;
    }
    // All constructed numbers are below 10^23. The modulus is at most
    // 207 * 9^23, safely inside unsigned 128-bit arithmetic.
    // Complete each prefix with its remaining digits in sorted order.
    // The full word determines its multiset and split, so this is injective.
    // At most 5^23 such prefixes occur, even in the control alphabet.
    Search(length, include_one).run(exact_multiset);
}
