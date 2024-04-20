from stable_baselines3 import PPO
import gymnasium as gym
from stable_baselines3.common.vec_env import SubprocVecEnv, VecNormalize
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from env_render_wrapper import SelectiveRenderWrapper
import time
import tax_collector_env

if __name__ == "__main__":
    
    env_id = "Tax_Collector_Env"
    num_cpu = 4
    
    
    # Create vectorized environment
    vec_env = Monitor(make_vec_env(env_id, n_envs=num_cpu, vec_env_cls=SubprocVecEnv))
    
    # Normalize vector environment
    norm_vec_env = VecNormalize(venv=vec_env)
    
    # Create and train your RL model
    model = PPO("MlpPolicy", norm_vec_env, verbose=0, tensorboard_log="./logs/tax_multiVsingle")
    
    start_time = time.time()
    model.learn(total_timesteps=200000, tb_log_name="PPO_multi", progress_bar=True)
    elapsed_time = time.time() - start_time
    
    print(f"Training time: {elapsed_time} seconds")
    
    norm_vec_env.reset()
    
    env = Monitor(gym.make(env_id, render_mode="human"))
    
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, render=True)
    print(f"Mean reward: {mean_reward}, Std reward: {std_reward}")