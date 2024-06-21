from environment.treasure_hunt_env import TreasureHuntEnv
from agent.random_agent import RandomAgent
from view import TreasureHuntView

def run_random_agent(env, agent, num_episodes=10, max_steps_per_episode=100):
    for episode in range(num_episodes):
        state = env.reset()
        done = False
        total_reward = 0

        for step in range(max_steps_per_episode):
            action = agent.choose_action(state)
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            state = next_state

            if done:
                break

        print(f"Episode {episode + 1}: Total Reward: {total_reward}")

if __name__ == "__main__":
    env = TreasureHuntEnv()
    agent = RandomAgent(env.action_space)
    
    # Sempre iniciar a visualização
    view = TreasureHuntView(env, agent)
    view.run()
