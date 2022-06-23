from proof_of_stake import proof_of_stake
from lot import lot
import string
import random

def get_random_string(length):
    letters = string.ascii_lowercase
    result_string = "".join(random.choice(letters) for i in range(length))
    return result_string


if __name__ == "__main__":
    pos = proof_of_stake()
    pos.update("bob", 100)
    pos.update("alice", 100)
    
    bob_wins = 0
    alice_wins = 0
    genesis_wins = 0
    
    for i in range(100):
        forger = pos.forger(get_random_string(i))
        if forger == "bob":
            bob_wins += 1
        elif forger == "alice":
            alice_wins += 1
        else:
            genesis_wins += 1
            
    print("bob won " + str(bob_wins) + " times")
    print("alice won " + str(alice_wins) + " times")
    print("who the fuck won " + str(genesis_wins) + " times")
    
    
    
  