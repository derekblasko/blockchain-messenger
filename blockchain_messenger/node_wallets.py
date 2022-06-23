from wallet import wallet

class node_wallets():
    
    def __init__(self):
        self.node5001 = wallet()
        self.node5001.from_key("keys/node5001.pem")
        self.node5002 = wallet()
        self.node5002.from_key("keys/node5001.pem")
        self.node5003 = wallet()
        self.node5003.from_key("keys/node5001.pem")
        self.node5004 = wallet()
        self.node5004.from_key("keys/node5001.pem")
        