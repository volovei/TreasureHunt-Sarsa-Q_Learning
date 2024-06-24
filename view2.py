import pygame
import numpy as np
import matplotlib.pyplot as plt
from environment.treasure_hunt_env import TreasureHuntEnv
from agent.q_learning import QLearningAgent

# Tamanho dos blocos do grid
BLOCK_SIZE = 50

# Inicialização do Pygame
pygame.init()

class TreasureHuntView:
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.window_size = (self.env.grid_size * BLOCK_SIZE, self.env.grid_size * BLOCK_SIZE)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Treasure Hunt")

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
        for x in range(0, self.env.grid_size):
            for y in range(0, self.env.grid_size):
                rect = pygame.Rect(y * BLOCK_SIZE, x * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                cell = self.env.grid[x, y]
                if cell == 'S':
                    self.screen.blit(self.ground_image, rect)
                elif cell == 'H':
                    self.screen.blit(self.trap_image, rect)
                elif cell == 'T':
                    self.screen.blit(self.small_treasure_image, rect)
                elif cell == 'G':
                    self.screen.blit(self.big_treasure_image, rect)
                else:
                    self.screen.blit(self.ground_image, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw_agent(self):
        x, y = self.agent.env.agent_pos
        rect = pygame.Rect(y * BLOCK_SIZE, x * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.screen.blit(self.agent_image, rect)

    def run(self, num_episodes=500, max_steps_per_episode=33): #50 normal onde 33 é o ideal por enquanto (isto quando 500 episodios)
        epsilon = 0.9
        learning_rate = 0.5 #0.5 deu melhor
        rewards_list = []
        for episode in range(num_episodes):
            state = self.env.reset()
            total_reward = 0
            done = False

            for step in range(max_steps_per_episode):
                self.screen.fill((255, 255, 255))
                self.draw_grid()
                self.draw_agent()
                pygame.display.flip()
                if episode == num_episodes - 1:
                    pygame.time.wait(300)

                action = self.agent.next_action(epsilon, state)
                next_state, reward, done, info = self.env.step(action)
                self.agent.update_q_table(state, action, reward, next_state, learning_rate, discount_rate=0.6)
                total_reward += reward

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                state = next_state

                if done:
                    break

            if episode % 100 == 0:
                if epsilon > 0 and episode > 1:
                    epsilon -= 0.2 #-0.15 onde 0.2 deu o melhor resultado por enquanto
                if learning_rate > 0.2 and episode > 1:
                    learning_rate -= 0.1
                elif learning_rate <= 0.2:
                    learning_rate = 0.1

            if episode == num_episodes - 1:
                epsilon = 0

            rewards_list.append(total_reward)
            print(f"Episodio: {episode} - Total Reward: {total_reward}")
        print(f"Episodio: Last - Total Reward: {total_reward}")

        # Plotagem das recompensas
        plt.plot(range(1, num_episodes + 1), rewards_list, marker='o', linestyle='-', color='b', label='Rewards per Episode')
        plt.xlabel('Episodes')
        plt.ylabel('Total Reward')
        plt.title('Evolução das Recompensas por Episódio')
        plt.legend()
        plt.grid(True)
        plt.show()

        pygame.quit()

if __name__ == "__main__":
    env = TreasureHuntEnv()
    q_table = np.zeros((env.observation_space.n, env.action_space.n))
    agent = QLearningAgent(q_table, env)
    view = TreasureHuntView(env, agent)
    view.run()
