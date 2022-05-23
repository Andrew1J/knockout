import pygame
import sys
from puck import Puck
pygame.init()


# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
PUCKS = pygame.sprite.Group()


# Defines a class for the shooting arrow
class Arrow(object):
    def __init__(self):
        self.position = (250,250)
        self.color = (255,0,255)
        pass

    def draw(self,surf):
        pass


# Set Up Levels
def setup_lvl1():
    ''' Sets up screen for level 1'''

    # Draw Water
    SCREEN.fill((0, 0, 255))

    # Draw Island
    pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

    # Draw Pucks
    puck1 = Puck((300, 500), (255,0,255))
    puck2 = Puck((300, 400), (255,0,255))
    puck3 = Puck((300, 300), (255,0,255))
    puck4 = Puck((500, 500), (255,0,0))
    puck5 = Puck((500, 400), (255,0,0))
    puck6 = Puck((500, 300), (255,0,0))

    PUCKS.add(puck1)
    PUCKS.add(puck2)
    PUCKS.add(puck3)
    PUCKS.add(puck4)
    PUCKS.add(puck5)
    PUCKS.add(puck6)


def display_information():
    ''' Displays the velocities after each collision in the side bar '''
    pass


def get_intersection(puck_pos, arrow_endpoint):
    ''' Returns the intersection between the arrow and the island border '''
    x1,y1 = puck_pos
    x2,y2 = arrow_endpoint
    

def main():
    ''' Main Function'''

    # Set up the level
    setup_lvl1()
    
    DRAW_ARROW_STATE = True

    # MAIN GAME LOOP
    running = True
    while running:

        if DRAW_ARROW_STATE:

            PLAYER_ONE_TURN = True
            ARROWS = []

            # Main Event Handling
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q: # Check for game quit()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse click
                    pos1 = pygame.mouse.get_pos()
                    clicked_sprites = [puck for puck in PUCKS if puck.col_circle(pos1)]
                    
                    for puck in clicked_sprites:
                        puck.click()

                if event.type == pygame.MOUSEBUTTONUP: # Draw arrow
                    # TODO reset arrow, store arrow magnitude + direction
                    pos2 = pygame.mouse.get_pos()

                    for puck in clicked_sprites:
                        get_intersection(puck.get_pos(), pos2)
                        pygame.draw.line(SCREEN, (0,0,0), puck.get_pos(), pos2)
                        ARROWS.append((puck.get_pos(), pos2))
                        puck.click()
        else:
            # Check for collisions after shooting the pucks

            pass

        # Draw Pucks To Screen
        for puck in PUCKS:
            puck.draw(SCREEN)

        # Flip / Update the Display
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
