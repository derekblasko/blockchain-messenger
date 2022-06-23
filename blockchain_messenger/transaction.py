import uuid
import time
import copy

class transaction():
    
    def __init__(self, sender_public_key, receiver_public_key, type, amount, data):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.type = type
        self.amount = amount
        self.id = (uuid.uuid1()).hex
        self.timestamp = time.time()
        self.signature = ""
        self.data = data
    
    def toJson(self):
        return self.__dict__
    
    def sign(self, signature):
        self.signature = signature
    
    def payload(self):
        json_representation = copy.deepcopy(self.toJson())
        json_representation["signature"] = ""
        return json_representation
    
    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        else:
            return False
