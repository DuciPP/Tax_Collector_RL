import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor

# Create the environment
environment = Monitor(gym.make('Tax_Collector_Env', render_mode="human"))

# Create the model
model = PPO('MlpPolicy', environment, verbose=1)
model.learn(total_timesteps=1000)

# Evaluate the model
mean_reward, std_reward = evaluate_policy(model, environment, n_eval_episodes=10, render=True)
print(f"Mean Reward: {mean_reward}, Std Reward: {std_reward}")

# Close the environment
environment.close()