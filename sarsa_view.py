import pygame
import numpy as np
import matplotlib.pyplot as plt
from environment.treasure_hunt_env import TreasureHuntEnv
from agent.sarsa import SARSAAgent 
import random

BLOCK_SIZE = 50 # o SARSA está muito fraco comparado ao Q-Learning

pygame.init()

class TreasureHuntView:
    def __init__(self, env1, env2, agent1, agent2):
        self.env1 = env1
        self.env2 = env2
        self.agent1 = agent1
        self.agent2 = agent2
        self.window_size = (self.env1.grid_size * BLOCK_SIZE * 2, self.env1.grid_size * BLOCK_SIZE)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Treasure Hunt - SARSA")

        # Carregar imagens
        self.ground_image = pygame.image.load("assets/ground.png")
        self.trap_image = pygame.image.load("assets/trap.png")
        self.small_treasure_image = pygame.image.load("assets/small_treasure.png")
        self.big_treasure_image = pygame.image.load("assets/big_treasure.png")
        self.agent_image = pygame.image.load("assets/agent.png")

        # Redimensionar imagens
        self.ground_image = pygame.transform.scale(self.ground_image, (BLOCK_SIZE, BLOCK_SIZE))
        self.trap_image = pygame.transform.scale(self.trap_image, (BLOCK_SIZE, BLOCK_SIZE))
        self.small_treasure_image = pygame.transform.scale(self.small_treasure_image, (BLOCK_SIZE, BLOCK_SIZE))
        self.big_treasure_image = pygame.transform.scale(self.big_treasure_image, (BLOCK_SIZE, BLOCK_SIZE))
        self.agent_image = pygame.transform.scale(self.agent_image, (BLOCK_SIZE, BLOCK_SIZE))

    def draw_grid(self):
        for x in range(0, self.env1.grid_size):
            for y in range(0, self.env1.grid_size):
                rect1 = pygame.Rect(y * BLOCK_SIZE, x * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                rect2 = pygame.Rect((y + self.env1.grid_size) * BLOCK_SIZE, x * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                cell1 = self.env1.grid[x, y]
                cell2 = self.env2.grid[x, y]
                
                # Desenhar ambiente 1
                if cell1 == 'S':
                    self.screen.blit(self.ground_image, rect1)
                elif cell1 == 'H':
                    self.screen.blit(self.trap_image, rect1)
                elif cell1 == 'T':
                    self.screen.blit(self.small_treasure_image, rect1)
                elif cell1 == 'G':
                    self.screen.blit(self.big_treasure_image, rect1)
                else:
                    self.screen.blit(self.ground_image, rect1)
                
                # Desenhar ambiente 2
                if cell2 == 'S':
                    self.screen.blit(self.ground_image, rect2)
                elif cell2 == 'H':
                    self.screen.blit(self.trap_image, rect2)
                elif cell2 == 'T':
                    self.screen.blit(self.small_treasure_image, rect2)
                elif cell2 == 'G':
                    self.screen.blit(self.big_treasure_image, rect2)
                else:
                    self.screen.blit(self.ground_image, rect2)
                
                pygame.draw.rect(self.screen, (0, 0, 0), rect1, 1)
                pygame.draw.rect(self.screen, (0, 0, 0), rect2, 1)

    def draw_agents(self):
        # Desenhar agente 1
        x1, y1 = self.agent1.env.agent_pos
        rect1 = pygame.Rect(y1 * BLOCK_SIZE, x1 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.screen.blit(self.agent_image, rect1)
        
        # Desenhar agente 2
        x2, y2 = self.agent2.env.agent_pos
        rect2 = pygame.Rect((y2 + self.env1.grid_size) * BLOCK_SIZE, x2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.screen.blit(self.agent_image, rect2)

    def start_episode(self, epsilon): # tentar fazer com que a função de escolha de spwan funcione
        spawns = [(9, 9), (1, 3), (7, 1), (5, 3), (4, 2)]

        best_spawn1 = (9, 9)
        best_spawn2 = (9, 9)

        if random.uniform(0, 1) < epsilon:
            best_spawn1 = random.choice(spawns)
            best_spawn2 = random.choice(spawns)
        else:
            spawn_scores1 = {}
            for spawn in spawns:
                spawn_scores1[spawn] = sum(self.agent1.q_table[spawn])

            best_spawn1 = max(spawn_scores1, key=spawn_scores1.get)

            spawn_scores2 = {}
            for spawn in spawns:
                spawn_scores2[spawn] = sum(self.agent2.q_table[spawn])

            best_spawn2 = max(spawn_scores2, key=spawn_scores2.get)


        self.env1.agent_position = best_spawn1
        self.env2.agent_position = best_spawn2
    def run(self, num_episodes=1000, max_steps_per_episode=50):
        epsilon = 0.9
        learning_rate = 0.5
        rewards_list_agent1 = []
        rewards_list_agent2 = []
        q_table_list = []
        total_reward1_sum = 0
        total_reward2_sum = 0
        Best_q_table_1 = 0
        Best_q_table_2 = 0

        for episode in range(num_episodes):
            state1 = self.env1.reset()
            state2 = self.env2.reset()
            total_reward1 = 0
            total_reward2 = 0
            done1 = False
            done2 = False

            action1 = self.agent1.next_action(epsilon, state1)
            action2 = self.agent2.next_action(epsilon, state2)

            for step in range(max_steps_per_episode):
                self.screen.fill((255, 255, 255))
                self.draw_grid()
                self.draw_agents()
                pygame.display.flip()
                if episode == num_episodes - 1:
                    pygame.time.wait(300)

                next_state1, reward1, done1, info1 = self.env1.step(action1)
                next_state2, reward2, done2, info2 = self.env2.step(action2)
                
                next_action1 = self.agent1.next_action(epsilon, next_state1)
                next_action2 = self.agent2.next_action(epsilon, next_state2)
                
                self.agent1.update_q_table(state1, action1, reward1, next_state1, next_action1, learning_rate, discount_rate=0.6)
                self.agent2.update_q_table(state2, action2, reward2, next_state2, next_action2, learning_rate, discount_rate=0.6)
                
                total_reward1 += reward1
                total_reward2 += reward2

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                state1 = next_state1
                state2 = next_state2
                action1 = next_action1
                action2 = next_action2

                if done1 or done2:
                    break 
            
            if episode > 700:
                total_reward1_sum += reward1
                total_reward2_sum += reward2

            if episode > 800:
                if episode % 50 ==0:
                    if total_reward1_sum > total_reward2_sum:
                        Best_q_table_1 += 1
                    elif total_reward1_sum < total_reward2_sum:
                        Best_q_table_2 += 1
                    else:
                        Best_q_table_1 += 1
                        Best_q_table_2 += 1

                if episode % 100 == 0:
                    if Best_q_table_1 < Best_q_table_2:
                        self.agent1.update_best_q_table(self.agent2.q_table)
                        total_reward1_sum = 0
                        total_reward2_sum = 0
                    else:
                        self.agent2.update_best_q_table(self.agent1.q_table)
                        total_reward1_sum = 0
                        total_reward2_sum = 0
                
            if episode % 100 == 0:
                q_table_list.append(self.agent1.q_table)
                if epsilon > 0 and episode > 1:
                    epsilon -= 0.1
            if learning_rate > 0.2 and episode > 1 and episode % 100 == 0:
                    learning_rate -= 0.1
            elif learning_rate <= 0.2:
                    learning_rate = 0.1

            if episode == num_episodes - 1:
                epsilon = 0

            rewards_list_agent1.append(total_reward1)
            rewards_list_agent2.append(total_reward2)

            print(f"Episódio: {episode} - Agente 1 - Total Reward: {total_reward1}")
            print(f"Episódio: {episode} - Agente 2 - Total Reward: {total_reward2}")
        print(f"Episódio: Último - Agente 1 - Total Reward: {total_reward1}")
        print(f"Episódio: Último - Agente 2 - Total Reward: {total_reward2}")

        # Plotar recompensas
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, num_episodes + 1), rewards_list_agent1, marker='o', linestyle='-', color='b', label='Agente 1')
        plt.plot(range(1, num_episodes + 1), rewards_list_agent2, marker='o', linestyle='-', color='r', label='Agente 2')
        plt.xlabel('Episódios')
        plt.ylabel('Recompensa Total')
        plt.title('Evolução das Recompensas por Episódio')
        plt.legend()
        plt.grid(True)
        plt.show()

        pygame.quit()

if __name__ == "__main__":
    seed_value = 199  # Definir uma semente para gerar o mesmo mapa para os dois agentes
    grid_size = 10 # Tamanho do grid
    num_treasures = 5 # Número de tesouros
    num_traps = 5 # Número de armadilhas

    env1 = TreasureHuntEnv(grid_size=grid_size, num_treasures=num_treasures, num_traps=num_traps, seed=seed_value)
    env2 = TreasureHuntEnv(grid_size=grid_size, num_treasures=num_treasures, num_traps=num_traps, seed=seed_value)

    
    q_table1 = np.zeros((env1.observation_space.n, env1.action_space.n))
    q_table2 = np.zeros((env2.observation_space.n, env2.action_space.n))
    
    agent1 = SARSAAgent(q_table1, env1)
    agent2 = SARSAAgent(q_table2, env2)

    view = TreasureHuntView(env1, env2, agent1, agent2)
    view.run()
