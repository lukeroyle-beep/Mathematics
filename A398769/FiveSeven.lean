import A398769.Stage5

/-! All-length necessary restrictions for the remaining decimal alphabet {5, 7}.
These restrictions do not settle the two-five case or the full conjecture. -/

namespace A398769
namespace FiveSeven

private theorem noOneTwentyFive {ds : List ℕ} (hne : ds ≠ [])
    (ha : ∀ d ∈ ds, d = 5 ∨ d = 7) :
    ¬ 125 ∣ Nat.ofDigits 10 ds := by
  rintro ⟨q, hq⟩
  cases ds with
  | nil => contradiction
  | cons d ds =>
    have hd := ha d (by simp)
    cases ds with
    | nil =>
      simp [Nat.ofDigits] at hq
      omega
    | cons e ds =>
      have he := ha e (by simp)
      cases ds with
      | nil =>
        simp [Nat.ofDigits] at hq
        omega
      | cons f ds =>
        have hf := ha f (by simp)
        simp only [Nat.ofDigits_cons] at hq
        omega

/-- At every length, a number on the decimal alphabet {5, 7} satisfying
the product-times-sum divisibility condition contains at most two fives. -/
theorem atMostTwoFives {n : ℕ} (hpos : 0 < n)
    (ha : ∀ d ∈ Nat.digits 10 n, d = 5 ∨ d = 7)
    (hdiv : digitProduct n * digitSum n ∣ n) :
    (Nat.digits 10 n).count 5 ≤ 2 := by
  have h125 : ¬ 125 ∣ n := by
    have hne : Nat.digits 10 n ≠ [] := Nat.digits_ne_nil_iff_ne_zero.mpr (by omega)
    simpa only [Nat.ofDigits_digits] using noOneTwentyFive hne ha
  by_contra! hmany
  have h3 : 3 ≤ (Nat.digits 10 n).count 5 := by omega
  have hpow : 5 ^ 3 ∣ n :=
    dvd_trans (pow_dvd_pow 5 h3) (Stage2.fivePowCountDvd (ds := Nat.digits 10 n) hdiv)
  exact h125 hpow

#print axioms atMostTwoFives

private theorem sevenDvdAllSeven (ds : List ℕ) (ha : ∀ d ∈ ds, d = 7) :
    7 ∣ Nat.ofDigits 10 ds := by
  induction ds with
  | nil => simp [Nat.ofDigits]
  | cons d ds ih =>
    have hd := ha d (by simp)
    have ht : ∀ x ∈ ds, x = 7 := fun x hx => ha x (by simp [hx])
    simpa only [Nat.ofDigits_cons, hd] using
      Nat.dvd_add (by decide : 7 ∣ 7) (Nat.dvd_mul_left_of_dvd (ih ht) 10)

private theorem notSevenDvdOneFive (ds : List ℕ)
    (ha : ∀ d ∈ ds, d = 5 ∨ d = 7) (hcnt : ds.count 5 = 1) :
    ¬ 7 ∣ Nat.ofDigits 10 ds := by
  induction ds with
  | nil => simp at hcnt
  | cons d ds ih =>
    have ht : ∀ x ∈ ds, x = 5 ∨ x = 7 := fun x hx => ha x (by simp [hx])
    rcases ha d (by simp) with rfl | rfl
    · have hz : ds.count 5 = 0 := by simpa using hcnt
      have hall7 : ∀ x ∈ ds, x = 7 := by
        intro x hx
        rcases ht x hx with h | h
        · have hp : 0 < ds.count 5 := List.count_pos_iff.mpr (h ▸ hx)
          omega
        · exact h
      obtain ⟨k, hk⟩ := sevenDvdAllSeven ds hall7
      rintro ⟨q, hq⟩
      simp only [Nat.ofDigits_cons] at hq
      omega
    · have hc : ds.count 5 = 1 := by simpa using hcnt
      have hi := ih ht hc
      intro hdiv
      simp only [Nat.ofDigits_cons] at hdiv
      omega

/-- One 5 among any number of 7s makes the number nondivisible by 7.
Thus a qualifying number containing a 7 cannot have exactly one 5. -/
theorem notExactlyOneFiveWithSeven {n : ℕ}
    (ha : ∀ d ∈ Nat.digits 10 n, d = 5 ∨ d = 7)
    (h7 : 7 ∈ Nat.digits 10 n)
    (hdiv : digitProduct n * digitSum n ∣ n) :
    (Nat.digits 10 n).count 5 ≠ 1 := by
  intro hcnt
  have hnot : ¬ 7 ∣ n := by
    simpa only [Nat.ofDigits_digits] using notSevenDvdOneFive (Nat.digits 10 n) ha hcnt
  apply hnot
  exact dvd_trans (List.dvd_prod h7)
    (dvd_trans (show digitProduct n ∣ digitProduct n * digitSum n from ⟨_, rfl⟩) hdiv)

#print axioms notExactlyOneFiveWithSeven

private theorem singletonFive (ds : List ℕ) (ha : ∀ d ∈ ds, d = 5)
    (hcnt : ds.count 5 = 1) : ds = [5] := by
  cases ds with
  | nil => simp at hcnt
  | cons d ds =>
    have hd := ha d (by simp)
    cases ds with
    | nil => simp [hd]
    | cons e ds =>
      have he := ha e (by simp)
      simp [hd, he] at hcnt

/-- A qualifying number on the decimal alphabet {5, 7} cannot have exactly
one 5, including the degenerate word consisting of that one digit alone. -/
theorem notExactlyOneFive {n : ℕ}
    (ha : ∀ d ∈ Nat.digits 10 n, d = 5 ∨ d = 7)
    (hdiv : digitProduct n * digitSum n ∣ n) :
    (Nat.digits 10 n).count 5 ≠ 1 := by
  intro hcnt
  by_cases h7 : 7 ∈ Nat.digits 10 n
  · exact notExactlyOneFiveWithSeven ha h7 hdiv hcnt
  · have hall5 : ∀ d ∈ Nat.digits 10 n, d = 5 := by
      intro d hd
      rcases ha d hd with h | h
      · exact h
      · exact (h7 (h ▸ hd)).elim
    have hds := singletonFive (Nat.digits 10 n) hall5 hcnt
    have hn : n = 5 := by
      calc
        n = Nat.ofDigits 10 (Nat.digits 10 n) := (Nat.ofDigits_digits 10 n).symm
        _ = 5 := by rw [hds]; rfl
    subst n
    exact (by decide : ¬ digitProduct 5 * digitSum 5 ∣ 5) hdiv

#print axioms notExactlyOneFive

end FiveSeven
end A398769
