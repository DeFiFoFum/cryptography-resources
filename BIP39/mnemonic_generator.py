# This simple app shows the simplicity of generating strong seed
# phrases using the BIP39 standard to unlock the power of web3.
# DISCLAIMER: For long term storage use offline, preferably on an air-gapped computer.

# Package Github
# https://github.com/trezor/python-mnemonic
# Setup
# pip/pip3 install mnemonic
# Run
# python/python3 ./mnemonic_generator.py
from mnemonic import Mnemonic


def generate_mnemonic(strength):
  # Choose the language for the mnemonic
  language = 'english'
  # Create a Mnemonic object
  mnemo = Mnemonic(language)
  return mnemo.generate(strength=strength)


# Generate a 24-word mnemonic (256 bits of entropy)
mnemonic_24_words = generate_mnemonic(256)
print("24-word mnemonic:", mnemonic_24_words)

# Generate a 12-word mnemonic (128 bits of entropy)
mnemonic_12_words = generate_mnemonic(128)
print("12-word mnemonic:", mnemonic_12_words)
