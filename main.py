# Import and initialize the pygame library
import pygame
pygame.init()

# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 300

# Set up the drawing window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Defines a class for the pucks
class Puck(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (0,0,255)

    def draw(self, surf):
        pass

# Defines a class for the shooting arrow
class Arrow(object):
    def __init__(self):
        pass

    def draw(self,surf):
        pass

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with blue
    screen.fill((0, 0, 255))

    # Draw a solid green rectangle in the center
    pygame.draw.rect(screen, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

    # Draw the puck on the screen
    puck = Puck()

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
