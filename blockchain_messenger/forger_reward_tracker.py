
class forger_reward_tracker():
    
    def __init__(self):
        self.forger_rewards = {}
        self.balance = 0
    
    def reward_tracker(self, forger, reward):
        if forger != "null":
            if reward != "null":
                for i in self.forger_rewards:
                    if forger.public_key_string() != i:
                        self.forger_rewards = self.forger_rewards[forger.public_key_string()] = (self.balance + reward)
                        return self.forger_rewards
                    new_rewards = self.forger_rewards[self.balance].append(self.balance + reward)
                    return self.forger_rewards[self.balance].append(self.balance + reward)
        return new_rewards