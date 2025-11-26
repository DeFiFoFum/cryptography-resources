#!/usr/bin/env python3
"""
Basic functionality tests for the cryptography tools.
Validates that core functions work correctly across platforms.
"""

import sys
from pathlib import Path

# Add BIP39 directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "BIP39"))

from mnemonic import Mnemonic


def test_mnemonic_generation():
    """Test that mnemonic generation works."""
    mnemo = Mnemonic("english")
    
    # Test 12-word generation (128 bits)
    mnemonic_12 = mnemo.generate(128)
    words_12 = mnemonic_12.split()
    assert len(words_12) == 12, f"Expected 12 words, got {len(words_12)}"
    print(f"✅ 12-word mnemonic: {len(words_12)} words generated")
    
    # Test 24-word generation (256 bits)
    mnemonic_24 = mnemo.generate(256)
    words_24 = mnemonic_24.split()
    assert len(words_24) == 24, f"Expected 24 words, got {len(words_24)}"
    print(f"✅ 24-word mnemonic: {len(words_24)} words generated")


def test_mnemonic_validation():
    """Test that generated mnemonics pass checksum validation."""
    mnemo = Mnemonic("english")
    
    for strength in [128, 160, 192, 224, 256]:
        mnemonic = mnemo.generate(strength)
        is_valid = mnemo.check(mnemonic)
        assert is_valid, f"Generated mnemonic failed checksum validation (strength={strength})"
        print(f"✅ Mnemonic checksum valid (strength={strength})")


def test_mnemonic_uniqueness():
    """Test that generated mnemonics are unique."""
    mnemo = Mnemonic("english")
    
    # Generate 100 mnemonics and check for uniqueness
    mnemonics = set()
    for i in range(100):
        m = mnemo.generate(256)
        assert m not in mnemonics, f"Duplicate mnemonic detected at iteration {i}!"
        mnemonics.add(m)
    
    print(f"✅ Generated 100 unique mnemonics")


def test_seed_derivation():
    """Test seed derivation from mnemonic."""
    mnemo = Mnemonic("english")
    
    # Test with known test vector (BIP39)
    test_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    seed = mnemo.to_seed(test_mnemonic, passphrase="")
    
    # Expected seed for this mnemonic (first 8 bytes in hex)
    expected_start = "5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4"
    actual = seed.hex()
    
    assert actual == expected_start, f"Seed derivation mismatch"
    print(f"✅ Seed derivation matches BIP39 test vector")


def test_wordlist_integrity():
    """Test that the English wordlist is intact."""
    mnemo = Mnemonic("english")
    
    assert len(mnemo.wordlist) == 2048, f"Wordlist should have 2048 words, got {len(mnemo.wordlist)}"
    
    # Check some known BIP39 words exist
    known_words = ["abandon", "zoo", "abstract", "ability", "above"]
    for word in known_words:
        assert word in mnemo.wordlist, f"Missing expected word: {word}"
    
    print(f"✅ Wordlist integrity verified (2048 words)")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🧪 Running Functionality Tests")
    print("=" * 60 + "\n")
    
    tests = [
        test_mnemonic_generation,
        test_mnemonic_validation,
        test_mnemonic_uniqueness,
        test_seed_derivation,
        test_wordlist_integrity,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: Unexpected error - {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

