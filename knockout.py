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
ARROW_SPEED_CONSTANT = 0.01
mu = 0.3


# Set Up Levels
def setup_lvl1():
    ''' Sets up screen for level 1'''

    # Draw Water
    SCREEN.fill((0, 0, 255))

    # Draw Island
    pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

    # Draw Pucks
    puck1 = Puck((300, 500), (0,0),(255,0,255), 1, 1)
    puck2 = Puck((300, 400), (0,0),(255,0,255), 1, 1)
    puck3 = Puck((300, 300), (0,0),(255,0,255), 1, 1)
    puck4 = Puck((500, 500), (0,0),(255,0,0), 1, 2)
    puck5 = Puck((500, 400), (0,0),(255,0,0), 1, 2)
    puck6 = Puck((500, 300), (0,0),(255,0,0), 1, 2)

    # Add pucks to the list of pucks
    PUCKS.append(puck1)
    PUCKS.append(puck2)
    PUCKS.append(puck3)
    PUCKS.append(puck4)
    PUCKS.append(puck5)
    PUCKS.append(puck6)

    for puck in PUCKS:
        print(puck.player)


def display_information():
    ''' Displays the velocities after each collision in the side bar '''
    
    pass


def game_end(pucks):
    ''' Renders game end screen if game is over '''
    cntp1 = 0
    cntp2 = 0
    for puck in PUCKS:
        if puck.player == 1:
            cntp1 += 1
        if puck.player == 2:
            cntp2 += 1
    if cntp1 == 0:
        SCREEN.fill((0, 0, 255))
        font = pygame.font.SysFont(None, 100)
        img = font.render('Player 2 Won', True, (255,255,255))
        SCREEN.blit(img, (0,0))
    if cntp2 == 0:
        SCREEN.fill((0, 0, 255))
        font = pygame.font.SysFont(None, 100)
        img = font.render('Player 1 Won', True, (255,255,255))
        SCREEN.blit(img, (0,0))

def outofbounds(coords):
    ''' Returns true if the puck is out of bounds '''

    x,y = coords

    if x > (SCREEN_WIDTH / 2) + (ISLAND_WIDTH / 2) or x <  (SCREEN_WIDTH / 2) - (ISLAND_WIDTH / 2):
        return True

    if y > (SCREEN_HEIGHT / 2) + (ISLAND_HEIGHT / 2) or y <  (SCREEN_HEIGHT / 2) - (ISLAND_HEIGHT/ 2):
        return True

    return False


def dot_product(v1, v2):
    '''Returns the dot product of two vectors'''

    return v1[0] * v2[0] + v1[1] * v2[1]


def magnitude_squared(v):
    '''Returns the magnitude squared of a vector'''

    return (v[0]*v[0] + v[1]*v[1])


def subtract_vectors(v1,v2):
    '''Subtracts two vectors'''

    return (v1[0] - v2[0], v1[1] - v2[1])


def get_angle_of_motion(v1,v2):
    '''Returns the angle of motion between two vectors'''

    return math.atan(v2/(v1+.000001))


def collision_response(puck1, puck2):
    '''Calculates the final velocities between two pucks after they collide'''

    vx1i = puck1.velocity[0] 
    vy1i = puck1.velocity[1] 
    vx2i = puck2.velocity[0] 
    vy2i = puck2.velocity[1] 
    m1 =  puck1.mass 
    m2 = puck2.mass 
    x1,y1 = puck1.position
    x2,y2 = puck2.position

    const1 = ((2*m2) / (m1 + m2)) * (dot_product([vx1i-vx2i, vy1i-vy2i], [x1-x2, y1-y2])) / (magnitude_squared([x1-x2, y1-y2])+.000001)
    vx1f = vx1i - (const1 * (x1-x2))
    vy1f = vy1i - (const1 * (y1-y2))

    const2 = ((2*m1) / (m1 + m2)) * (dot_product([vx2i-vx1i, vy2i-vy1i], [x2-x1, y2-y1])) / (magnitude_squared([x2-x1, y2-y1])+.000001)
    vx2f = vx2i - (const2 * (x2-x1))
    vy2f = vy2i - (const2 * (y2-y1))

    return [vx1f, vy1f], [vx2f, vy2f]


def main():
    ''' Main Function'''

    DRAW_ARROW_STATE = True
    PLAYERONETURN = True

    # Set up the level
    setup_lvl1()

    # MAIN GAME LOOP
    running = True
    while running:
        clock.tick(120)

        # End game if no pucks are left
        if len(PUCKS) == 0:
            running = False

        if DRAW_ARROW_STATE: # Drawing arrows phase
            
            # Draw whose turn it is on the screen
            if PLAYERONETURN:
                font = pygame.font.SysFont(None, 24)
                img = font.render('Player 1\'s Turn', True, (255,255,255))
                SCREEN.blit(img, (20, 20))
            else:
                font = pygame.font.SysFont(None, 24)
                img = font.render('Player 2\'s Turn', True, (255,255,255))
                SCREEN.blit(img, (20, 20))


            # Main Event Handling
            for event in pygame.event.get():

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT: # Check for game quit()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse click
                    pos1 = pygame.mouse.get_pos()
                    clicked_sprites = [puck for puck in PUCKS if puck.col_circle(pos1)]

                    for puck in clicked_sprites:
                        if ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            puck.click()

                if event.type == pygame.MOUSEBUTTONUP: # Draw arrow
                    pos2 = pygame.mouse.get_pos()

                    for puck in clicked_sprites:
                        print(not PLAYERONETURN)
                        # print(((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)))
                        if not puck.hasLine and ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            # print(puck.get_pos())
                            pygame.draw.line(SCREEN, (0,0,0), puck.get_pos(), pos2)
                            ARROWS.append((puck.get_pos(),(pos2[0]-puck.get_pos()[0], pos2[1] - puck.get_pos()[1])))
                            puck.hasLine = True
                            puck.click()
                        if puck.hasLine:
                            #TODO RESET ARROW
                            pass

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_a): # Check for game shoot phase #TODO REPLACE WITH BUTTON
                    DRAW_ARROW_STATE = False

            # Check whose turn it is
            drawn_p1_sprites = [puck for puck in PUCKS if (puck.player == 1 and not puck.hasLine)]
            drawn_p2_sprites = [puck for puck in PUCKS if (puck.player == 2 and not puck.hasLine)]
            if len(drawn_p1_sprites) == 0:
                PLAYERONETURN = False
            if len(drawn_p2_sprites) == 0:
                PLAYERONETURN = True

        else: # Check for collisions after shooting the pucks

            # Draw Water
            SCREEN.fill((0, 0, 255))

            # Draw Island
            pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])
            
            # TODO: Puck gets removed if its out of bounds
            puckscopy = PUCKS.copy()
            for i in range(len(puckscopy)):
                x,y = puckscopy[i].position

                if x >= (SCREEN_WIDTH / 2) + (ISLAND_WIDTH / 2) or x <  (SCREEN_WIDTH / 2) - (ISLAND_WIDTH / 2):
                    PUCKS.remove(puckscopy[i])
                if y >= (SCREEN_HEIGHT / 2) + (ISLAND_HEIGHT / 2) or y <  (SCREEN_HEIGHT / 2) - (ISLAND_HEIGHT/ 2):
                    PUCKS.remove(puckscopy[i])
            
            # Calculate the pucks initial velocities based on arrows
            for i in range(len(PUCKS)):
                for arrow in ARROWS:
                    if PUCKS[i].position == arrow[0]:
                        PUCKS[i].velocity = (arrow[1][0] * ARROW_SPEED_CONSTANT, arrow[1][1] * ARROW_SPEED_CONSTANT)
                PUCKS[i].hasLine = False

            # Check for collisions
            for i in range(len(PUCKS)):
                for j in range(i+1, len(PUCKS)):
                    if PUCKS[i].col_circle(PUCKS[j].position): # Check for collision
                        v1f, v2f = collision_response(PUCKS[i], PUCKS[j]) # Calculate the new velocities
                        PUCKS[i].velocity = v1f
                        PUCKS[j].velocity = v2f

            # Apply frictional accelerations to the velocities
            for puck in PUCKS:
                ax = mu * GRAVITY * math.cos(get_angle_of_motion(abs(puck.velocity[0]), abs(puck.velocity[1])))
                ay = mu * GRAVITY * math.sin(get_angle_of_motion(abs(puck.velocity[0]), abs(puck.velocity[1])))
                puck.acceleration = ax, ay
                vx,vy = puck.velocity
                if vx > 0:
                    vx += ax * .01
                elif vx < 0:
                    vx -= ax * .01
                if vy > 0:
                    vy += ay * .01
                elif vy < 0:
                    vy -= ay * .01
                puck.velocity = (vx,vy)
                if abs(vx) < 0.01 and abs(vy) < 0.01:
                    puck.velocity = (0,0)
                puck.move()

            # Check if all pucks stopped (changing game state back)
            STOPPED = True
            for i in range(len(PUCKS)):
                if PUCKS[i].velocity[0] != 0 and PUCKS[i].velocity[1] != 0:
                    STOPPED = False
            if STOPPED:
                DRAW_ARROW_STATE = not DRAW_ARROW_STATE

        # Draw Pucks To Screen
        for puck in PUCKS:
            puck.draw(SCREEN)

        # Display end game screen if pucks fall off
        game_end(PUCKS)

        # Flip / Update the Display
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
