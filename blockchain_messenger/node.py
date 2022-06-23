from transaction_pool import transaction_pool
from wallet import wallet
from blockchain import blockchain
from socket_communication import socket_communication
from node_api import node_api
from message import message
from blockchain_utils import blockchain_utils
import copy

class node():
    
    def __init__(self, ip, port, key):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.Transaction_pool = transaction_pool()
        self.Wallet = wallet()
        self.Blockchain = blockchain()
        self.Wallet.from_key(key)

    def start_p2p(self, peer, peer_port):
        self.p2p = socket_communication(self.ip, self.port)
        self.p2p.start_socket_communication(self, peer, peer_port)
        
    def start_api(self, api_port):
        self.api = node_api()
        self.api.inject_node(self)
        self.api.start(api_port)
        
    def handle_transaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signer_public_key = transaction.sender_public_key
        signature_valid = wallet.signature_valid(data, signature, signer_public_key)
        transaction_exists = self.Transaction_pool.transaction_exists(transaction)
        transaction_in_block = self.Blockchain.transaction_exists(transaction)
        if not transaction_exists and not transaction_in_block and signature_valid:
            self.Transaction_pool.add_transaction(transaction)
            Message = message(self.p2p.Socket_connector, "TRANSACTION", transaction)
            encoded_message = blockchain_utils.encode(Message)
            self.p2p.broadcast(encoded_message)
            forging_required = self.Transaction_pool.forging_required()
            if forging_required:
                self.forge()
                
    def handle_block(self, block):
        forger = block.forger
        block_hash = block.payload()
        signature = block.signature        
        block_count_valid = self.Blockchain.block_count_valid(block)
        last_block_hash_valid = self.Blockchain.last_block_hash_valid(block)
        forger_valid = self.Blockchain.forger_valid(block)
        transactions_valid = self.Blockchain.transaction_valid(block.transactions)
        signature_valid = wallet.signature_valid(block_hash, signature, forger)
        if not block_count_valid:
            self.request_chain()
        if last_block_hash_valid and forger_valid and transactions_valid and signature_valid:
            self.Blockchain.add_block(block)
            self.Transaction_pool.remove_from_pool(block.transactions)
            Message = message(self.p2p.Socket_connector, "BLOCK", block)
            encoded_message = blockchain_utils.encode(Message)
            self.p2p.broadcast(encoded_message)
            
    def request_chain(self):
        Message = message(self.p2p.Socket_connector, "BLOCKCHAINREQUEST", None)
        encoded_message = blockchain_utils.encode(Message)
        self.p2p.broadcast(encoded_message)
        
    def handle_blockchain_request(self, requesting_node):
        Message = message(self.p2p.Socket_connector, "BLOCKCHAIN", self.Blockchain)
        encoded_message = blockchain_utils.encode(Message)
        self.p2p.broadcast(encoded_message)
        
    def handle_blockchain(self, blockchain):
        local_blockchain_copy = copy.deepcopy(self.Blockchain)
        local_block_count = len(local_blockchain_copy.blocks)
        received_chain_block_count = len(blockchain.blocks)
        if local_block_count < received_chain_block_count:
            for block_number, block in enumerate(blockchain.blocks):
                if block_number >= local_block_count:
                    local_blockchain_copy.add_block(block)
                    self.Transaction_pool.remove_from_pool(block.transactions)
            self.Blockchain = local_blockchain_copy
            
    def forge(self):    
        forger = self.Blockchain.next_forger()
        if forger == self.Wallet.public_key_string():
            print("i am the forger")
            block = self.Blockchain.create_block(self.Transaction_pool.transactions, self.Wallet)
            self.Transaction_pool.remove_from_pool(self.Transaction_pool.transactions)
            Message = message(self.p2p.Socket_connector, "BLOCK", block)
            encoded_message = blockchain_utils.encode(Message)
            self.p2p.broadcast(encoded_message)
        else:
            print("i am not the next forger")

        
            
            