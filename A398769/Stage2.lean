import A398769.Stage4
import Mathlib.Algebra.BigOperators.Group.List.Lemmas
import Mathlib.Algebra.Ring.Parity

/-! Necessary restrictions on the decimal digits of a counterexample to A398769. -/

namespace A398769
namespace Stage2


private theorem oddOfDvdOdd {d n : ℕ} (hd : d ∣ n) (hn : n % 2 = 1) :
    d % 2 = 1 := by
  by_cases h : d % 2 = 1
  · exact h
  · have h2d : 2 ∣ d := by omega
    have h2n : 2 ∣ n := Nat.dvd_trans h2d hd
    omega

private theorem sumParityOfOddDigits (ds : List ℕ)
    (ho : ∀ d ∈ ds, d % 2 = 1) :
    ds.sum % 2 = ds.length % 2 := by
  induction ds with
  | nil => rfl
  | cons d ds ih =>
      have hd : d % 2 = 1 := ho d (by simp)
      have ht : ∀ x ∈ ds, x % 2 = 1 := fun x hx => ho x (by simp [hx])
      have hi := ih ht
      simp only [List.sum_cons, List.length_cons]
      omega

/-- Every 5 contributes one factor 5 to the product, with multiplicity. -/
theorem fivePowCountDvdProd (ds : List ℕ) : 5 ^ ds.count 5 ∣ ds.prod := by
  induction ds with
  | nil => simp
  | cons d ds ih =>
      obtain ⟨k, hk⟩ := ih
      by_cases hd : d = 5
      · subst d
        refine ⟨k, ?_⟩
        simp only [List.prod_cons, List.count_cons_self, hk, Nat.pow_succ]
        ac_rfl
      · refine ⟨d * k, ?_⟩
        simp only [List.prod_cons, List.count_cons_of_ne hd, hk]
        ac_rfl

/-- From the full product-times-sum condition every power from the 5s divides n. -/
theorem fivePowCountDvd {ds : List ℕ} {n : ℕ} (hdiv : ds.prod * ds.sum ∣ n) :
    5 ^ ds.count 5 ∣ n :=
  Nat.dvd_trans (fivePowCountDvdProd ds) (Nat.dvd_trans (show ds.prod ∣ ds.prod * ds.sum from
    ⟨ds.sum, rfl⟩) hdiv)

/-- Restrictions for an odd counterexample with any list of bounded decimal digits. -/
theorem digitRestrictions {ds : List ℕ} {n : ℕ} (hn : n % 2 = 1)
    (hno : 1 ∉ ds) (hlt : ∀ d ∈ ds, d < 10) (hdiv : ds.prod * ds.sum ∣ n) :
    (∀ d ∈ ds, d = 3 ∨ d = 5 ∨ d = 7 ∨ d = 9) ∧ ds.length % 2 = 1 := by
  have hp : ds.prod ∣ n := Nat.dvd_trans (show ds.prod ∣ ds.prod * ds.sum from
    ⟨ds.sum, rfl⟩) hdiv
  have hs : ds.sum ∣ n := Nat.dvd_trans (show ds.sum ∣ ds.prod * ds.sum from
    ⟨ds.prod, Nat.mul_comm _ _⟩) hdiv
  have ho : ∀ d ∈ ds, d % 2 = 1 :=
    fun _ hd => oddOfDvdOdd (Nat.dvd_trans (List.dvd_prod hd) hp) hn
  constructor
  · intro d hd
    have hbound := hlt d hd
    have hodd := ho d hd
    have hne : d ≠ 1 := fun he => hno (he ▸ hd)
    omega
  · exact (sumParityOfOddDigits ds ho).symm.trans (oddOfDvdOdd hs hn)

/-- Check all `places` low decimal positions, including any leading zero
in the fixed-width suffix. -/
private def allowedLowPlaces : ℕ → ℕ → Bool
  | 0, _ => true
  | k + 1, n =>
      decide (n % 10 = 3 ∨ n % 10 = 5 ∨ n % 10 = 7 ∨ n % 10 = 9) &&
        allowedLowPlaces k (n / 10)

private theorem allowedLowPlaces_ofDigits (ds : List ℕ)
    (h : ∀ d ∈ ds, d = 3 ∨ d = 5 ∨ d = 7 ∨ d = 9) :
    allowedLowPlaces ds.length (Nat.ofDigits 10 ds) = true := by
  induction ds with
  | nil => rfl
  | cons d ds ih =>
      have hd := h d (by simp)
      have ht : ∀ x ∈ ds, x = 3 ∨ x = 5 ∨ x = 7 ∨ x = 9 := by
        intro x hx
        exact h x (List.mem_cons_of_mem d hx)
      have hlt : d < 10 := by omega
      have hm : (d + 10 * Nat.ofDigits 10 ds) % 10 = d := by omega
      have hq : (d + 10 * Nat.ofDigits 10 ds) / 10 = Nat.ofDigits 10 ds := by omega
      simp only [List.length_cons, Nat.ofDigits_cons, allowedLowPlaces, hm, hq]
      simp [hd, ih ht]

-- 10^9 / 5^9 = 512. This is a finite kernel computation of exact decimal
-- digits, over the complete set of multiples modulo 10^9.
set_option maxRecDepth 8192 in
set_option maxHeartbeats 4000000 in
private theorem no_allowed_nine_place_multiple :
    ∀ i : Fin 512, allowedLowPlaces 9 (1953125 * i.val) = false := by decide

/-- A nine-place decimal suffix over {3,5,7,9} cannot be divisible by 5^9. -/
theorem nine_place_suffix_excludes_five_pow_nine {n : ℕ}
    (hlen : 9 ≤ (Nat.digits 10 n).length)
    (hdigits : ∀ d ∈ Nat.digits 10 n, d = 3 ∨ d = 5 ∨ d = 7 ∨ d = 9)
    (hpow : 5 ^ 9 ∣ n) : False := by
  let ds := Nat.digits 10 n
  have subvalid : ∀ d ∈ ds.take 9, d = 3 ∨ d = 5 ∨ d = 7 ∨ d = 9 :=
    fun d hd => hdigits d (List.mem_of_mem_take hd)
  have h9 : (ds.take 9).length = 9 := by
    rw [List.length_take, Nat.min_eq_left hlen]
  have hlow : n % 10 ^ 9 = Nat.ofDigits 10 (ds.take 9) :=
    Nat.self_mod_pow_eq_ofDigits_take 9 n (by decide)
  have good := allowedLowPlaces_ofDigits (ds.take 9) subvalid
  rw [h9, ← hlow] at good
  obtain ⟨q, hq⟩ := hpow
  have decomp : n % 10 ^ 9 = 1953125 * (q % 512) := by
    rw [hq]
    change (1953125 * q) % (1953125 * 512) = 1953125 * (q % 512)
    exact Nat.mul_mod_mul_left _ _ _
  rw [decomp] at good
  have bad := no_allowed_nine_place_multiple ⟨q % 512, Nat.mod_lt _ (by decide)⟩
  change allowedLowPlaces 9 (1953125 * (q % 512)) = false at bad
  rw [good] at bad
  contradiction

end Stage2

/-- Necessary digit restrictions for a counterexample to the conjecture in A398769. -/
theorem counterexample_restrictions {n : ℕ} (_hpos : 0 < n) (hn : Odd n)
    (hno : 1 ∉ Nat.digits 10 n) (hdiv : digitProduct n * digitSum n ∣ n) :
    (∀ d ∈ Nat.digits 10 n, d = 3 ∨ d = 5 ∨ d = 7 ∨ d = 9) ∧
      Odd (digitLength n) ∧ (Nat.digits 10 n).count 5 ≤ 8 := by
  obtain ⟨hdigits, hlength⟩ := Stage2.digitRestrictions (Nat.odd_iff.mp hn) hno
    (fun _ hd => Nat.digits_lt_base (by decide) hd) hdiv
  refine ⟨hdigits, Nat.odd_iff.mpr hlength, ?_⟩
  by_contra! hmany
  have h9 : 9 ≤ (Nat.digits 10 n).count 5 := hmany
  have hlen : 9 ≤ (Nat.digits 10 n).length := le_trans h9 List.count_le_length
  have hpow : 5 ^ 9 ∣ n :=
    dvd_trans (pow_dvd_pow 5 h9) (Stage2.fivePowCountDvd (ds := Nat.digits 10 n) hdiv)
  exact Stage2.nine_place_suffix_excludes_five_pow_nine hlen hdigits hpow

#print axioms A398769.counterexample_restrictions

end A398769
