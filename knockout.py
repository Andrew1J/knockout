import pygame
import sys
from puck import Puck
pygame.init()
clock = pygame.time.Clock()

# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
PUCKS = []
PLAYER_ONE_TURN = True
ARROWS = []

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
    puck1 = Puck((300, 500), (1,1),(255,0,255))
    puck2 = Puck((300, 400), (1,1),(255,0,255))
    puck3 = Puck((300, 300), (1,1),(255,0,255))
    puck4 = Puck((500, 500), (1,1),(255,0,0))
    puck5 = Puck((500, 400), (1,1),(255,0,0))
    puck6 = Puck((500, 300), (1,1),(255,0,0))

    PUCKS.append(puck1)
    PUCKS.append(puck2)
    PUCKS.append(puck3)
    PUCKS.append(puck4)
    PUCKS.append(puck5)
    PUCKS.append(puck6)


def display_information():
    ''' Displays the velocities after each collision in the side bar '''
    pass


def outofbounds(coords):
    x,y = coords

    if x > (SCREEN_WIDTH / 2) + (ISLAND_WIDTH / 2) or x <  (SCREEN_WIDTH / 2) - (ISLAND_WIDTH / 2):
        return True

    if y > (SCREEN_HEIGHT / 2) + (ISLAND_HEIGHT / 2) or y <  (SCREEN_HEIGHT / 2) - (ISLAND_HEIGHT/ 2):
        return True

    return False

def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def magnitude(v):
    return (v[0]**2 + v[1]**2)**0.5

def subtract_vectors(v1,v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def main():
    ''' Main Function'''

    DRAW_ARROW_STATE = True

    # Set up the level
    setup_lvl1()

    DRAW_ARROW_STATE = True

    # MAIN GAME LOOP
    running = True
    while running:
        clock.tick(60)

        if DRAW_ARROW_STATE:

            # Main Event Handling
            for event in pygame.event.get():

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT: # Check for game quit()
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
                        if not outofbounds(pos2) and not puck.hasLine:
                            pygame.draw.line(SCREEN, (0,0,0), puck.get_pos(), pos2)
                            ARROWS.append((puck.get_pos(), pos2))
                            puck.hasLine = True
                        puck.click()

                    print(ARROWS)

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_a): # Check for game quit()
                    DRAW_ARROW_STATE = False
        else:
            # Check for collisions after shooting the pucks
            # Draw Water
            SCREEN.fill((0, 0, 255))

            # Draw Island
            pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

            for i in range(len(PUCKS)):
                for j in range(i+1, len(PUCKS)):
                    if PUCKS[i].col_circle(PUCKS[j].position):
                        vx1i = PUCKS[i].velocity[0]
                        vx2i = PUCKS[j].velocity[0]
                        vy1i = PUCKS[i].velocity[1]
                        vy2i = PUCKS[j].velocity[1]
                        m1 = PUCKS[i].mass
                        m2 = PUCKS[j].mass
                        x1,y1 = PUCKS[i].position
                        x2,y2 = PUCKS[j].position

                        const1 = ((2*m2) / (m1 + m2)) * (dot_product([vx1i-vx2i, vy1i-vy2i], [x1-x2, y1-y2]) / magnitude([x1-x2, y1-y2])**0.5)
                        vx1f = subtract_vectors(vx1i, [element * const1 for element in [x1-x2, y1-y2]])

                        const2 = ((2*m1) / (m1 + m2)) * (dot_product([vx2i-vx1i, vy2i-vy1i], [x2-x1, y2-y1]) / magnitude([x2-x1, y2-y1])**0.5)
                        vx2f = subtract_vectors(vx1i, [element * const2 for element in [x2-x1, y2-y1]])

                        const3 = ((2*m2) / (m1 + m2)) * (dot_product([vy1i-vy2i, vx1i-vx2i], [x1-x2, y1-y2]) / magnitude([x1-x2, y1-y2])**0.5)
                        vy1f = subtract_vectors(vx1i, [element * const3 for element in [x1-x2, y1-y2]])

                        const4 = ((2*m1) / (m1 + m2)) * (dot_product([vy2i-vy1i, vx2i-vx1i], [x2-x1, y2-y1]) / magnitude([x2-x1, y2-y1])**0.5)
                        vy2f = subtract_vectors(vx1i, [element * const4 for element in [x2-x1, y2-y1]])

                        PUCKS[i].velocity = (vx1f, vy1f)
                        PUCKS[j].velocity = (vx2f, vy2f)

            for puck in PUCKS:
                puck.move()

        # Draw Pucks To Screen
        for puck in PUCKS:
            puck.draw(SCREEN)

        # Flip / Update the Display
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
