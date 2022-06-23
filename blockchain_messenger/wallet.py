from Cryptodome.PublicKey import RSA
from transaction import transaction
from blockchain_utils import blockchain_utils
from Cryptodome.Signature import PKCS1_v1_5
from block import block


class wallet():
    
    def __init__(self):
        self.key_pair = RSA.generate(2048)
       
    def from_key(self, file):
        key = ""
        with open(file, "r") as keyfile:
            key = RSA.importKey(keyfile.read())
        self.key_pair = key
      
    def sign(self, data):
        data_hash = blockchain_utils.hash(data)
        signature_scheme_object = PKCS1_v1_5.new(self.key_pair)
        signature = signature_scheme_object.sign(data_hash)
        return signature.hex()
    
    @staticmethod
    def signature_valid(data, signature, public_key_string):
        signature = bytes.fromhex(signature)
        data_hash = blockchain_utils.hash(data)
        public_key = RSA.importKey(public_key_string)
        signature_scheme_object = PKCS1_v1_5.new(public_key)
        signature_valid = signature_scheme_object.verify(data_hash, signature)
        return signature_valid
        
    def public_key_string(self):
        public_key_string = self.key_pair.public_key().exportKey("PEM").decode("utf-8")
        return public_key_string
    
    def create_transaction(self, receiver, type, amount, data):
        Transaction = transaction(self.public_key_string(), receiver, type, amount, data)
        signature = self.sign(Transaction.payload())
        Transaction.sign(signature)
        return Transaction
    
    def create_block(self, transactions, last_hash, block_count):
        Block = block(transactions, last_hash, self.public_key_string(), block_count)
        signature = self.sign(Block.payload())
        Block.sign(signature)
        return Block