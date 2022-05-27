import pygame
import sys
from puck import Puck
import math
pygame.init()
clock = pygame.time.Clock()

# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
PUCKS = []
PLAYER_ONE_TURN = True
ARROWS = []
GRAVITY = -2
mu = 0.5

# Set Up Levels
def setup_lvl1():
    ''' Sets up screen for level 1'''

    # Draw Water
    SCREEN.fill((0, 0, 255))

    # Draw Island
    pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

    # Draw Pucks
    puck1 = Puck((300, 500), (0,0),(255,0,255), 1)
    puck2 = Puck((300, 400), (0,0),(255,0,255), 1)
    puck3 = Puck((300, 300), (0,0),(255,0,255), 1)
    puck4 = Puck((500, 500), (0,0),(255,0,0), 1)
    puck5 = Puck((500, 400), (0,0),(255,0,0), 1)
    puck6 = Puck((500, 300), (0,0),(255,0,0), 1)

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
    return (v[0]*v[0] + v[1]*v[1])

def subtract_vectors(v1,v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def get_angle_of_motion(v1,v2):
    return math.atan(v2/(v1+.000001))

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
                            ARROWS.append((puck.get_pos(),(pos2[0]-puck.get_pos()[0], pos2[1] - puck.get_pos()[1])))
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

            # FOR TESTING PURPOSES
            for i in range(len(PUCKS)):
                x,y = PUCKS[i].position

                ''' PUCK GETS REMOVED WHEN ITS OVER THE BORDER '''
                if x >= (SCREEN_WIDTH / 2) + (ISLAND_WIDTH / 2) - PUCKS[i].radius or x <  (SCREEN_WIDTH / 2) - (ISLAND_WIDTH / 2) + PUCKS[i].radius:
                    # PUCKS[i].velocity = (-PUCKS[i].velocity[0], PUCKS[i].velocity[1])
                    PUCKS[i].position = (-1,-1)
                    PUCKS[i].velocity = (0,0)
                    PUCKS[i].onIsland = False
                if y >= (SCREEN_HEIGHT / 2) + (ISLAND_HEIGHT / 2) - PUCKS[i].radius or y <  (SCREEN_HEIGHT / 2) - (ISLAND_HEIGHT/ 2) + PUCKS[i].radius:
                    # PUCKS[i].velocity = (PUCKS[i].velocity[0], -PUCKS[i].velocity[1])
                    PUCKS[i].position = (-1,-1)
                    PUCKS[i].velocity = (0,0)
                    PUCKS[i].onIsland = False

            for i in range(len(PUCKS)):
                for arrow in ARROWS:
                    if PUCKS[i].position == arrow[0]:
                        PUCKS[i].velocity = (arrow[1][0] * 0.01, arrow[1][1] * 0.01)
                PUCKS[i].hasLine = False

            # Check for collisions
            for i in range(len(PUCKS)):
                for j in range(i+1, len(PUCKS)):
                    if PUCKS[i].col_circle(PUCKS[j].position):

                        vx1i = PUCKS[i].velocity[0] # 1
                        vy1i = PUCKS[i].velocity[1] # 1
                        vx2i = PUCKS[j].velocity[0] # 1
                        vy2i = PUCKS[j].velocity[1] # 1
                        m1 = PUCKS[i].mass # 1
                        m2 = PUCKS[j].mass # 1
                        x1,y1 = PUCKS[i].position
                        x2,y2 = PUCKS[j].position

                        const1 = ((2*m2) / (m1 + m2)) * (dot_product([vx1i-vx2i, vy1i-vy2i], [x1-x2, y1-y2])) / (magnitude([x1-x2, y1-y2])+.000001)
                        vx1f = vx1i - (const1 * (x1-x2))
                        vy1f = vy1i - (const1 * (y1-y2))

                        const2 = ((2*m1) / (m1 + m2)) * (dot_product([vx2i-vx1i, vy2i-vy1i], [x2-x1, y2-y1])) / (magnitude([x2-x1, y2-y1])+.000001)
                        vx2f = vx2i - (const2 * (x2-x1))
                        vy2f = vy2i - (const2 * (y2-y1))

                        PUCKS[i].velocity = (vx1f,vy1f)
                        PUCKS[j].velocity = (vx2f, vy2f)

            for puck in PUCKS:
                ax = mu * GRAVITY * math.cos(get_angle_of_motion(puck.velocity[0], puck.velocity[1]))
                ay = mu * GRAVITY * math.sin(get_angle_of_motion(puck.velocity[0], puck.velocity[1]))
                puck.acceleration = ax, ay
                vx,vy = puck.velocity
                vx += ax * .01
                vy += ay * .01
                puck.velocity = (vx,vy)
                print(puck.acceleration)
                puck.move()

            STOPPED = True

            for i in range(len(PUCKS)):
                if PUCKS[i].velocity[0] != 0 and PUCKS[i].velocity[1] != 0:
                    STOPPED = False

            if STOPPED:
                DRAW_ARROW_STATE = not DRAW_ARROW_STATE

        # Draw Pucks To Screen
        for puck in PUCKS:
            puck.draw(SCREEN)

        # Flip / Update the Display
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
