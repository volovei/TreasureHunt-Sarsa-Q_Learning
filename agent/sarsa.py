import numpy as np
import random

class SARSAAgent: 
    def __init__(self, q_table, env): # q_table: A q_table do agente, env: TreasureHuntEnv
        self.q_table = q_table
        self.env = env
        
    def next_action(self, epsilon, state): # epsilon: A probabilidade de ir para uma exploração random, state: O estado atual do agente
        if random.uniform(0, 1) < epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.q_table[state])
    
    def update_q_table(self, state, action, reward, next_state, next_action, learning_rate, discount_rate): # state: O estado atual do agente, action: A ação tomada, reward: A recompensa recebida, next_state: O próximo estado, next_action: A próxima ação, learning_rate: A probabilidade de aprender, discount_rate: A probabilidade de desconto na proxima recompensa
        self.q_table[state, action] += learning_rate * (reward + discount_rate * self.q_table[next_state, next_action] - self.q_table[state, action])

    def update_best_q_table(self, q_table): # q_table: A q_table do agente (dar update na melhor q_table entre os agentes)
        self.q_table = q_table
