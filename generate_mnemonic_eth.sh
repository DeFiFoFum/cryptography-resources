#!/bin/bash

# Make the script executable
# chmod +x generate_mnemonic_eth.sh


# Run the mnemonic generator and capture the output
show_keys=true
output=$(python3 ./BIP39/generate_eth.py $show_keys)

# Print the output
echo "$output"
