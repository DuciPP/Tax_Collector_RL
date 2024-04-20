from stable_baselines3 import PPO
import gymnasium as gym
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
import tax_collector_env
from env_render_wrapper import SelectiveRenderWrapper
import time

if __name__ == "__main__":
    
    env_id = "Tax_Collector_Env"
    
    env = gym.make(env_id, render_mode="human", screen_width=300, screen_height=300)

    wrapped_env = SelectiveRenderWrapper(env, render_frequency=10000, render_length=1000)
    
    # Create a single environment within DummyVecEnv directly
    dummy_env = DummyVecEnv([lambda: Monitor(wrapped_env)])

    norm_env = VecNormalize(dummy_env)
    
    # Create and train your RL model
    model = PPO("MlpPolicy", norm_env, verbose=0, tensorboard_log="./logs/tax_multiVsingle")

    # Time the training process
    start_time = time.time()
    model.learn(total_timesteps=100000, tb_log_name="PPO_single", progress_bar=True)
    elapsed_time = time.time() - start_time

    print(f"Training completed in {elapsed_time} seconds")

    # Reset the environment after training
    norm_env.reset()
    
    norm_env_2 = VecNormalize(DummyVecEnv([lambda: Monitor(env)]))
    
    # Evaluate the policy
    mean_reward, std_reward = evaluate_policy(model, norm_env_2, n_eval_episodes=10, render=True)
    print(f"Mean reward: {mean_reward}, Std reward: {std_reward}")