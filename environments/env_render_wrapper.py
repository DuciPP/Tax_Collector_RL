import gymnasium as gym

class SelectiveRenderWrapper(gym.Wrapper):
    def __init__(self, env, render_frequency, render_length):
        super().__init__(env)
        self.render_frequency = render_frequency
        self.render_length = render_length
        self.time_step_count = 0
        self.time_render_start = 0
        self.render = False

    def step(self, action):
        self.time_step_count += 1
        
        if self.time_step_count % self.render_frequency == 0:
            self.time_render_start = self.time_step_count
            self.render = True
            
        if self.render == True and self.time_step_count < (self.time_render_start + self.render_length):
            self.env.render()
        else:
            self.render = False
            
            
        return self.env.step(action)