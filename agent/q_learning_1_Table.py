import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
import random

class QLearningAgent: 
    def __init__(self, q_table, env):
        self.q_table = q_table.copy()
        self.env = env
        
    def next_action(self, epsilon, state):
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.q_table[state])
      
    def choose_action(self, state, epsilon):
        return self.next_action(epsilon, state)
    
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


import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
import random

class QLearningAgent: 
    def __init__(self, q_table, env):
        self.q_table_with_treasure = q_table
        self.q_table_without_treasure = q_table
        self.env = env
        self.doenst_have_treasure = []
        
    def next_action(self, epsilon, state):
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            # Calcula a lista de vizinhos do estado atual
            neighbors = self.get_neighbors(state)
            
            # Verifica se o estado atual está entre os vizinhos dos estados sem o tesouro
            if neighbors in self.doenst_have_treasure:
                return np.argmax(self.q_table_without_treasure[state])
            else:
                return np.argmax(self.q_table_with_treasure[state])
      
    def choose_action(self, state, epsilon):
        return self.next_action(epsilon, state)
    
    def get_neighbors(self, state):
        # Retorna os vizinhos do estado atual
        neighbors = []
        state_decoded = self.env.decode_state(state)
        row, column = state_decoded[0], state_decoded[1]
        if row > 0:
            neighbors.append(self.env.encode_state([row - 1, column]))
        if row < self.env.grid_size - 1:
            neighbors.append(self.env.encode_state([row + 1, column]))
        if column > 0:
            neighbors.append(self.env.encode_state([row, column - 1]))
        if column < self.env.grid_size - 1:
            neighbors.append(self.env.encode_state([row, column + 1]))       

        return neighbors
    

    
    def update_q_table(self, state, action, reward, next_state, learning_rate, discount_rate):
        if reward > 0:
            self.q_table_without_treasure[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table_without_treasure[next_state]) - self.q_table_without_treasure[state, action])
            self.doenst_have_treasure.append(state)
        else:
            self.q_table_with_treasure[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table_with_treasure[next_state]) - self.q_table_with_treasure[state, action])
            

    def get_shortest_path(self, start_row, start_column):
        current_row, current_column = start_row, start_column
        shortest_path = [[current_row, current_column]]
        state = self.env.encode_state([current_row, current_column])
        while self.env.grid[current_row, current_column] != 'G':
            action = np.argmax(self.q_table_with_treasure[state])
            next_state, _, _, _ = self.env.step(action)
            next_state_decoded = self.env.decode_state(next_state)
            current_row, current_column = next_state_decoded[0], next_state_decoded[1]
            shortest_path.append([current_row, current_column])
            state = self.env.encode_state([current_row, current_column])
        return shortest_path

if __name__ == "__main__":
    env = TreasureHuntEnv()

import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
import random


class QLearningAgent: 
    def __init__(self, q_table, env):
        self.q_table_with_treasure = q_table
        self.q_table_without_treasure = q_table
        self.env = env
        self.doenst_have_treasure = []
        
    def next_action(self, epsilon, state):
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            if self.get_neighbors(state) in self.doenst_have_treasure:
                return np.argmax(self.q_table_without_treasure[state])
            else:
                return np.argmax(self.q_table_with_treasure[state])
      
    def choose_action(self, state, epsilon):
        return self.next_action(epsilon, state)
    
    def get_neighbors(self, state):
        neighbors = []
        state_decoded = self.env.decode_state(state)
        row, column = state_decoded[0], state_decoded[1]
        if row > 0:
            neighbors.append(self.env.encode_state([row - 1, column]))
        if row < self.env.grid_size - 1:
            neighbors.append(self.env.encode_state([row + 1, column]))
        if column > 0:
            neighbors.append(self.env.encode_state([row, column - 1]))
        if column < self.env.grid_size - 1:
            neighbors.append(self.env.encode_state([row, column + 1]))       

        return neighbors
    
    def update_q_table(self, state, action, reward, next_state, learning_rate, discount_rate):
        if self.get_neighbors(next_state) in self.doenst_have_treasure:
            self.q_table_without_treasure[state, action] += learning_rate * (-1 + discount_rate * np.max(self.q_table_without_treasure[next_state]) - self.q_table_without_treasure[state, action])
            self.q_table_with_treasure[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table_with_treasure[next_state]) - self.q_table_with_treasure[state, action])
            self.doenst_have_treasure.append(state)
        elif reward == -20 or reward == -40:
            self.q_table_without_treasure[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table_without_treasure[next_state]) - self.q_table_without_treasure[state, action])
            self.q_table_with_treasure[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table_with_treasure[next_state]) - self.q_table_with_treasure[state, action])
        else:
            self.q_table_with_treasure[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table_with_treasure[next_state]) - self.q_table_with_treasure[state, action])
            

    def get_shortest_path(self, start_row, start_column):
        current_row, current_column = start_row, start_column
        shortest_path = [[current_row, current_column]]
        state = self.env.encode_state([current_row, current_column])
        while self.env.grid[current_row, current_column] != 'G':
            action = np.argmax(self.q_table_with_treasure[state])
            next_state, _, _, _ = self.env.step(action)
            next_state_decoded = self.env.decode_state(next_state)
            current_row, current_column = next_state_decoded[0], next_state_decoded[1]
            shortest_path.append([current_row, current_column])
            state = self.env.encode_state([current_row, current_column])
        return shortest_path

if __name__ == "__main__":
    env = TreasureHuntEnv()


import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
import random
import copy

class QLearningAgent: 
    def __init__(self, q_table, env):
        self.q_table = q_table
        self.q_table_with_treasure = q_table
        self.env = env
        
    def next_action(self, epsilon, state, laststate):
        row_state, column_state = self.env.decode_state(state)
        row_laststate, column_laststate = self.env.decode_state(laststate)
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            if self.env.grid[row_state, column_state] == 'G' or self.env.grid[row_state, column_state] == 'T' or self.env.grid[row_state, column_state] == 'R':
                second = self.get_second_best_action(self.q_table, state)
                return second    
            else:
                return np.argmax(self.q_table[state])
      
    def choose_action(self, state, epsilon):
        return self.next_action(epsilon, state)
    
    def update_q_table_with_treasure(self):
        self.q_table_with_treasure = copy.deepcopy(self.q_table)
    
    def update_q_table(self, state, action, reward, next_state, learning_rate, discount_rate):
        self.q_table[state, action] += learning_rate * (reward + discount_rate * np.max(self.q_table[next_state]) - self.q_table[state, action])


    def q_value(self, state, action): #se eu quiser ver os valores de q_value em certos states
        return self.q_table[state, action]

    def get_second_best_action(self, q_table, state):
        actions = q_table[state]
        sorted_actions = np.argsort(actions)[::-1]
        second_best_action = sorted_actions[1]
        return second_best_action



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


import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
import random

class QLearningAgent: 
    def __init__(self, q_table, env):
        self.q_table = q_table
        self.q_table_1 = q_table
        self.q_table_2 = q_table
        self.q_table_3 = q_table
        self.q_table_4 = q_table
        self.last_q_table = q_table
        self.table = 1
        self.env = env
        
    def next_action(self, epsilon, state):
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            if (self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'T' or self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'G') and self.table == 1:
                return np.argmax(self.q_table_1[state])
            elif (self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'T' or self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'G') and self.table == 2:
                return np.argmax(self.q_table_2[state])
            elif (self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'T' or self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'G') and self.table == 3:
                return np.argmax(self.q_table_3[state])
            elif (self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'T' or self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'G') and self.table == 4:
                return np.argmax(self.q_table_4[state])
            elif (self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'T' or self.env.grid[self.env.decode_state(state)[0], self.env.decode_state(state)[1]] == 'G') and self.table == 5:
                return np.argmax(self.last_q_table[state])
            else:
                return np.argmax(self.q_table[state])
      
    def choose_action(self, state, epsilon):
        return self.next_action(epsilon, state)
    
    def update_q_table(self, state, action, reward, next_state, learning_rate, discount_rate):
            self.q_table[state, action] = self.q_table[state, action] + learning_rate * (reward + discount_rate * np.max(self.q_table[next_state]) - self.q_table[state, action])
            if reward >= 1 and self.table == 1:
                self.q_table_1[state, action] = self.q_table_1[state, action] + learning_rate * (reward + discount_rate * np.max(self.q_table_1[next_state]) - self.q_table_1[state, action])
                self.table = 2
            elif reward >= 1 and self.table == 2:
                self.q_table_2 = self.q_table_1
                self.q_table_2[state, action] = self.q_table_2[state, action] + learning_rate * (reward + discount_rate * np.max(self.q_table_2[next_state]) - self.q_table_2[state, action])
                self.table = 3
            elif reward >= 1 and self.table == 3:
                self.q_table_3 = self.q_table_2
                self.q_table_3[state, action] = self.q_table_3[state, action] + learning_rate * (reward + discount_rate * np.max(self.q_table_3[next_state]) - self.q_table_3[state, action])
                self.table = 4
            elif reward >= 1 and self.table == 4:
                self.q_table_4 = self.q_table_3
                self.q_table_4[state, action] = self.q_table_4[state, action] + learning_rate * (reward + discount_rate * np.max(self.q_table_4[next_state]) - self.q_table_4[state, action])
                self.table = 1
            self.last_q_table = self.q_table_4
            self.last_q_table [state, action] = self.last_q_table[state, action] + learning_rate * (reward + discount_rate * np.max(self.last_q_table[next_state]) - self.last_q_table[state, action])


    def q_value(self, state, action): #se eu quiser ver os valores de q_value em certos states
        return self.q_table[state, action]

    def get_second_best_action(self, q_table, state):
        actions = q_table[state]
        sorted_actions = np.argsort(actions)[::-1]
        second_best_action = sorted_actions[1]
        return second_best_action



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
