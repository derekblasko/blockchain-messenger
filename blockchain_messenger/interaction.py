from wallet import wallet
from blockchain_utils import blockchain_utils
import requests




def mint_post(sender, receiver, type, amount, data):
    
        transaction = sender.create_transaction(receiver.public_key_string(), type, amount, data)
    
        url = "http://localhost:5000/transaction"
    
        package = {"transaction": blockchain_utils.encode(transaction)}
    
        requests.post(url, json=package)
        
        


#if __name__ == "__main__":
    
    #node5002 = wallet()
    #node5003 = wallet()
    #node5004 = wallet()
    #node5005 = wallet()
    
    
    #node5002.from_key("keys/node5002.pem")
    #node5003.from_key("keys/node5003.pem")
    #node5004.from_key("keys/node5004.pem")
    #node5005.from_key("keys/node5005.pem")
    #exchange = wallet()
    
"""print("5001")
    print(node5001.public_key_string())
    print("5002")
    print(node5002.public_key_string())
    print("5003")
    print(node5003.public_key_string())
    print("5004")
    print(node5004.public_key_string())
    
    
    
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")
    mint_post(node5001, node5001, "MINT & STAKE", "Stake from Node 5001")"""
    
    #mint_post(exchange, node5002, "EXCHANGE", 1, "1")
    #mint_post(exchange, node5003, "EXCHANGE", 1, "1")
    #mint_post(exchange, node5004, "EXCHANGE", 1, "1")
    #mint_post(exchange, node5005, "EXCHANGE", 1, "1")

"""mint_post(node5002, node5002, "MINT & STAKE", "2")
    
    mint_post(node5003, node5003, "MINT & STAKE", "3")
    
    mint_post(node5004, node5004, "MINT & STAKE", "4")
    
    mint_post(node5001, node5001, "MINT & STAKE", "5")
    
    mint_post(node5002, node5002, "MINT & STAKE", "6")
    
    mint_post(node5003, node5003, "MINT & STAKE", "7")
   
    mint_post(node5004, node5004, "MINT & STAKE", "8")
    
    mint_post(node5001, node5001, "MINT & STAKE", "9")
   
    mint_post(node5002, node5002, "MINT & STAKE", "10")
    
    mint_post(node5003, node5003, "MINT & STAKE", "11")
    
    mint_post(node5004, node5004, "MINT & STAKE", "12")
    
    mint_post(node5001, node5001, "MINT & STAKE", "13")
    
    mint_post(node5002, node5002, "MINT & STAKE", "14")
    
    mint_post(node5003, node5003, "MINT & STAKE", "15")
   
    mint_post(node5004, node5004, "MINT & STAKE", "16")"""
   
