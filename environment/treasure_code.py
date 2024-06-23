import gym
from gym import spaces
import numpy as np

class TreasureHuntEnv(gym.Env):
    def __init__(self):
        super(TreasureHuntEnv, self).__init__()
        self.grid_size = 10
        self.observation_space = spaces.Discrete(self.grid_size * self.grid_size)
        self.action_space = spaces.Discrete(4)

        self.reset()

    def reset(self):
        self.grid = np.array([
            ['S', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
            ['F', 'H', 'F', 'F', 'F', 'T', 'F', 'F', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'T', 'F'],
            ['F', 'F', 'F', 'H', 'F', 'F', 'F', 'F', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F'],
            ['F', 'G', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'T'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'H', 'H', 'F', 'H', 'F', 'F'],
            ['T', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F']
        ])
        
        self.agent_pos = [9, 9]
        self.collected_treasures = 0
        self.num_moves = 0

        return self.encode_state(self.agent_pos)

    def encode_state(self, state):
        return state[0] * self.grid_size + state[1]

    def decode_state(self, state):
        return [state // self.grid_size, state % self.grid_size]

    def step(self, action):
        self.num_moves += 1
        x, y = self.agent_pos
        
        if action == 0:  # Esquerda
            y -= 1
        elif action == 1:  # Cima
            x -= 1
        elif action == 2:  # Direita
            y += 1
        elif action == 3:  # Baixo
            x += 1

        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return self.encode_state(self.agent_pos), -40, True, {}

        self.agent_pos = [x, y]
        cell = self.grid[x, y]

        if cell == 'H':
            return self.encode_state(self.agent_pos), -20, True, {}
        elif cell == 'T':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward = 5
        elif cell == 'G':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward = 20
        else:
            reward = -1

        done = self.num_moves >= 60 or self.collected_treasures == 4

        return self.encode_state(self.agent_pos), reward, done, {}


import gym
from gym import spaces
import numpy as np

class TreasureHuntEnv(gym.Env):
    def __init__(self):
        super(TreasureHuntEnv, self).__init__()
        self.grid_size = 10
        self.observation_space = spaces.Discrete(self.grid_size * self.grid_size)
        self.action_space = spaces.Discrete(4)

        self.reset()

    def reset(self):
        self.grid = np.array([
            ['S', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
            ['F', 'H', 'F', 'F', 'F', 'T', 'F', 'F', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'T', 'F'],
            ['F', 'F', 'F', 'H', 'F', 'F', 'F', 'F', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F'],
            ['F', 'G', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'T'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'H', 'H', 'F', 'H', 'F', 'F'],
            ['T', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F'],
            ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'H', 'F', 'F']
        ])
        
        self.agent_pos = [9, 9]
        self.collected_treasures = 0
        self.num_moves = 0

        return self.encode_state(self.agent_pos)

    def encode_state(self, state):
        return state[0] * self.grid_size + state[1]

    def decode_state(self, state):
        return [state // self.grid_size, state % self.grid_size]

    def distance_to_nearest_treasure(self):
        distances = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x, y] in ['T', 'G']:
                    distance = abs(self.agent_pos[0] - x) + abs(self.agent_pos[1] - y)
                    distances.append(distance)
        return min(distances) if distances else 0
    
    def distance_to_nearest_treasure_gold(self):
        distances = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x, y] in ['G']:
                    distance = abs(self.agent_pos[0] - x) + abs(self.agent_pos[1] - y)
                    distances.append(distance)
        return min(distances) if distances else 0

    def step(self, action):
        self.num_moves += 1
        x, y = self.agent_pos
        
        if action == 0:  # Esquerda
            y -= 1
        elif action == 1:  # Cima
            x -= 1
        elif action == 2:  # Direita
            y += 1
        elif action == 3:  # Baixo
            x += 1

        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
            return self.encode_state(self.agent_pos), -40, True, {}

        self.agent_pos = [x, y]
        cell = self.grid[x, y]

        if cell == 'H':
            return self.encode_state(self.agent_pos), -20, True, {}
        elif cell == 'T':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward = 20
        elif cell == 'G':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward = 50
        else:
            reward = -self.distance_to_nearest_treasure()

        done = self.num_moves >= 60 or self.collected_treasures == 4

        return self.encode_state(self.agent_pos), reward, done, {}
