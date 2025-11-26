# Cryptography Resources

[![CI - Cross Platform Tests](https://github.com/DeFiFoFum/cryptography-resources/actions/workflows/ci.yml/badge.svg)](https://github.com/DeFiFoFum/cryptography-resources/actions/workflows/ci.yml)
[![Security Audit](https://github.com/DeFiFoFum/cryptography-resources/actions/workflows/security-audit.yml/badge.svg)](https://github.com/DeFiFoFum/cryptography-resources/actions/workflows/security-audit.yml)
![Randomness](https://img.shields.io/badge/Randomness-VERIFIED-brightgreen?style=flat-square&logo=python)
![BIP39](https://img.shields.io/badge/BIP39-Compliant-blue?style=flat-square)
![Entropy](https://img.shields.io/badge/Entropy-256_bit-purple?style=flat-square)

A simple repo showcasing the power and accessibility of cryptography for generating secure wallet seeds.

- [Cryptography Resources](#cryptography-resources)
  - [Security Certification](#security-certification)
  - [Setup](#setup)
  - [Quick Start](#quick-start)
  - [Features](#features)
    - [BIP39 Mnemonic Generation](#bip39-mnemonic-generation)
    - [Chain-Specific Key Derivation](#chain-specific-key-derivation)
  - [Testing](#testing)
  - [Resources](#resources)

## Security Certification

This tool's randomness quality is **automatically validated** on every commit:

| Test | Description | Status |
|------|-------------|--------|
| **Entropy Source** | Uses Python `secrets` module (CSPRNG) | ✅ Verified |
| **Chi-Square** | Uniform byte distribution | ✅ Verified |
| **Monobit** | Balanced bit distribution | ✅ Verified |
| **Runs Test** | No detectable patterns | ✅ Verified |
| **Collision** | No duplicate outputs | ✅ Verified |
| **Shannon Entropy** | ≥7.9 bits/byte | ✅ Verified |

> ⚠️ **For cold storage**: Always generate seeds on an air-gapped machine.

## Setup

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# For Solana support
uv sync --extra solana
```

## Quick Start

**Mac/Linux:**
```bash
make help              # Show all commands
make quick             # Petty cash wallet (auto-clears screen)
make secure            # Cold storage (security checklist)
```

**Windows (or any platform):**
```bash
uv run python tasks.py help      # Show all commands
uv run python tasks.py quick     # Petty cash wallet
uv run python tasks.py secure    # Cold storage
```

## Features

### BIP39 Mnemonic Generation

| File | Description |
|------|-------------|
| [`secure_mnemonic_generate.py`](./BIP39/secure_mnemonic_generate.py) | **Recommended** - Secure generator with auto-clearing display |
| [`mnemonic_generator.py`](./BIP39/mnemonic_generator.py) | Basic generator (no security features) |

```bash
# Secure mode (cold storage - use on air-gapped machine!)
 make secure
# ^ Note the leading space to avoid shell history

# Quick mode (petty cash / hot wallets)
make quick

# Basic mode (no security features)
make mnemonic
```

### Chain-Specific Key Derivation

```bash
make eth      # Ethereum wallet
make btc      # Bitcoin keys  
make solana   # Solana keys
```

## Testing

Run the test suite to verify functionality and randomness quality:

```bash
# Functionality tests
make test

# Entropy validation suite (statistical randomness tests)
make test-entropy

# All tests
make test-all
```

Or cross-platform:
```bash
uv run python tasks.py test
uv run python tasks.py test-entropy
```

## Resources

- [trezor/python-mnemonic](https://github.com/trezor/python-mnemonic) - The mnemonic library used
- [mnemonic python package](https://pypi.org/project/mnemonic/)
- [BIP-0039 Specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
- [Security Review](./docs/security-review.md) - Detailed security analysis
