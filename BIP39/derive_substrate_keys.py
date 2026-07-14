from typing import List, Optional

from bittensor_wallet import CRYPTO_ED25519, CRYPTO_SR25519, Keypair
from mnemonic import Mnemonic


def crypto_type_name(crypto_type: int) -> str:
    if crypto_type == CRYPTO_SR25519:
        return "SR25519"
    if crypto_type == CRYPTO_ED25519:
        return "ED25519"
    return str(crypto_type)


def keypair_private_key_hex(keypair: Keypair) -> Optional[str]:
    private_key = getattr(keypair, "private_key", None)
    if private_key is None:
        return None
    if isinstance(private_key, bytes):
        return private_key.hex()
    return str(private_key)


def create_substrate_keypair(uri: str, ss58_format: int) -> Keypair:
    keypair = Keypair.create_from_uri(uri, crypto_type=CRYPTO_SR25519)
    if ss58_format == keypair.ss58_format:
        return keypair

    return Keypair(
        public_key=keypair.public_key,
        private_key=getattr(keypair, "private_key", None),
        ss58_format=ss58_format,
        crypto_type=keypair.crypto_type,
    )


def derive_substrate_keys(
    mnemonic: str,
    account_count: int = 10,
    ss58_format: int = 42,
) -> List[dict]:
    """Derive Substrate/Bittensor SR25519 accounts from a mnemonic phrase."""
    keys_list = []

    for account in range(account_count):
        derivation_path = "" if account == 0 else f"//{account - 1}"
        keypair = create_substrate_keypair(f"{mnemonic}{derivation_path}", ss58_format)

        keys_list.append({
            "account": account,
            "derivation_path": derivation_path or "root",
            "address": keypair.ss58_address,
            "public_key": keypair.public_key.hex(),
            "private_key": keypair_private_key_hex(keypair),
            "crypto_type": crypto_type_name(keypair.crypto_type),
            "ss58_format": keypair.ss58_format,
        })

    return keys_list


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        mnemonic = " ".join(sys.argv[1:]).strip().strip('"')
        if not Mnemonic("english").check(mnemonic):
            print("❌ Invalid mnemonic (checksum failed)")
            sys.exit(1)
    else:
        mnemonic = Mnemonic("english").generate(strength=256)
        print("⚠️  New Substrate/Bittensor wallet generated. Save this mnemonic securely!\n")

    print(f"Mnemonic: {mnemonic}\n")
    for key_info in derive_substrate_keys(mnemonic):
        print(f"Account {key_info['account']} ({key_info['derivation_path']}):")
        print(f"Address: {key_info['address']}")
        print(f"Public Key: {key_info['public_key']}")
        if key_info["private_key"]:
            print(f"Private Key: {key_info['private_key']}")
        print(f"Crypto Type: {key_info['crypto_type']}")
        print(f"SS58 Format: {key_info['ss58_format']}\n")
