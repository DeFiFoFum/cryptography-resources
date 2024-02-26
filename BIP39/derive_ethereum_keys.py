from eth_account import Account
from eth_utils import to_checksum_address
from eth_keys import keys

# Enable unaudited HD Wallet features
Account.enable_unaudited_hdwallet_features()

# Ethereum Keys
def derive_ethereum_keys(mnemonic, account_count=10):
    keys_list = []

    for account in range(account_count):
        # Derive private key using the seed and account number
        acct = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/{account}")
        private_key = acct.key
        public_key = keys.PrivateKey(private_key).public_key

        keys_list.append({
            'account': account,
            'address': to_checksum_address(acct.address),
            'public_key': public_key.to_hex(),
            'private_key': private_key.hex(),
        })

    return keys_list

if __name__ == "__main__":
    # Example mnemonic for demonstration purposes
    example_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    derived_keys = derive_ethereum_keys(example_mnemonic)
    for key_info in derived_keys:
        print(f"Account {key_info['account']}:")
        print(f"Address: {key_info['address']}")
        print(f"Public Key: {key_info['public_key']}")
        print(f"Private Key: {key_info['private_key']}\n")
