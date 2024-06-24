import gym
from gym import spaces
import numpy as np

class TreasureHuntEnv(gym.Env):
    def __init__(self):
        super(TreasureHuntEnv, self).__init__()
        self.grid_size = 10
        self.observation_space = spaces.Discrete(self.grid_size * self.grid_size)
        self.action_space = spaces.Discrete(4)
        self.max_moves = 100  # Limite de movimentos
        self.state_visit_count = np.zeros((self.grid_size, self.grid_size))  # Contador de visitas a cada estado

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
        self.state_visit_count.fill(0)  # Reiniciar contador de visitas

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
            return self.encode_state(self.agent_pos), -80, False, {}

        self.agent_pos = [x, y]
        cell = self.grid[x, y]

        # Atualizar visitas
        self.state_visit_count[x, y] += 1

        if cell == 'H':
            return self.encode_state(self.agent_pos), -40, False, {}
        elif cell == 'T':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward = 20 - 0.2 * self.num_moves  # Penalidade de tempo
        elif cell == 'G':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward = 35 - 0.2 * self.num_moves  # Penalidade de tempo
        else:
            reward = -self.distance_to_nearest_treasure()

        # Aplicar penalidade por visitas repetidas
        visit_penalty = 5 * (self.state_visit_count[x, y] - 1)
        reward -= visit_penalty

        done = False

        if self.collected_treasures >= 5:
            done = True
        elif self.num_moves >= self.max_moves:
            done = True

        return self.encode_state(self.agent_pos), reward, done, {}
