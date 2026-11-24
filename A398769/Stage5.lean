import A398769.Stage2

namespace A398769
namespace Stage5

private theorem noTwentyFive {ds : List ℕ} (hne : ds ≠ [])
    (ha : ∀ d ∈ ds, d = 3 ∨ d = 5 ∨ d = 9) :
    ¬ 25 ∣ Nat.ofDigits 10 ds := by
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
      simp only [Nat.ofDigits_cons] at hq
      omega

private theorem residueThree (ds : List ℕ)
    (ha : ∀ d ∈ ds, d = 3 ∨ d = 5 ∨ d = 9) :
    Nat.ofDigits 10 ds % 3 = (2 * ds.count 5) % 3 := by
  induction ds with
  | nil => rfl
  | cons d ds ih =>
    have ht : ∀ x ∈ ds, x = 3 ∨ x = 5 ∨ x = 9 := fun x hx => ha x (by simp [hx])
    have hi := ih ht
    rcases ha d (by simp) with rfl | rfl | rfl <;>
      simp [Nat.ofDigits_cons] <;> omega

private theorem fiveDividesSum (ds : List ℕ) (ha : ∀ d ∈ ds, d = 5) : 5 ∣ ds.sum := by
  induction ds with
  | nil => simp
  | cons d ds ih =>
    have hd := ha d (by simp)
    have ht : ∀ x ∈ ds, x = 5 := fun x hx => ha x (by simp [hx])
    have hi := ih ht
    simp only [List.sum_cons, hd]
    omega

/-- In the absence of a 7, a counterexample would use only 3 and 9. -/
theorem digitsThreeOrNine_of_noSeven {n : ℕ} (hpos : 0 < n) (hn : Odd n)
    (h1 : 1 ∉ Nat.digits 10 n) (hdiv : digitProduct n * digitSum n ∣ n)
    (h7 : 7 ∉ Nat.digits 10 n) : DigitsThreeOrNine n := by
  let ds := Nat.digits 10 n
  have hr := (counterexample_restrictions hpos hn h1 hdiv).1
  have ha : ∀ d ∈ ds, d = 3 ∨ d = 5 ∨ d = 9 := by
    intro d hd
    rcases hr d hd with h | h | h | h
    · exact Or.inl h
    · exact Or.inr (Or.inl h)
    · exact (h7 (h ▸ hd)).elim
    · exact Or.inr (Or.inr h)
  have h25 : ¬ 25 ∣ n := by
    have hne : ds ≠ [] := Nat.digits_ne_nil_iff_ne_zero.mpr (by omega)
    simpa only [ds, Nat.ofDigits_digits] using noTwentyFive hne ha
  have hp : ds.prod ∣ n := dvd_trans (show ds.prod ∣ ds.prod * ds.sum from ⟨_, rfl⟩) hdiv
  have h5 : 5 ∉ ds := by
    intro hmem
    have hcnt : ds.count 5 = 1 := by
      have hc : 0 < ds.count 5 := List.count_pos_iff.mpr hmem
      by_contra hn1
      have hbig : 2 ≤ ds.count 5 := by omega
      exact h25 (dvd_trans (pow_dvd_pow 5 hbig) (Stage2.fivePowCountDvd (ds := ds) hdiv))
    have hmod := residueThree ds ha
    rw [hcnt] at hmod
    have h3 : ¬ 3 ∣ n := by
      simp only [ds, Nat.ofDigits_digits] at hmod
      omega
    have hall5 : ∀ d ∈ ds, d = 5 := by
      intro d hd
      have hdn := dvd_trans (List.dvd_prod hd) hp
      rcases ha d hd with rfl | rfl | rfl
      · exact (h3 hdn).elim
      · rfl
      · exact (h3 (dvd_trans (by decide : 3 ∣ 9) hdn)).elim
    have hprod : 5 ∣ ds.prod := List.dvd_prod hmem
    have hsum := fiveDividesSum ds hall5
    exact h25 (dvd_trans (Nat.mul_dvd_mul hprod hsum) hdiv)
  intro d hd
  rcases ha d hd with h | h | h
  · exact Or.inl h
  · exact (h5 (h ▸ hd)).elim
  · exact Or.inr h

#print axioms digitsThreeOrNine_of_noSeven

end Stage5
end A398769
