from Crypto.Hash import SHA256
from wallet import wallet
from blockchain_utils import blockchain_utils

alice = wallet()
alice.from_key = "keys/node5001/pem"
print(alice.public_key_string)
alice_string = str(alice)
data_bytes = alice_string.encode("utf-8")
data_hash = SHA256.new(data_bytes)



if __name__ == "__main__":
    print(alice_string)
    print(data_hash)