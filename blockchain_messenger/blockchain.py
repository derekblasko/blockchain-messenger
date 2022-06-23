from block import block as Block
from blockchain_utils import blockchain_utils
from account_model import account_model
from proof_of_stake import proof_of_stake


class blockchain():
    
    def __init__(self):
        self.blocks = [Block.genesis()]
        self.account_model = account_model()
        self.pos = proof_of_stake()
    
    def add_block(self, block):
        self.execute_transactions(block.transactions)
        if self.blocks[-1].block_count < block.block_count:
            self.blocks.append(block)
    
    def toJson(self):
        data = {}
        json_blocks = []
        for block in self.blocks:
            json_blocks.append(block.toJson())
        data["blocks"] = json_blocks
        return data
    
    def block_count_valid(self, block):
        if self.blocks[-1].block_count == block.block_count - 1:
            return True
        else:
            return False
        
    def last_block_hash_valid(self, block):
        latest_blockchain_block_hash = blockchain_utils.hash(self.blocks[-1].payload()).hexdigest()
        if latest_blockchain_block_hash == block.last_hash:
            return True
        else:
            return False
        
    def get_covered_transaction_set(self, transactions):
        covered_transactions = []
        for transaction in transactions:
            if self.transaction_covered(transaction):
                covered_transactions.append(transaction)
        return covered_transactions
    
    def transaction_covered(self, transaction):
        if transaction.type == "EXCHANGE" :
            return True
        sender_balance = self.account_model.get_balance(transaction.sender_public_key)
        if sender_balance >= transaction.amount:
            return True
        else:
            return False
    
    def execute_transactions(self, transactions):
        for transaction in transactions:
            self.execute_transaction(transaction)
        
    def execute_transaction(self, transaction):
        if transaction.type == "POST":
            sender = transaction.sender_public_key
            receiver = transaction.receiver_public_key
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, 0)
                self.account_model.update_balance(sender, -amount)
        
    def next_forger(self):
        last_block_hash = blockchain_utils.hash(self.blocks[-1].payload()).hexdigest()
        next_forger = self.pos.forger(last_block_hash)
        return next_forger
    
    def create_block(self, transaction_from_pool, forger_wallet):
        covered_transactions = self.get_covered_transaction_set(transaction_from_pool)
        self.execute_transactions(covered_transactions)
        new_block = forger_wallet.create_block(covered_transactions, blockchain_utils.hash(self.blocks[-1].payload()).hexdigest(), len(self.blocks))
        self.blocks.append(new_block)
        return new_block
    
    def transaction_exists(self, transaction):
        for block in self.blocks:
            for block_transaction in block.transactions:
                if transaction.equals(block_transaction):
                    return True
        return False
    
    def forger_valid(self, block):
        forger_public_key = self.pos.forger(block.last_hash)
        proposed_block_forger = block.forger
        if forger_public_key == proposed_block_forger:
            return True
        else:
            return False
        
    def transaction_valid(self, transactions):
        covered_transactions = self.get_covered_transaction_set(transactions)
        if len(covered_transactions) == len(transactions):
            return True
        return False