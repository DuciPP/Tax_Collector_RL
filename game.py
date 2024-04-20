import pygame
import random

# Initialize a pygame window
pygame.init()

# Set screen size and display window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Creates the player red rectangle
player = pygame.Rect(random.randint(0, int(round(SCREEN_WIDTH/4))), 
                     random.randint(0, SCREEN_HEIGHT),
                     50, 50)


# Creates first money
money = pygame.Rect(random.randint(int(round(SCREEN_WIDTH/2)), SCREEN_WIDTH - 20), 
                    random.randint(0, SCREEN_HEIGHT - 10),
                    20, 10)
# Finds new money position
def get_new_money_position():
    return pygame.Rect(random.randint(0, SCREEN_WIDTH - 20), 
                       random.randint(0, SCREEN_HEIGHT - 10), 
                       20, 10)


# Key dictionary    
key_to_movement = {pygame.K_a: (-10, 0),
                   pygame.K_d: (10, 0),
                   pygame.K_w: (0, -10),
                   pygame.K_s: (0, 10),}
# Check that entity stays in window
def check_boundaries(entity, boundary):
    entity.clamp_ip(boundary.get_rect())
    


# Initiates clock
clock = pygame.time.Clock()

# Initiates run with True
run = True

# Initiates score
score = 0
font = pygame.font.SysFont(name='Arial', size=36)


while run:
    
    # Checks wether game is being quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Checks for key presses
    keys = pygame.key.get_pressed()
    # Moves player depending of key
    for key, (x, y) in key_to_movement.items():
        if keys[key]:
            player.move_ip(x, y)
            
    # Keeps player in bounds
    check_boundaries(entity=player, boundary=screen)
    
    # Checks wether player touches money        
    if player.colliderect(money):
        score += 1
        while True:
            new_position = get_new_money_position()
            if not player.colliderect(new_position):
                money = new_position
                break 
    
    # Resets screen
    screen.fill((0, 0, 0))
    
    # Renders the player
    pygame.draw.rect(screen, (255, 0, 0), player)
    pygame.draw.rect(screen, (0, 255, 0), money)
    
    # Initiates new score
    text_score = font.render(f'Score: {score}', True, (0, 255, 0))
    # Renders score
    screen.blit(text_score, (10, 10))
    
    # Refreshes the window
    pygame.display.update()
    
    # Set FPS to 60
    clock.tick(60)

pygame.quit()