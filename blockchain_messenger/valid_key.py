import hashlib



class valid_key():
    
    def __init__(self, key):
        self.key = hashlib.sha256(((key).encode("utf-8"))).hexdigest()
        
    def is_key_valid(self, key):
        key_hash = hashlib.sha256(((key).encode("utf-8"))).hexdigest()
        if key_hash == self.key:
            return True
        else:
            return False