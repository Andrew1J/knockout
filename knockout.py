import pygame
import sys
from puck import Puck
import math
import numpy as np
pygame.init()
clock = pygame.time.Clock()


# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400
BUTTON_WIDTH, BUTTON_HEIGHT = 140, 40
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
PUCKS = []
PUCK_RADIUS = 10
PLAYER_ONE_TURN = True
ARROWS = []
GRAVITY = -9.8
ARROW_SPEED_CONSTANT = 0.02
mu = 0.1


# Set Up Levels
def setup_lvl1():
    ''' Sets up screen for level 1'''

    # Draw Water
    SCREEN.fill((0, 0, 255))

    # Draw Island
    pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

    # Draw Pucks
    puck1 = Puck((300, 500), (0,0),(255,0,255), 1, 1, PUCK_RADIUS)
    puck2 = Puck((300, 400), (0,0),(255,0,255), 1, 1, PUCK_RADIUS)
    puck3 = Puck((300, 300), (0,0),(255,0,255), 1, 1, PUCK_RADIUS)
    puck4 = Puck((500, 500), (0,0),(255,0,0), 1, 2, PUCK_RADIUS)
    puck5 = Puck((500, 400), (0,0),(255,0,0), 1, 2, PUCK_RADIUS)
    puck6 = Puck((500, 300), (0,0),(255,0,0), 1, 2, PUCK_RADIUS)

    # Add pucks to the list of pucks
    PUCKS.append(puck1)
    PUCKS.append(puck2)
    PUCKS.append(puck3)
    PUCKS.append(puck4)
    PUCKS.append(puck5)
    PUCKS.append(puck6)


def display_buttons():
    # Display ice button
    smallfont = pygame.font.SysFont('Corbel',35)
    text = smallfont.render('Ice' , True , (255,255,255))
    pygame.draw.rect(SCREEN, (100,100,100),[SCREEN_WIDTH/6,5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
    SCREEN.blit(text , (SCREEN_WIDTH/6 + 50,5 * (SCREEN_HEIGHT/6) + 5))

    # Display steel button
    pygame.draw.rect(SCREEN, (50,50,50),[2*SCREEN_WIDTH/6,5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
    text = smallfont.render('Steel' , True , (255,255,255))
    SCREEN.blit(text , (2*SCREEN_WIDTH/6 + 40,5 * (SCREEN_HEIGHT/6) + 5))

    # Display rock button
    pygame.draw.rect(SCREEN, (100,100,100),[3*SCREEN_WIDTH/6,5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
    text = smallfont.render('Rock' , True , (255,255,255))
    SCREEN.blit(text , (3*SCREEN_WIDTH/6 + 40,5 * (SCREEN_HEIGHT/6) + 5))

    # Display wool button
    pygame.draw.rect(SCREEN, (50,50,50),[4*SCREEN_WIDTH/6,5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
    text = smallfont.render('Wool' , True , (255,255,255))
    SCREEN.blit(text , (4*SCREEN_WIDTH/6 + 40,5 * (SCREEN_HEIGHT/6) + 5))


def display_information(pucks):
    ''' Displays the velocities after each collision in the side bar '''

    for i in range(len(pucks)):
        smallfont = pygame.font.SysFont('Corbel',15)
        text = smallfont.render("PUCK " + str(i+1) + " Velocity: "+ str(round(pucks[i].velocity[0])) + ", " + str(round(pucks[i].velocity[1])) , True , (255,255,255))
        SCREEN.blit(text , (6*SCREEN_WIDTH/8 + 50, (i+1) * (SCREEN_HEIGHT/9)))


def game_end(pucks):
    ''' Renders game end screen if game is over '''
    cntp1 = 0
    cntp2 = 0
    for puck in pucks:
        if puck.player == 1:
            cntp1 += 1
        if puck.player == 2:
            cntp2 += 1
    if cntp1 == 0:
        SCREEN.fill((0, 0, 255))
        pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])
        for puck in pucks:
            puck.draw(SCREEN)
        font = pygame.font.SysFont(None, 100)
        img = font.render('Player 2 Won', True, (0,0,0))
        imgx, imgy = img.get_size()
        SCREEN.blit(img, (SCREEN_WIDTH/2 - imgx/2, SCREEN_HEIGHT/2 - imgy/2))
    if cntp2 == 0:
        SCREEN.fill((0, 0, 255))
        pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])
        for puck in pucks:
            puck.draw(SCREEN)
        font = pygame.font.SysFont(None, 100)
        img = font.render('Player 1 Won', True, (0,0,0))
        imgx, imgy = img.get_size()
        SCREEN.blit(img, (SCREEN_WIDTH/2 - imgx/2, SCREEN_HEIGHT/2 - imgy/2))


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

    # Display information
    display_information(PUCKS)

    # MAIN GAME LOOP
    running = True
    while running:
        clock.tick(120)

        display_buttons()

        # End game if no pucks are left
        if len(PUCKS) == 0:
            running = False

        if DRAW_ARROW_STATE: # Drawing arrows phase

            # Check whose turn it is
            drawn_p1_sprites = [puck for puck in PUCKS if (puck.player == 1 and not puck.hasLine)]
            drawn_p2_sprites = [puck for puck in PUCKS if (puck.player == 2 and not puck.hasLine)]
            if len(drawn_p1_sprites) == 0:
                PLAYERONETURN = False
            if len(drawn_p2_sprites) == 0:
                PLAYERONETURN = True

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
                global mu
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT: # Check for game quit()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse click
                    pos1 = pygame.mouse.get_pos()

                    clicked_sprites = [puck for puck in PUCKS if puck.col_circle(pos1)]

                    for puck in clicked_sprites:
                        if not puck.hasLine and ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            puck.click()

                if event.type == pygame.MOUSEBUTTONUP: # Draw arrow
                    pos2 = pygame.mouse.get_pos()

                    # Ice button
                    if SCREEN_WIDTH/6 <= pos2[0] <= SCREEN_WIDTH/6+BUTTON_WIDTH and 5*SCREEN_HEIGHT/6 <= pos2[1] <= 5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.05
                        print("mu was set to " + str(mu))

                    # steel button
                    if 2*SCREEN_WIDTH/6 <= pos2[0] <= 2*SCREEN_WIDTH/6+BUTTON_WIDTH and 5*SCREEN_HEIGHT/6 <= pos2[1] <= 5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.1
                        print("mu was set to " + str(mu))

                    # rock button
                    if 3*SCREEN_WIDTH/6 <= pos2[0] <= 3*SCREEN_WIDTH/6+BUTTON_WIDTH and 5*SCREEN_HEIGHT/6 <= pos2[1] <= 5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.2
                        print("mu was set to " + str(mu))

                    # wool button
                    if 4*SCREEN_WIDTH/6 <= pos2[0] <= 4*SCREEN_WIDTH/6+BUTTON_WIDTH and 5*SCREEN_HEIGHT/6 <= pos2[1] <= 5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.3
                        print("mu was set to " + str(mu))


                    for puck in clicked_sprites:
                        if not puck.hasLine and ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            pygame.draw.line(SCREEN, (0,0,0), puck.get_pos(), pos2)
                            ARROWS.append((puck.get_pos(),(pos2[0]-puck.get_pos()[0], pos2[1] - puck.get_pos()[1])))
                            puck.hasLine = True
                            puck.click()
                        if puck.hasLine:
                            #TODO RESET ARROW
                            pass

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_a): # Check for game shoot phase #TODO REPLACE WITH BUTTON
                    DRAW_ARROW_STATE = False
                    PLAYERONETURN = True


        else: # Check for collisions after shooting the pucks

            # Draw Water
            SCREEN.fill((0, 0, 255))

            # Draw Island
            pygame.draw.rect(SCREEN, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

            display_buttons()

            # Display information
            display_information(PUCKS)

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
                    if np.sign(vx + ax * 0.01) != np.sign(vx):
                        vx = 0
                elif vx < 0:
                    if np.sign(vx - ax * 0.01) != np.sign(vx):
                        vx = 0
                if vy > 0:
                    if np.sign(vy + ay * 0.01) != np.sign(vy):
                        vy = 0
                elif vy < 0:
                    if np.sign(vy + ay * 0.01) != np.sign(vy):
                        vy = 0
                if vx > 0:
                    vx += ax * .01
                elif vx < 0:
                    vx -= ax * .01
                if vy > 0:
                    vy += ay * .01
                elif vy < 0:
                    vy -= ay * .01
                puck.velocity = (vx,vy)

                # if abs(vx) < 0.01 and abs(vy) < 0.01: #TODO FIX HOW WE HANDLE STOPPING
                #     puck.velocity = (0,0)
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
        # TODO IMPLEMENT GAME RESTART
        game_end(PUCKS)

        # Flip / Update the Display
        pygame.display.flip()
        pygame.display.update()
        pygame.event.pump()

    pygame.quit()


if __name__ == '__main__':
    main()
