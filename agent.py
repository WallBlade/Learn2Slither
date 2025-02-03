import random as rd
import json

class Agent:
    def __init__(self, sessions=100, file_path='models/default_model.json'):
        self.sessions = sessions
        self.file_path = file_path
        self.learning_rate = 0.01
        self.discount_rate = 0.95
        self.q_table = {}
        self.epsilon = 0.8
        self.min_epsilon = 0.001
        self.epsilon_decay = 0.9995

    def choose_action(self, values):
        """
        Choose an action based on the current state.
        Use an epsilon-greedy approach.
        """
        if rd.random() < self.epsilon:
            return rd.randint(0, 3)
        else:
            max_value = max(values)
            best_actions = [i for i, v in enumerate(values) if v == max_value]
            return rd.choice(best_actions)
    
    def take_action(self, state):
        """
        Take an action and return the next state and reward.
        """
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0, 0.0]

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
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def save_model(self, file_path):
        """
        Save the Q-table to a file.
        Convert tuple keys to strings for JSON serialization.
        """
        serializable_q_table = {str(k): v for k, v in self.q_table.items()}
        try:
            with open(file_path, 'w') as outfile:
                json.dump(serializable_q_table, outfile)
        except Exception as e:
            print(f"Error: {e}")

    def load_model(self, file_path):
        """
        Load the Q-table from a file.
        Convert string keys back to tuples.
        """
        try:
            with open(file_path, 'r') as infile:
                string_q_table = json.load(infile)
                # Convert string keys back to tuples
                self.q_table = {eval(k): v for k, v in string_q_table.items()}
        except Exception as e:
            self.q_table = {}
