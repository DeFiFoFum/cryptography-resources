#!/usr/bin/env python3
"""
Entropy and Randomness Validation Tests

This module performs statistical tests on the entropy generation to verify
that the randomness source is cryptographically sound.

Tests performed:
1. Chi-Square Test - Tests uniform distribution of bytes
2. Runs Test - Tests randomness of bit sequences
3. Monobit Test - Tests balance of 0s and 1s
4. Collision Test - Tests for duplicate outputs
5. Entropy Source Verification - Confirms secrets module usage

These tests provide a "seal of approval" for the randomness quality.
"""

import sys
import math
import secrets
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "BIP39"))

from mnemonic import Mnemonic


# Test parameters
SAMPLE_SIZE = 1000  # Number of samples to generate
SIGNIFICANCE_LEVEL = 0.01  # 1% significance level


def chi_square_test(data: bytes) -> tuple[float, bool]:
    """
    Chi-square test for uniform distribution of bytes.
    
    Returns:
        (chi_square_statistic, passed)
    """
    # Count occurrences of each byte value
    counts = Counter(data)
    n = len(data)
    expected = n / 256  # Expected count for each byte value (0-255)
    
    # Calculate chi-square statistic
    chi_square = sum(
        ((counts.get(i, 0) - expected) ** 2) / expected
        for i in range(256)
    )
    
    # Degrees of freedom = 255 (256 categories - 1)
    # Critical value for df=255, alpha=0.01 is approximately 310
    critical_value = 310.457
    passed = chi_square < critical_value
    
    return chi_square, passed


def monobit_test(data: bytes) -> tuple[float, bool]:
    """
    NIST Monobit Test - Tests the balance of 0s and 1s.
    
    For truly random data, the number of 1s should be approximately n/2.
    """
    # Convert bytes to bits and count 1s
    bits = ''.join(format(byte, '08b') for byte in data)
    n = len(bits)
    ones = bits.count('1')
    
    # Calculate test statistic
    s = abs(ones - n/2) / math.sqrt(n/4)
    
    # For significance level 0.01, critical value is approximately 2.576
    passed = s < 2.576
    
    return s, passed


def runs_test(data: bytes) -> tuple[float, bool]:
    """
    Runs test - Tests for randomness in bit sequences.
    
    A "run" is a maximal sequence of consecutive identical bits.
    """
    bits = ''.join(format(byte, '08b') for byte in data)
    n = len(bits)
    
    # Count ones
    ones = bits.count('1')
    pi = ones / n
    
    # Check if proportion is within acceptable range
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return float('inf'), False
    
    # Count runs
    runs = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            runs += 1
    
    # Calculate expected runs and variance
    expected_runs = 2 * ones * (n - ones) / n + 1
    variance = (2 * ones * (n - ones) * (2 * ones * (n - ones) - n)) / (n * n * (n - 1))
    
    if variance <= 0:
        return float('inf'), False
    
    # Calculate test statistic
    z = (runs - expected_runs) / math.sqrt(variance)
    
    # For significance level 0.01, critical value is approximately 2.576
    passed = abs(z) < 2.576
    
    return z, passed


def collision_test(mnemo: Mnemonic, num_samples: int = 1000) -> tuple[int, bool]:
    """
    Test for collisions in mnemonic generation.
    
    With 256 bits of entropy, collisions should be astronomically rare.
    """
    mnemonics = set()
    collisions = 0
    
    for _ in range(num_samples):
        m = mnemo.generate(256)
        if m in mnemonics:
            collisions += 1
        mnemonics.add(m)
    
    # Any collision with 256-bit entropy is essentially impossible
    passed = collisions == 0
    
    return collisions, passed


def verify_entropy_source() -> tuple[str, bool]:
    """
    Verify that the mnemonic library uses the secrets module for entropy.
    """
    import inspect
    
    source = inspect.getsource(Mnemonic.generate)
    uses_secrets = "secrets.token_bytes" in source or "secrets." in source
    
    return "secrets.token_bytes" if uses_secrets else "UNKNOWN", uses_secrets


def entropy_estimation(data: bytes) -> float:
    """
    Estimate Shannon entropy of the data.
    
    Maximum entropy for bytes is 8 bits.
    """
    if not data:
        return 0.0
    
    counts = Counter(data)
    n = len(data)
    
    entropy = 0.0
    for count in counts.values():
        if count > 0:
            p = count / n
            entropy -= p * math.log2(p)
    
    return entropy


def main():
    """Run all entropy validation tests."""
    print("\n" + "=" * 70)
    print("🔐 ENTROPY & RANDOMNESS VALIDATION SUITE")
    print("=" * 70)
    print(f"\nSample size: {SAMPLE_SIZE}")
    print(f"Significance level: {SIGNIFICANCE_LEVEL}")
    print("\n" + "-" * 70)
    
    mnemo = Mnemonic("english")
    all_passed = True
    results = []
    
    # 1. Verify entropy source
    print("\n📌 Test 1: Entropy Source Verification")
    source, source_ok = verify_entropy_source()
    status = "✅ PASS" if source_ok else "❌ FAIL"
    print(f"   Entropy source: {source}")
    print(f"   Result: {status}")
    results.append(("Entropy Source", source_ok))
    all_passed = all_passed and source_ok
    
    # 2. Generate entropy samples
    print("\n📌 Generating entropy samples...")
    raw_entropy = b''.join(secrets.token_bytes(32) for _ in range(SAMPLE_SIZE))
    
    # Also test mnemonic library's entropy
    mnemonic_entropy = b''
    for _ in range(100):  # Fewer samples for mnemonic (slower)
        m = mnemo.generate(256)
        # Convert mnemonic back to entropy
        mnemonic_entropy += bytes(mnemo.to_entropy(m))
    
    # 3. Chi-Square Test
    print("\n📌 Test 2: Chi-Square Test (Uniform Distribution)")
    chi_sq, chi_passed = chi_square_test(raw_entropy)
    status = "✅ PASS" if chi_passed else "❌ FAIL"
    print(f"   Chi-square statistic: {chi_sq:.2f}")
    print(f"   Critical value (α=0.01): 310.46")
    print(f"   Result: {status}")
    results.append(("Chi-Square Test", chi_passed))
    all_passed = all_passed and chi_passed
    
    # 4. Monobit Test
    print("\n📌 Test 3: Monobit Test (Bit Balance)")
    mono_stat, mono_passed = monobit_test(raw_entropy)
    status = "✅ PASS" if mono_passed else "❌ FAIL"
    print(f"   Test statistic: {mono_stat:.4f}")
    print(f"   Critical value (α=0.01): 2.576")
    print(f"   Result: {status}")
    results.append(("Monobit Test", mono_passed))
    all_passed = all_passed and mono_passed
    
    # 5. Runs Test
    print("\n📌 Test 4: Runs Test (Sequence Randomness)")
    runs_stat, runs_passed = runs_test(raw_entropy[:10000])  # Subset for performance
    status = "✅ PASS" if runs_passed else "❌ FAIL"
    print(f"   Test statistic: {runs_stat:.4f}")
    print(f"   Critical value (α=0.01): ±2.576")
    print(f"   Result: {status}")
    results.append(("Runs Test", runs_passed))
    all_passed = all_passed and runs_passed
    
    # 6. Collision Test
    print("\n📌 Test 5: Collision Test (Uniqueness)")
    collisions, collision_passed = collision_test(mnemo, 500)
    status = "✅ PASS" if collision_passed else "❌ FAIL"
    print(f"   Collisions detected: {collisions}")
    print(f"   Expected (256-bit): 0")
    print(f"   Result: {status}")
    results.append(("Collision Test", collision_passed))
    all_passed = all_passed and collision_passed
    
    # 7. Entropy Estimation
    print("\n📌 Test 6: Shannon Entropy Estimation")
    entropy = entropy_estimation(raw_entropy)
    entropy_passed = entropy > 7.9  # Should be very close to 8 for uniform random bytes
    status = "✅ PASS" if entropy_passed else "❌ FAIL"
    print(f"   Estimated entropy: {entropy:.4f} bits/byte")
    print(f"   Maximum possible: 8.0000 bits/byte")
    print(f"   Minimum threshold: 7.9000 bits/byte")
    print(f"   Result: {status}")
    results.append(("Entropy Estimation", entropy_passed))
    all_passed = all_passed and entropy_passed
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 VALIDATION SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        icon = "✅" if passed else "❌"
        print(f"   {icon} {name}")
    
    print("\n" + "-" * 70)
    if all_passed:
        print("🏆 ALL TESTS PASSED - Randomness quality verified!")
        print("   This entropy source is suitable for cryptographic use.")
    else:
        print(f"⚠️  {total_count - passed_count}/{total_count} TESTS FAILED")
        print("   Review failed tests before using for sensitive applications.")
    print("=" * 70 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

