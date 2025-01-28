import random as rd

class Agent:
    def __init__(self, sessions=10, save_path='models/default_model.txt'):
        self.sessions = sessions
        self.save_path = save_path
        self.learning_rate = 0.5
        self.discount_rate = 0.99
        self.q_table = {}
        self.epsilon = 0.1
        self.epsilon_decay = 0.9999
        self.REWARDS = {
            'DEATH': -10,      # Snake dies (wall or self collision)
            'GREEN_APPLE': 10,  # Eat green apple (grow)
            'RED_APPLE': -5,   # Eat red apple (shrink)
            'CLOSER': 1,       # Move closer to green apple
            'FARTHER': -1,     # Move away from green apple
            'SURVIVE': 0.1     # Small reward for surviving each move
        }

    def choose_action(self, values):
        """
        Choose an action based on the current state.
        Use an epsilon-greedy approach.
        """
        if rd.random() < self.epsilon:
            return rd.randint(0, 3)
        else:
            return values.index(max(values))
    
    def take_action(self, state):
        """
        Take an action and return the next state and reward.
        """
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]

        print(f"Q-table: {self.q_table[state]}")

        return self.choose_action(self.q_table[state])

    def update_q_table(self, state, action, reward, new_state):
        """
        Update the Q-table based on the Q-learning formula.
        """
        if new_state not in self.q_table:
            self.q_table[new_state] = [0.0, 0.0, 0.0, 0.0]
        
        new_max = max(self.q_table[new_state])

        current_q = self.q_table[state][action]

        # Bellman equation
        new_q = current_q + self.learning_rate * (
            reward + self.discount_rate * new_max - current_q
        )
        
        # Update Q-value
        self.q_table[state][action] = new_q
        
        # Decay epsilon
        self.epsilon *= self.epsilon_decay

    def save_model(self, file_path):
        """
        Save the Q-table to a file.
        """
        pass # Implement model saving logic

    def load_model(self, file_path):
        """
        Load the Q-table from a file.
        """
        pass # Implement model loading logic
