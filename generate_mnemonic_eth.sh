#!/bin/bash

# Make the script executable
# chmod +x generate_mnemonic_eth.sh


# Run the mnemonic generator and capture the output
output=$(python3 ./BIP39/generate_eth.py)

# Print the output
echo "$output"
