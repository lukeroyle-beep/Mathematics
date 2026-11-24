// Exact enumeration of length-L decimal words over {1,3} with b threes,
// divisible by a supplied positive odd divisor D. GMP handles full integers;
// the native suffix residue is bounded by 10^6 and counters are checked.
//
// CLI: search LENGTH COUNT_THREES DIVISOR [MAX_NODES] [MAX_MILLISECONDS]
// A zero or omitted resource limit means unlimited. A limited result never
// certifies a complete case, although any reported witnesses remain valid.
#include <gmpxx.h>

#include <array>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

using Clock = std::chrono::steady_clock;
constexpr unsigned MAX_LENGTH = 75;

static bool decimal(const std::string& text) {
    if (text.empty()) return false;
    for (char c : text) if (c < '0' || c > '9') return false;
    return true;
}

static uint64_t counter_argument(const char* text) {
    std::string s(text);
    if (!decimal(s)) throw std::invalid_argument("expected unsigned decimal integer");
    size_t used = 0;
    unsigned long long value = std::stoull(s, &used, 10);
    if (used != s.size() || value > std::numeric_limits<uint64_t>::max())
        throw std::invalid_argument("integer exceeds uint64 range");
    return static_cast<uint64_t>(value);
}

class Search {
public:
    const unsigned length, b;
    const mpz_class divisor;
    uint64_t nodes = 0, leaves = 0, candidates_tested = 0;
    std::vector<std::string> witnesses;
    bool limited = false;
    std::string termination_reason = "exhausted";

    Search(unsigned length_, unsigned b_, const mpz_class& divisor_,
           uint64_t max_nodes_, uint64_t max_milliseconds_)
        : length(length_), b(b_), divisor(divisor_),
          max_nodes(max_nodes_), max_milliseconds(max_milliseconds_),
          start(Clock::now()) {
        powers[0] = 1;
        repunits[0] = 0;
        for (unsigned r = 1; r <= length; ++r) {
            powers[r] = powers[r - 1] * 10;
            repunits[r] = repunits[r - 1] * 10 + 1;
        }
        for (unsigned r = 0; r <= length; ++r) {
            minimum_add[r] = 2 * repunits[r];
            weights[r] = 2 * powers[r];
        }
        suffix_digits = length < 6 ? length : 6;
        suffix_modulus = 1;
        for (unsigned i = 0; i < suffix_digits; ++i) suffix_modulus *= 10;
        const mpz_class stride = 2 * divisor;
        for (unsigned r = 0; r <= length; ++r) {
            for (unsigned k = 0; k <= r; ++k) {
                widths[r][k] = minimum_add[k] * (powers[r - k] - 1);
                terminal[r][k] = widths[r][k] < stride;
            }
        }
        value = repunits[length];
    }

    void run() { visit(length, b); }

    double elapsed_seconds() const {
        return std::chrono::duration<double>(Clock::now() - start).count();
    }

private:
    const uint64_t max_nodes, max_milliseconds;
    const Clock::time_point start;
    std::array<mpz_class, MAX_LENGTH + 1> powers, repunits, minimum_add, weights;
    std::array<std::array<mpz_class, MAX_LENGTH + 1>, MAX_LENGTH + 1> widths;
    std::array<std::array<bool, MAX_LENGTH + 1>, MAX_LENGTH + 1> terminal{};
    mpz_class value, lower, quotient, candidate, delta;
    unsigned suffix_digits = 0;
    unsigned long suffix_modulus = 1;

    void stop(const char* reason) {
        limited = true;
        termination_reason = reason;
    }

    bool increment(uint64_t& counter) {
        if (counter == std::numeric_limits<uint64_t>::max()) {
            stop("counter_limit");
            return false;
        }
        ++counter;
        return true;
    }

    bool enter_node() {
        if (limited) return false;
        if (max_nodes != 0 && nodes >= max_nodes) {
            stop("node_limit");
            return false;
        }
        // Time is only a resource limit, never part of a mathematical test.
        // Check every 4096 nodes to keep wide prefix traversal inexpensive.
        if (max_milliseconds != 0 && (nodes & 4095U) == 0) {
            auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
                Clock::now() - start).count();
            if (elapsed >= 0 && static_cast<uint64_t>(elapsed) >= max_milliseconds) {
                stop("time_limit");
                return false;
            }
        }
        return increment(nodes);
    }

    void visit(unsigned remaining, unsigned required) {
        if (!enter_node()) return;
        // Invariant: value is the fixed prefix followed by all 1s. The suffix
        // must replace exactly `required` of `remaining` 1s with 3s. Its least
        // value places these 3s at the right; its greatest puts them at left.
        // Their difference is precomputed as widths[remaining][required].
        if (terminal[remaining][required]) {
            if (!increment(leaves)) return;
            lower = value + minimum_add[required];
            // Every candidate and D are odd, so only odd quotients can work.
            // Consecutive possible multiples are 2D apart. The interval here
            // has width < 2D and therefore contains at most one of them.
            mpz_cdiv_q(quotient.get_mpz_t(), lower.get_mpz_t(), divisor.get_mpz_t());
            if (mpz_even_p(quotient.get_mpz_t())) ++quotient;
            candidate = quotient * divisor;
            delta = candidate - lower;
            if (delta > widths[remaining][required]) return;
            if (!increment(candidates_tested)) return;
            // Necessary decimal-suffix test before allocating the full string.
            // The modulus is at most 10^6, so the remainder and arithmetic
            // below fit unsigned long on every supported GMP platform. Test
            // exactly suffix_digits positions; leading zeroes must also fail.
            unsigned long suffix = mpz_fdiv_ui(candidate.get_mpz_t(), suffix_modulus);
            for (unsigned i = 0; i < suffix_digits; ++i) {
                unsigned long digit = suffix % 10;
                if (digit != 1 && digit != 3) return;
                suffix /= 10;
            }
            std::string digits = candidate.get_str();
            if (digits.size() != length) return;
            unsigned threes = 0;
            for (char digit : digits) {
                if (digit == '3') ++threes;
                else if (digit != '1') return;
            }
            if (threes == b) witnesses.push_back(std::move(digits));
            return;
        }
        // The branches partition every permissible suffix. Empty-count and
        // full-count suffixes have width zero and were already handled above.
        if (required < remaining) visit(remaining - 1, required);
        if (limited) return;
        if (required != 0) {
            value += weights[remaining - 1];
            visit(remaining - 1, required - 1);
            value -= weights[remaining - 1];
        }
    }
};

int main(int argc, char** argv) {
    try {
        if (argc < 4 || argc > 6)
            throw std::invalid_argument(
                "usage: search LENGTH COUNT_THREES DIVISOR [MAX_NODES] [MAX_MILLISECONDS]");
        uint64_t parsed_length = counter_argument(argv[1]);
        uint64_t parsed_b = counter_argument(argv[2]);
        if (parsed_length == 0 || parsed_length > MAX_LENGTH || parsed_b > parsed_length)
            throw std::invalid_argument("require 1 <= LENGTH <= 75 and 0 <= COUNT_THREES <= LENGTH");
        std::string divisor_text(argv[3]);
        if (!decimal(divisor_text)) throw std::invalid_argument("DIVISOR must be positive odd decimal");
        mpz_class divisor(divisor_text, 10);
        if (divisor <= 0 || mpz_even_p(divisor.get_mpz_t()))
            throw std::invalid_argument("DIVISOR must be positive and odd");
        uint64_t max_nodes = argc >= 5 ? counter_argument(argv[4]) : 0;
        uint64_t max_milliseconds = argc >= 6 ? counter_argument(argv[5]) : 0;
        Search search(static_cast<unsigned>(parsed_length), static_cast<unsigned>(parsed_b),
                      divisor, max_nodes, max_milliseconds);
        search.run();
        std::cout << "{\"engine\":\"stage4-prefix-v1\",\"status\":\""
                  << (search.limited ? "limited" : "complete")
                  << "\",\"termination_reason\":\"" << search.termination_reason
                  << "\",\"length\":" << search.length << ",\"b\":" << search.b
                  << ",\"divisor\":\"" << divisor.get_str()
                  << "\",\"max_nodes\":" << max_nodes
                  << ",\"max_milliseconds\":" << max_milliseconds
                  << ",\"nodes\":" << search.nodes << ",\"leaves\":" << search.leaves
                  << ",\"candidates_tested\":" << search.candidates_tested
                  << ",\"elapsed_seconds\":" << std::setprecision(9) << search.elapsed_seconds()
                  << ",\"witnesses\":[";
        for (size_t i = 0; i < search.witnesses.size(); ++i) {
            if (i != 0) std::cout << ',';
            std::cout << '"' << search.witnesses[i] << '"';
        }
        std::cout << "]}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
