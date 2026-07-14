# Cryptography Resources - Makefile
# For Mac/Linux. Windows users: use `uv run python tasks.py <command>`

.PHONY: help install install-all quick secure mnemonic eth btc solana tron substrate bittensor ledger-check test test-entropy test-all clean

# Default target
help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║          Cryptography Resources - Make Commands              ║"
	@echo "╠══════════════════════════════════════════════════════════════╣"
	@echo "║  make install      Install dependencies                      ║"
	@echo "║  make install-all  Install all deps including Solana         ║"
	@echo "║                                                              ║"
	@echo "║  Seed Generation:                                            ║"
	@echo "║  make quick        Secure seed gen (petty cash mode)         ║"
	@echo "║  make secure       Secure seed gen (cold storage mode)       ║"
	@echo "║  make mnemonic     Basic seed gen (no security features)     ║"
	@echo "║                                                              ║"
	@echo "║  Chain-Specific:                                             ║"
	@echo "║  make eth          Generate Ethereum wallet                  ║"
	@echo "║  make btc          Generate Bitcoin keys                     ║"
	@echo "║  make solana       Generate Solana keys                      ║"
	@echo "║  make tron         Generate TRON keys                        ║"
	@echo "║  make substrate    Generate Substrate/Bittensor keys         ║"
	@echo "║  make bittensor    Alias for substrate keys                  ║"
	@echo "║                                                              ║"
	@echo "║  Hardware Wallet:                                            ║"
	@echo "║  make ledger-check Verify Ledger SE attestation (Nano S Plus)║"
	@echo "║                    override: make ledger-check DEVICE=nano-x ║"
	@echo "║                                                              ║"
	@echo "║  Testing:                                                    ║"
	@echo "║  make test         Run functionality tests                   ║"
	@echo "║  make test-entropy Run entropy validation suite              ║"
	@echo "║  make test-all     Run all tests                             ║"
	@echo "║                                                              ║"
	@echo "║  make clean        Remove cached files                       ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Windows users: use 'uv run python tasks.py <command>'"
	@echo ""

# Install dependencies
install:
	uv sync

install-all:
	uv sync --all-extras

# Seed generation - SECURE (prefix with space to avoid history)
quick:
	@uv run python ./BIP39/secure_mnemonic_generate.py --quick

secure:
	@echo "⚠️  TIP: Run with leading space to avoid shell history:"
	@echo "    ' make secure'"
	@echo ""
	@uv run python ./BIP39/secure_mnemonic_generate.py --secure

# Basic mnemonic (no security features - just prints to stdout)
mnemonic:
	@uv run python ./BIP39/mnemonic_generator.py

# Chain-specific generation
eth:
	@echo "⚠️  Generating new Ethereum wallet with private keys visible"
	@echo "   Make sure to save the mnemonic and private keys securely!"
	@echo ""
	@uv run python ./BIP39/generate_eth.py true

btc:
	@uv run python ./BIP39/derive_bitcoin_keys.py

solana:
	@uv run python ./BIP39/derive_solana_keys.py

# Generate TRON keys
tron:
	@uv run python ./BIP39/derive_tron_keys.py

substrate:
	@uv run python ./BIP39/derive_substrate_keys.py

bittensor: substrate

# Hardware wallet verification
DEVICE ?= nano-s-plus
ledger-check:
	@uv run --extra ledger python ./ledger/check_genuine.py --device $(DEVICE)

# Testing
test:
	@echo "🧪 Running functionality tests..."
	@uv run python tests/test_functionality.py

test-entropy:
	@echo "🔐 Running entropy validation suite..."
	@uv run python tests/test_entropy_validation.py

test-all: test test-entropy
	@echo "✅ All tests complete"

# Utilities
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleaned cached files"
