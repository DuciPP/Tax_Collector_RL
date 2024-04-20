import gymnasium as gym

class LunarWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
    
    def step(self, action):
        # Implement your reward modification logic here
        # For example:
        observation, reward, done, info = self.env.step(action)
        reward -= 1  # Example: Subtracting 1 from the reward
        return observation, reward, done, info

class CustomLunarLander(gym.Wrapper):  # Corrected inheritance
    def __init__(self, **kwargs):
        super().__init__(gym.make("LunarLander-v2", **kwargs))
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        return self.env.reset()

    def render(self, mode='human', **kwargs):
        return self.env.render(mode=mode, **kwargs)

    def close(self):
        self.env.close()

    def seed(self, seed=None):
        self.env.seed(seed)

# Register the environment
gym.register(
    id='CustomLunarLander',
    entry_point='lunar_wrapper:CustomLunarLander',  # Update with the correct module name
    metadata={'render_mode': ['human', 'rgb_array']},
)