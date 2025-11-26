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

def main(show_keys):
    # Generate a 24-word mnemonic (256 bits of entropy)
    mnemonic_24_words = generate_mnemonic(256)
    print("24-word mnemonic:", mnemonic_24_words)
    # show_keys=False to hide the private keys
    derive_keys_and_print(mnemonic_24_words, show_keys=show_keys)

    print("NOTE: Skipping 12-word mnemonic.")
    # # Generate a 12-word mnemonic (128 bits of entropy)
    # mnemonic_12_words = generate_mnemonic(128)
    # print("12-word mnemonic:", mnemonic_12_words)
    # # show_keys=True to display the private keys
    # derive_keys_and_print(mnemonic_12_words, show_keys=show_keys)

if __name__ == "__main__":
    """
    Usage:
        python generate_eth.py [show_keys]
    
    Arguments:
        show_keys: Optional. A boolean flag to indicate whether to show the keys.
                   Use 'true' to show keys, defaults to 'false' if not specified.
    """
    import sys
    show_keys = False  # Default to False to hide the private keys
    # Check if an argument is passed to optionally set show_keys
    if len(sys.argv) > 1:
        show_keys = sys.argv[1].lower() == 'true'
    main(show_keys)