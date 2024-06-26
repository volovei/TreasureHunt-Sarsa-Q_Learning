import gym
from gym import spaces
import numpy as np

class TreasureHuntEnv(gym.Env):
    def __init__(self, grid_size=10, num_treasures=5, num_traps=5, seed=None):
        super(TreasureHuntEnv, self).__init__()
        self.grid_size = grid_size
        self.num_treasures = num_treasures
        self.num_traps = num_traps
        self.seed_value = seed

        self.observation_space = spaces.Discrete(self.grid_size * self.grid_size)
        self.action_space = spaces.Discrete(4)
        self.state_visit_count = np.zeros((self.grid_size, self.grid_size))  # Contador de visitas a cada estado
        self.moves_since_last_treasure = 0  # Contador de movimentos desde o último tesouro

        self.reset()

    def reset(self):
        if self.seed_value is not None:
            np.random.seed(self.seed_value)

        self.grid = self.generate_random_grid()
        self.agent_pos = [self.grid_size - 1, self.grid_size - 1]  # Posição inicial
        self.collected_treasures = 0
        self.num_moves = 0
        self.moves_since_last_treasure = 0
        self.state_visit_count.fill(0)  # Reiniciar contador de visitas

        return self.encode_state(self.agent_pos)

    def encode_state(self, state):
        return state[0] * self.grid_size + state[1]

    def decode_state(self, state):
        return [state // self.grid_size, state % self.grid_size]

    def generate_random_grid(self):
        grid = np.full((self.grid_size, self.grid_size), 'F', dtype=str) 

        # Posicionar tesouros
        positions = np.random.choice(self.grid_size * self.grid_size, size=self.num_treasures + self.num_traps, replace=False)
        treasure_positions = positions[:self.num_treasures]
        trap_positions = positions[self.num_treasures:]

        for pos in treasure_positions:
            x, y = pos // self.grid_size, pos % self.grid_size
            grid[x, y] = 'T'

        for pos in trap_positions:
            x, y = pos // self.grid_size, pos % self.grid_size
            grid[x, y] = 'H'

        # Posicionar best tesouro
        pos_g = np.random.choice(self.grid_size * self.grid_size, size=1, replace=False)
        grid[pos_g // self.grid_size, pos_g % self.grid_size] = 'G'

        return grid

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
            return self.encode_state(self.agent_pos), -80, False, {}  # Penalidade por sair fora do mapa

        self.agent_pos = [x, y]
        cell = self.grid[x, y]

        # Atualizar visitas
        self.state_visit_count[x, y] += 1

        # Penalidade inicial baseada na distância ao tesouro mais próximo
        reward = 0

        # Aplicar penalidade por visitas repetidas
        visit_penalty = 5 * (self.state_visit_count[x, y] - 1)  # Penalidade de 5 pontos por visita repetida
        reward -= visit_penalty

        if cell == 'H':
            reward -= 40  # Penalidade por cair em uma armadilha
        elif cell == 'T':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward += 20 - 0.2 * self.num_moves  # Recompensa por coletar um tesouro
            self.moves_since_last_treasure = 0  
        elif cell == 'G':
            self.collected_treasures += 1
            self.grid[x, y] = 'F'
            reward += 35 - 0.2 * self.num_moves  # Recompensa por coletar o best tesouro
            self.moves_since_last_treasure = 0  
        else:
            self.moves_since_last_treasure += 1

        # Penalidade por passar muito tempo sem encontrar tesouros
        if self.moves_since_last_treasure > 10:
            reward -= 4  # Penalidade por 10 movimentos sem encontrar tesouros

        done = False
        if self.collected_treasures >= self.num_treasures + 1:  # +1 para contar o best tesouro
            done = True

        return self.encode_state(self.agent_pos), reward, done, {}

