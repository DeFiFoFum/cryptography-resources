# BIP39 Mnemonic Generator
This simple app shows the simplicity of generating strong seed phrases using the BIP39 standard to unlock the power of web3.
https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki

DISCLAIMER: For long term storage use offline, preferably on an air-gapped computer.

Package Github
https://github.com/trezor/python-mnemonic
## Setup
```bash
# Install dependencies with uv
uv sync

# Run the mnemonic generator
uv run python ./mnemonic_generator.py
```

## Secure Generation
For more secure seed generation with auto-clearing display:
```bash
# Quick mode (petty cash / hot wallets)
uv run python ./secure_mnemonic_generate.py --quick

# Secure mode (cold storage - use air-gapped!)
uv run python ./secure_mnemonic_generate.py --secure
```