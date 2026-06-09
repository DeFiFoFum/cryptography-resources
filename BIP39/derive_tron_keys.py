import hashlib

from eth_account import Account
from eth_keys import keys

# Enable unaudited HD Wallet features
Account.enable_unaudited_hdwallet_features()

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58check_encode(payload: bytes) -> str:
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    data = payload + checksum
    num = int.from_bytes(data, "big")
    encoded = ""
    while num > 0:
        num, rem = divmod(num, 58)
        encoded = BASE58_ALPHABET[rem] + encoded
    # Preserve leading zero bytes
    for byte in data:
        if byte == 0:
            encoded = BASE58_ALPHABET[0] + encoded
        else:
            break
    return encoded


def eth_address_to_tron(address_bytes: bytes) -> str:
    # TRON addresses are the 20-byte Ethereum-style address with a 0x41
    # version prefix, Base58Check encoded (always starts with 'T')
    return base58check_encode(b"\x41" + address_bytes)


# TRON Keys (BIP44 coin type 195)
def derive_tron_keys(mnemonic, account_count=10):
    keys_list = []

    for account in range(account_count):
        acct = Account.from_mnemonic(mnemonic, account_path=f"m/44'/195'/0'/0/{account}")
        private_key = acct.key
        public_key = keys.PrivateKey(private_key).public_key

        keys_list.append({
            'account': account,
            'address': eth_address_to_tron(bytes.fromhex(acct.address[2:])),
            'public_key': public_key.to_hex(),
            'private_key': private_key.hex(),
        })

    return keys_list


if __name__ == "__main__":
    import sys
    from mnemonic import Mnemonic

    if len(sys.argv) > 1:
        # Derive from an existing mnemonic passed as arguments
        mnemonic = " ".join(sys.argv[1:]).strip().strip('"')
        if not Mnemonic("english").check(mnemonic):
            print("❌ Invalid mnemonic (checksum failed)")
            sys.exit(1)
    else:
        # Generate a fresh 24-word mnemonic
        mnemonic = Mnemonic("english").generate(strength=256)
        print("⚠️  New wallet generated. Save this mnemonic securely!\n")

    print(f"Mnemonic: {mnemonic}\n")
    derived_keys = derive_tron_keys(mnemonic)
    for key_info in derived_keys:
        print(f"Account {key_info['account']}:")
        print(f"Address: {key_info['address']}")
        print(f"Public Key: {key_info['public_key']}")
        print(f"Private Key: {key_info['private_key']}\n")
