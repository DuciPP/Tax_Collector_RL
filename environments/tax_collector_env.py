import gymnasium as gym
import numpy as np
import pygame
import random

class Tax_Collector_Env(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60,}

    def __init__(self, render_mode=None, screen_width=500, screen_height=500, player_width=50, player_height=50, money_width=20, money_height=10, time_length=1000):
        super(Tax_Collector_Env, self).__init__()
        if render_mode not in self.metadata['render_modes']:
            raise ValueError(f"Invalid render mode '{render_mode}'")
        self.render_mode = render_mode

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_width = player_width
        self.player_height = player_height
        self.money_width = money_width
        self.money_height = money_height
        self.time_length = time_length
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=np.array([0, 0, 0, 0]),
                                                high=np.array([screen_width - player_width, screen_height - player_height, screen_width - money_width, screen_height - money_height]))
        self.key_to_movement = {0: (-20, 0), 1: (20, 0), 2: (0, -20), 3: (0, 20)}
        self.reset()

    def reset(self, seed=None, options=None):
        if seed:
            random.seed(seed)
            np.random.seed(seed)
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.player = self.random_position(self.player_width, self.player_height)
        self.money = self.find_new_money_position()
        self.timer = 0
        self.done = False
        self.state = np.array([self.player.x, self.player.y, self.money.x, self.money.y], dtype=np.float32)
        self.clock = pygame.time.Clock()
        return self.state, {}

    def step(self, action):
        dx, dy = self.key_to_movement[action]
        self.player.move_ip(dx, dy)
        self.player.clamp_ip(self.screen.get_rect())
        reward = 0
        if self.player.colliderect(self.money):
            reward = 1
            self.money = self.find_new_money_position()
            self.state[2:4] = self.money.x, self.money.y
        self.state[:2] = self.player.x, self.player.y
        self.timer += 1
        if self.timer == self.time_length:
            self.done = True
        return self.state, reward, self.done, False, {}

    def random_position(self, width, height):
        x = random.randint(0, self.screen_width - width)
        y = random.randint(0, self.screen_height - height)
        return pygame.Rect(x, y, width, height)

    def find_new_money_position(self):
        while True:
            new_pos = self.random_position(self.money_width, self.money_height)
            if not self.player.colliderect(new_pos):
                return new_pos

    def render(self, mode="human"):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), self.player)
        pygame.draw.rect(self.screen, (0, 255, 0), self.money)
        pygame.display.update()
        self.clock.tick(self.metadata['render_fps'])

    def close(self):
        pygame.quit()
        
gym.register(id="Tax_Collector_Env", entry_point='environments.tax_collector_env:Tax_Collector_Env')