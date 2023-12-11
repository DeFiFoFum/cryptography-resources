from mnemonic_generator import generate_mnemonic
from derive_ethereum_keys import derive_ethereum_keys  # Import the derive_keys function

def derive_keys_and_print(mnemonic, show_keys=False):
    keys = derive_ethereum_keys(mnemonic)
    for key in keys:
        print(f"Account {key['account']}: Address: {key['address']}")
        if show_keys:
            print(f"Public Key: {key['public_key']}")
            print(f"Private Key: {key['private_key']}")
        print()  # Add a newline for better readability

def main():
    # Generate a 24-word mnemonic (256 bits of entropy)
    mnemonic_24_words = generate_mnemonic(256)
    print("24-word mnemonic:", mnemonic_24_words)
    # show_keys=False to hide the private keys
    derive_keys_and_print(mnemonic_24_words, show_keys=False)

    # Generate a 12-word mnemonic (128 bits of entropy)
    mnemonic_12_words = generate_mnemonic(128)
    print("12-word mnemonic:", mnemonic_12_words)
    # show_keys=True to display the private keys
    derive_keys_and_print(mnemonic_12_words, show_keys=True)

if __name__ == "__main__":
    main()