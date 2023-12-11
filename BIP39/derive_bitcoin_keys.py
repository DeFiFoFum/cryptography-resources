from bip32utils import BIP32Key
from bip32utils import BIP32_HARDEN

def derive_bitcoin_keys(mnemonic, account_count=10):
    seed = Mnemonic.to_seed(mnemonic)
    master_key = BIP32Key.fromEntropy(seed)
    keys = []

    for account in range(account_count):
        # Derive the path for the account using BIP44
        # m / purpose' / coin_type' / account' / change / address_index
        # For Bitcoin, coin_type is 0 and we use the external chain (change=0)
        account_key = master_key.ChildKey(44 + BIP32_HARDEN) \
                                 .ChildKey(0 + BIP32_HARDEN) \
                                 .ChildKey(account + BIP32_HARDEN)
        
        # Derive the first address key pair (change=0, address_index=0)
        address_key = account_key.ChildKey(0).ChildKey(0)
        
        keys.append({
            'account': account,
            'address': address_key.Address(),
            'public_key': address_key.PublicKey().hex(),
            'private_key': address_key.WalletImportFormat(),
        })

    return keys

