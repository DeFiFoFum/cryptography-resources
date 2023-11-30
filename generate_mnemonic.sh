#!/bin/bash

# Make the script executable
# chmod +x generate_mnemonic.sh


# Run the mnemonic generator and capture the output
output=$(python3 ./BIP39/mnemonic_generator.py)

# Print the output
echo "$output"
