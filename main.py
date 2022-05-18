# Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

player = Player()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    # Draw a solid blue circle in the center
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Draw the player on the screen
    screen.blit(player.surf, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
