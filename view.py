import pygame
import numpy as np
from environment.treasure_hunt_env import TreasureHuntEnv
from agent.random_agent import RandomAgent

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
        x, y = self.env.agent_pos
        rect = pygame.Rect(y * BLOCK_SIZE, x * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        self.screen.blit(self.agent_image, rect)

    def run(self, num_episodes=10, max_steps_per_episode=100):
        clock = pygame.time.Clock()

        for episode in range(num_episodes):
            state = self.env.reset()
            done = False
            total_reward = 0

            for step in range(max_steps_per_episode):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                action = self.agent.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                total_reward += reward
                state = next_state

                self.screen.fill((255, 255, 255))
                self.draw_grid()
                self.draw_agent()
                pygame.display.flip()

                clock.tick(5)

                if done:
                    break

            print(f"Episode {episode + 1}: Total Reward: {total_reward}")

        pygame.quit()

if __name__ == "__main__":
    env = TreasureHuntEnv()
    agent = RandomAgent(env.action_space)
    view = TreasureHuntView(env, agent)
    view.run()