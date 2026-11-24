// Independent exhaustive verifier for the base-ten OEIS A398769 conjecture.
// Build: c++ -std=c++17 -O3 -Wall -Wextra -pedantic suffix_check.cpp -o suffix_check
// Run: ./suffix_check [maximum decimal length, 1..19; default 19]
#include <array>
#include <charconv>
#include <cstdint>
#include <iostream>
#include <string_view>

namespace {
using Integer = std::uint64_t;
constexpr int capacity = 19;
constexpr std::array<unsigned, 4> digits{3, 5, 7, 9};
struct Counts {
    Integer surviving{};
    Integer product_divides{};
    Integer separate_divisibility{};
    Integer full_divisibility{};
};

int limit = capacity;
std::array<Integer, capacity + 1> powers_of_five{1}, powers_of_ten{1};
std::array<Counts, capacity + 1> counts{};

// At most 19 digits give n < 10^19 and P <= 9^19, both below 2^64.
// The final test checks S | (n/P) after P | n, so P*S is never constructed.
void prepend(Integer suffix, Integer product, unsigned sum, int length, int fives) {
    if (length == limit) return;
    const int next_length = length + 1;
    for (const unsigned digit : digits) {
        const Integer number = digit * powers_of_ten[length] + suffix;
        const int next_fives = fives + (digit == 5);
        // The final digit product includes 5^next_fives. Any prefix added
        // later changes number by a multiple of 10^next_length, and
        // next_fives <= next_length. A failed suffix can never be repaired.
        if (number % powers_of_five[next_fives] != 0) continue;
        const Integer next_product = digit * product;
        const unsigned next_sum = digit + sum;
        Counts &row = counts[next_length];
        ++row.surviving;
        // Every digit is odd, hence an even-length word has even sum
        // and cannot divide the odd number under the combined test.
        if (next_length % 2 == 1 && number % next_product == 0) {
            ++row.product_divides;
            if (number % next_sum == 0) ++row.separate_divisibility;
            if ((number / next_product) % next_sum == 0) {
                ++row.full_divisibility;
                std::cout << "witness " << number << ' ' << next_product
                          << ' ' << next_sum << ' ' << (number / next_product) / next_sum << '\n';
            }
        }
        prepend(number, next_product, next_sum, next_length, next_fives);
    }
}
} // namespace

int main(int argc, char **argv) {
    if (argc > 2) return 2;
    if (argc == 2) {
        const std::string_view arg(argv[1]);
        const auto parsed = std::from_chars(arg.data(), arg.data() + arg.size(), limit);
        if (parsed.ec != std::errc{} || parsed.ptr != arg.data() + arg.size()
            || limit < 1 || limit > capacity) {
            std::cerr << "Maximum length must be an integer from 1 through 19.\n";
            return 2;
        }
    }
    for (int j = 1; j <= limit; ++j) {
        powers_of_five[j] = powers_of_five[j-1] * 5;
        powers_of_ten[j] = powers_of_ten[j-1] * 10;
    }
    prepend(0, 1, 0, 0, 0);
    std::cout << "digits,suffix_survivors,product_divides,separately_divide,full_divisibility\n";
    for (int j = 1; j <= limit; j += 2) {
        const auto &row = counts[j];
        std::cout << j << ',' << row.surviving << ',' << row.product_divides
                  << ',' << row.separate_divisibility << ',' << row.full_divisibility << '\n';
    }
}
