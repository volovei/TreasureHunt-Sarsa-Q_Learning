import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
import random

class QLearningAgent: #não esta a funcionar bem, tenho de corrigir
        def __init__(self,q_table, q_values):
            self.q_table = q_table
            self.q_values = q_values           
            
        def next_action(self, current_row, current_column, epsilon):
            if random.uniform(0, 1) > epsilon:
                return np.argmax(self.q_values[current_row, current_column])
            else:
                return np.random.randint(4)
            
        def choose_action(self, current_row, current_column, epsilon):
            return self.next_action(current_row, current_column, epsilon)
        
        def starting_location(self):
            return self.env.agent_pos[0], self.env.agent_pos[1]
        
        
        def update_q_table(self, state, action, reward, next_state, learning_rate, discount_rate):
            self.q_table[state, action] = self.q_table[state, action] + learning_rate * (reward + discount_rate * np.max(self.q_table[next_state]) - self.q_table[state, action])
        
        def update_q_values(self, current_row, current_column, action, reward, next_row, next_column, learning_rate, discount_rate):    
            self.q_values[current_row, current_column, action] = self.q_values[current_row, current_column, action] + learning_rate * (reward + discount_rate * np.max(self.q_values[next_row, next_column]) - self.q_values[current_row, current_column, action])

        def get_shortest_path(self, start_row, start_column):
            current_row, current_column = start_row, start_column
            shortest_path = []
            shortest_path.append([current_row, current_column])
            while self.env.grid[current_row, current_column] != 'G':
                action = np.argmax(self.q_values[current_row, current_column])
                current_row, current_column = self.next_location(current_row, current_column, action)
                shortest_path.append([current_row, current_column])
            return shortest_path
             
            

if __name__ == "__main__":
    env = TreasureHuntEnv()