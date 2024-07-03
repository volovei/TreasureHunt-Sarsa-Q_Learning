import random
import gym
from gym import spaces
import numpy as np

class TreasureHuntEnv(gym.Env): # Ambiente do jogo
    def __init__(self, grid_size=10, num_treasures=5, num_traps=5, seed=1): # grid_size: O tamanho do mapa, num_treasures: O número de tesouros, num_traps: O número de armadilhas, seed: A semente do mapa
        super(TreasureHuntEnv, self).__init__() # serve para fazer um loop com a classe
        self.grid_size = grid_size 
        self.num_treasures = num_treasures - 1 #  -1 para retirar o melhor tesouro
        self.num_traps = num_traps
        self.seed_value = seed

        self.observation_space = spaces.Discrete(self.grid_size * self.grid_size) # ambiente do jogo
        self.action_space = spaces.Discrete(4) # ações do jogo
        self.state_visit_count = np.zeros((self.grid_size, self.grid_size))  # Contador de visitas a cada estado
        self.moves_since_last_treasure = 0  # Contador de movimentos desde o último tesouro

        self.reset() 

    def reset(self): # reinicia o jogo (serve para seguir tambem para o proximo episodio)
        if self.seed_value is not None: 
            np.random.seed(self.seed_value)

        self.grid = self.generate_random_grid() 
        self.agent_pos = [self.grid_size - 1, self.grid_size - 1]  # Posição inicial do agente
        self.collected_treasures = 0
        self.num_moves = 0
        self.moves_since_last_treasure = 0
        self.state_visit_count.fill(0)  # Reiniciar contador de visitas

        return self.encode_state(self.agent_pos) # retorna o estado do agente

    def encode_state(self, state): # codifica o estado do agente
        return state[0] * self.grid_size + state[1]

    def decode_state(self, state): # decodifica o estado do agente
        return [state // self.grid_size, state % self.grid_size] 

    def generate_random_grid(self): # gera um mapa aleatorio
        grid = np.full((self.grid_size, self.grid_size), 'F', dtype=str)  # 'F' representa um state chão/floor

        # Posicionar tesouros
        positions = np.random.choice(self.grid_size * self.grid_size, size=self.num_treasures + self.num_traps, replace=False) # Posições aleatórias para tesouros e armadilhas
        treasure_positions = positions[:self.num_treasures] 
        trap_positions = positions[self.num_treasures:] 

        for pos in treasure_positions: # Posicionar os tesouros
            x, y = pos // self.grid_size, pos % self.grid_size
            grid[x, y] = 'T'

        for pos in trap_positions: # Posicionar as armadilhas
            x, y = pos // self.grid_size, pos % self.grid_size
            grid[x, y] = 'H'

        # Posicionar o melhor tesouro
        pos_g = np.random.choice(self.grid_size * self.grid_size, size=1, replace=False)
        grid[pos_g // self.grid_size, pos_g % self.grid_size] = 'G'

        return grid
    
    '''
    #Função não utilizada - servia de ajuda para calcular a distância do agente ao tesouro mais próximo e assim aumentar a capacidade de o agente encontrar os tesouros mas não foi implementada no jogo final porque parecia cheats

    def distance_to_nearest_treasure(self):
        distances = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x, y] in ['T', 'G']:
                    distance = abs(self.agent_pos[0] - x) + abs(self.agent_pos[1] - y)
                    distances.append(distance)
        return min(distances) if distances else 0

    #Para episodios mais pequenas aumenta imenso a eficacia do agente 
    
    '''


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
            return self.encode_state(self.agent_pos), -80, False, self.num_moves  # Penalidade por sair fora do mapa

        self.agent_pos = [x, y]
        cell = self.grid[x, y]

        # Atualizar visitas
        self.state_visit_count[x, y] += 1

        reward = 0 

        # Aplicar penalidade por visitas repetidas
        visit_penalty = 5 * (self.state_visit_count[x, y] - 1) 
        reward -= visit_penalty
        

        '''
        INFORMAÇÃO:

        A recompensa é dada por: 
        -1 por cada movimento
        +1 por cada nova célula visitada
        -40 por cair em uma armadilha
        +20 - 0.2 * num_moves por coletar um tesouro
        +35 - 0.2 * num_moves por coletar o melhor tesouro
        -4 por passar muito tempo sem encontrar tesouros

        O 0.2 * num_moves é uma penalidade por coletar tesouros mais tarde no jogo. Quanto mais cedo o tesouro é coletado, maior a recompensa.
        
        '''


        if self.state_visit_count[x, y] == 1:
            reward += 1  # Recompensa por explorar uma nova célula

        if cell == 'H':
            reward -= 40  # Penalidade por cair em uma armadilha
        elif cell == 'T':
            self.collected_treasures += 1
            self.grid[x, y] = 'L'
            reward += 20 - 0.2 * self.num_moves  # Recompensa por coletar um tesouro
            self.moves_since_last_treasure = 0  
        elif cell == 'G':
            self.collected_treasures += 1
            self.grid[x, y] = 'R'
            reward += 35 - 0.2 * self.num_moves  # Recompensa por coletar o melhor tesouro 
            self.moves_since_last_treasure = 0  
        else:
            self.moves_since_last_treasure += 1 # Aumentar o contador de movimentos sem coletar tesouros

        # Penalidade por passar muito tempo sem encontrar tesouros
        if self.moves_since_last_treasure > 10:
            reward -= 4
            
        done = False
        if self.collected_treasures >= self.num_treasures + 1:  # +1 para contar o melhor tesouro
            done = True

        return self.encode_state(self.agent_pos), reward, done, self.num_moves # retorna o estado do agente, a recompensa, se o jogo acabou e informações adicionais (que honestamente não são usadas mas que poderiam ser usadas para futura implementação de melhorias no pós rewards)
    

