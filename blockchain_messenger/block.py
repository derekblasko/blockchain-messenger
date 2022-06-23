import time
import copy


class block():
    
    def __init__(self, transactions, last_hash, forger, block_count):
        self.transactions = transactions
        self.last_hash = last_hash
        self.forger = forger
        self.block_count = block_count
        self.timestamp = time.time()
        self.signature = ""
        
    @staticmethod
    def genesis():
        genesis_block = block([], "genesis_hash", "genesis", 0)
        genesis_block.timestamp = 0
        return genesis_block
        
    def toJson(self):
        data = {}
        data["last_hash"] = self.last_hash
        data["forger"] = self.forger
        data["block_count"] = self.block_count
        data["timestamp"] = self.timestamp
        data["signature"] = self.signature
        json_transactions = []
        for transaction in self.transactions:
            json_transactions.append(transaction.toJson())
        data["transactions"] = json_transactions
        return data
        
    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation["signature"] = ""
        return json_representation
        
    def sign(self, signature):
        self.signature = signature
    
    