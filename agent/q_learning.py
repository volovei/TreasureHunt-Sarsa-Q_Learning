import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
import random

class QLearningAgent:
    def __init__(self, q_table, env):
        self.q_table = q_table
        self.env = env

    def next_action(self, epsilon, state):
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.q_table[state])

    def update_q_table(self, state, action, reward, next_state, learning_rate, discount_rate):
        self.q_table[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table[next_state]) - self.q_table[state, action])

    def get_shortest_path(self, start_row, start_column):
        current_row, current_column = start_row, start_column
        shortest_path = [[current_row, current_column]]
        state = self.env.encode_state([current_row, current_column])
        
        while self.env.grid[current_row, current_column] != 'G':
            action = np.argmax(self.q_table[state])
            next_state, _, _, _ = self.env.step(action)
            next_state_decoded = self.env.decode_state(next_state)
            current_row, current_column = next_state_decoded[0], next_state_decoded[1]
            shortest_path.append([current_row, current_column])
            state = self.env.encode_state([current_row, current_column])
        
        return shortest_path

if __name__ == "__main__":
    env = TreasureHuntEnv()


    