import Mathlib.Data.Nat.Digits.Defs
import Mathlib.Algebra.BigOperators.Group.List.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
# The {3, 9} decimal-digit reduction

This module independently reconstructs the reduction directly from `Nat.digits 10 n`.
Digits are listed least significant first; length, count, sum and product do not
change when the order is reversed. No finite search is part of this proof.
-/

namespace A398769

/-- Every actual decimal digit of `n` is either 3 or 9. -/
def DigitsThreeOrNine (n : ℕ) : Prop :=
  ∀ d ∈ Nat.digits 10 n, d = 3 ∨ d = 9

/-- Decimal digit length. -/
def digitLength (n : ℕ) : ℕ := (Nat.digits 10 n).length

/-- Number of occurrences of 9 among the decimal digits. -/
def numberOfNines (n : ℕ) : ℕ := (Nat.digits 10 n).count 9

/-- Product of the actual decimal digits. -/
def digitProduct (n : ℕ) : ℕ := (Nat.digits 10 n).prod

/-- Sum of the actual decimal digits. -/
def digitSum (n : ℕ) : ℕ := (Nat.digits 10 n).sum

/-- Derive the product formula by induction on the digits. -/
lemma prod_three_or_nine (ds : List ℕ)
    (h : ∀ d ∈ ds, d = 3 ∨ d = 9) :
    ds.prod = 3 ^ (ds.length + ds.count 9) := by
  induction ds with
  | nil => simp
  | cons d ds ih =>
      have ht : ∀ x ∈ ds, x = 3 ∨ x = 9 := fun x hx => h x (by simp [hx])
      rcases h d (by simp) with rfl | rfl
      · simp [ih ht, pow_add]
        ring
      · simp [ih ht, pow_add]
        ring

/-- Derive the sum formula by induction on the digits. -/
lemma sum_three_or_nine (ds : List ℕ)
    (h : ∀ d ∈ ds, d = 3 ∨ d = 9) :
    ds.sum = 3 * (ds.length + 2 * ds.count 9) := by
  induction ds with
  | nil => simp
  | cons d ds ih =>
      have ht : ∀ x ∈ ds, x = 3 ∨ x = 9 := fun x hx => h x (by simp [hx])
      rcases h d (by simp) with rfl | rfl
      · simp [ih ht]
        omega
      · simp [ih ht]
        omega

/-- Decimal reconstruction is divisible by 3 independently of the target condition. -/
lemma three_dvd_ofDigits (ds : List ℕ)
    (h : ∀ d ∈ ds, d = 3 ∨ d = 9) :
    3 ∣ Nat.ofDigits 10 ds := by
  induction ds with
  | nil => simp
  | cons d ds ih =>
      have ht : ∀ x ∈ ds, x = 3 ∨ x = 9 := fun x hx => h x (by simp [hx])
      have hd : 3 ∣ d := by
        rcases h d (by simp) with rfl | rfl <;> norm_num
      simpa [Nat.ofDigits] using Nat.dvd_add hd (Nat.dvd_mul_left_of_dvd (ih ht) 10)

/-- Both closed forms are consequences of the actual-digit hypothesis. -/
theorem digit_formulas_of_three_or_nine {n : ℕ} (h : DigitsThreeOrNine n) :
    digitProduct n = 3 ^ (digitLength n + numberOfNines n) ∧
    digitSum n = 3 * (digitLength n + 2 * numberOfNines n) := by
  exact ⟨prod_three_or_nine (Nat.digits 10 n) h,
    sum_three_or_nine (Nat.digits 10 n) h⟩

/-- Every natural number with only decimal digits 3 and 9 is a multiple of 3. -/
theorem three_dvd_of_three_or_nine {n : ℕ} (h : DigitsThreeOrNine n) : 3 ∣ n := by
  simpa only [Nat.ofDigits_digits] using three_dvd_ofDigits (Nat.digits 10 n) h

/--
For positive `n` whose actual decimal digits are all 3 or 9, `P * S ∣ n` if and
only if `3^(L+b) * (L+2*b) ∣ n/3`, with all four quantities defined from its digits.
The proof below works even for zero; positivity is retained to match the statement.
-/
theorem stage4_reduction {n : ℕ} (_hn : 0 < n) (h : DigitsThreeOrNine n) :
    digitProduct n * digitSum n ∣ n ↔
      3 ^ (digitLength n + numberOfNines n) *
        (digitLength n + 2 * numberOfNines n) ∣ n / 3 := by
  obtain ⟨hp, hs⟩ := digit_formulas_of_three_or_nine h
  have hn3 : n = 3 * (n / 3) := by
    have := Nat.mod_eq_zero_of_dvd (three_dvd_of_three_or_nine h)
    omega
  rw [hp, hs]
  have hprod : 3 ^ (digitLength n + numberOfNines n) *
      (3 * (digitLength n + 2 * numberOfNines n)) =
      3 * (3 ^ (digitLength n + numberOfNines n) *
        (digitLength n + 2 * numberOfNines n)) := by ring
  rw [hprod]
  constructor
  · rintro ⟨k, hk⟩
    refine ⟨k, ?_⟩
    rw [mul_assoc] at hk
    omega
  · rintro ⟨k, hk⟩
    refine ⟨k, ?_⟩
    calc
      n = 3 * (n / 3) := hn3
      _ = _ := by rw [hk]; ring

#print axioms A398769.digit_formulas_of_three_or_nine
#print axioms A398769.three_dvd_of_three_or_nine
#print axioms A398769.stage4_reduction

end A398769
