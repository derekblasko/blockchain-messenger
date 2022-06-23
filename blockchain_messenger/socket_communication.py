from p2pnetwork.node import Node
from peer_discovery_handler import peer_discovery_handler
from socket_connector import socket_connector
from blockchain_utils import blockchain_utils
import json

class socket_communication(Node):
    
    def __init__(self, ip, port):
        super(socket_communication, self).__init__(ip, port, None)
        self.peers = []
        self.Peer_discovery_handler = peer_discovery_handler(self)
        self.Socket_connector = socket_connector(ip, port)
        
    def connect_to_peer(self, peer, peer_port):
        self.connect_with_node(peer, peer_port)
        
    def start_socket_communication(self, node, peer, peer_port):
        self.node = node
        self.start()
        self.Peer_discovery_handler.start()
        self.connect_to_peer(peer, peer_port)
        
    def inbound_node_connected(self, connected_node):
        self.Peer_discovery_handler.handshake(connected_node)
        
    def outbound_node_connected(self, connected_node):
        self.Peer_discovery_handler.handshake(connected_node)
        
    def node_message(self, connected_node, message):
        message = blockchain_utils.decode(json.dumps(message))
        if message.message_type == "DISCOVERY":
            self.Peer_discovery_handler.handle_message(message)
        elif message.message_type == "TRANSACTION":
            transaction = message.data
            self.node.handle_transaction(transaction)
        elif message.message_type == "BLOCK":
            block = message.data
            self.node.handle_block(block)
        elif message.message_type == "BLOCKCHAINREQUEST":
            self.node.handle_blockchain_request(connected_node)
        elif message.message_type == "BLOCKCHAIN":
            blockchain = message.data
            self.node.handle_blockchain(blockchain)
            
    def send(self, receiver, message):
        self.send_to_node(receiver, message)
        
    def broadcast(self, message):
        self.send_to_nodes(message)