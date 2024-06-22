from environment.treasure_hunt_env import TreasureHuntEnv
from agent.random_agent import RandomAgent
from view import TreasureHuntView
from agent.q_learning import QLearningAgent



def run_random_agent(env, agent, num_episodes=100, max_steps_per_episode=100):

    for episode in range(num_episodes):
        state = env.reset()
        curremt_row, current_column = state[0], state[1]
        epsilon = 0.9
        learning_rate = 0.1
        done = False
        total_reward = 0

        for step in range(max_steps_per_episode):
            action = agent.next_action(curremt_row, current_column, epsilon)
            next_state, reward, done, info = env.step(action)
            agent.update_q_table(state, action, reward, next_state, learning_rate, epsilon)
            if step % 20 == 0:
                epsilon -= 0.2
                learning_rate += 0.2
            total_reward += reward
            state = next_state


            

        print(f"Episode {episode + 1}: Total Reward: {total_reward}")

if __name__ == "__main__":
    env = TreasureHuntEnv()
    agent = QLearningAgent(env.action_space, env.observation_space, env.grid_size)
    
    # Sempre iniciar a visualização
    view = TreasureHuntView(env, agent)
    view.run()
