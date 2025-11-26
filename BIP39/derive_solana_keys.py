from solana.keypair import Keypair
from mnemonic import Mnemonic
import hashlib
import hmac
from bip32utils import BIP32Key
from typing import List

def derive_solana_keys(mnemonic: str, account_count: int = 10) -> List[dict]:
    """Derive Solana keypairs from a mnemonic phrase."""
    keys_list = []
    
    # Generate seed from mnemonic
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic)
    
    for account in range(account_count):
        # Derive path: m/44'/501'/account'/0'
        path = f"m/44'/501'/{account}'/0'"
        
        # Generate master key and derive child key
        master_key = BIP32Key.fromEntropy(seed)
        derived_key = master_key
        
        # Follow derivation path
        for index in path.split('/')[1:]:
            if index[-1] == "'":
                # Hardened derivation
                index = int(index[:-1]) + 0x80000000
            else:
                index = int(index)
            derived_key = derived_key.ChildKey(index)
            
        # Create Solana keypair from derived private key
        private_key = derived_key.PrivateKey()
        keypair = Keypair.from_seed(private_key[:32])  # Solana uses first 32 bytes
        
        keys_list.append({
            'account': account,
            'address': str(keypair.public_key),
            'public_key': str(keypair.public_key),
            'private_key': private_key.hex(),
        })
    
    return keys_list

if __name__ == "__main__":
    # Example mnemonic for demonstration purposes
    example_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    derived_keys = derive_solana_keys(example_mnemonic)
    for key_info in derived_keys:
        print(f"Account {key_info['account']}:")
        print(f"Address: {key_info['address']}")
        print(f"Public Key: {key_info['public_key']}")
        print(f"Private Key: {key_info['private_key']}\n")
