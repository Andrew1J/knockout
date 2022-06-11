import pygame
import sys
from puck import Puck
import math
from collisionmath import *
import numpy as np
import button
pygame.init()
clock = pygame.time.Clock()


# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 750
ISLAND_WIDTH, ISLAND_HEIGHT = 500, 500
BUTTON_WIDTH, BUTTON_HEIGHT = 140, 40
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
PUCKS = []
PUCK_RADIUS = 30
PLAYER_ONE_TURN = True
ARROWS = []
GRAVITY = -9.8
ARROW_SPEED_CONSTANT = 0.025
mu = 0.3
field_type = 'Ground'
elasticity = 1.0


# Set Up Levels
def setup_lvl1():
    ''' Sets up screen for level 1'''

    # Draw Background
    draw_background()

    # Draw Island
    draw_island()

    # Draw Pucks
    offset = ISLAND_WIDTH / 4
    startx, starty = SCREEN_WIDTH/12 + offset, SCREEN_HEIGHT/8 + offset
    puck1 = Puck((startx, starty), (0,0),(255,0,255), 2.0, 1, PUCK_RADIUS, "A")
    puck2 = Puck((startx, starty + offset), (0,0),(255,0,255), 2.0, 1, PUCK_RADIUS, "B")
    puck3 = Puck((startx, starty + 2 * offset), (0,0),(255,0,255), 2.0, 1, PUCK_RADIUS, "C")
    puck4 = Puck((startx + 2 * offset, starty), (0,0),(255,0,0), 2.0, 2, PUCK_RADIUS, "D")
    puck5 = Puck((startx + 2 * offset, starty + offset), (0,0),(255,0,0), 2.0, 2, PUCK_RADIUS, "E")
    puck6 = Puck((startx + 2 * offset, starty + 2*offset), (0,0),(255,0,0), 2.0, 2, PUCK_RADIUS, "F")

    # Add pucks to the list of pucks
    PUCKS.append(puck1)
    PUCKS.append(puck2)
    PUCKS.append(puck3)
    PUCKS.append(puck4)
    PUCKS.append(puck5)
    PUCKS.append(puck6)


def draw_island():
    if field_type == 'Ice':
        pygame.draw.rect(SCREEN, (200,233,233), [SCREEN_WIDTH/12, SCREEN_HEIGHT/8, ISLAND_WIDTH, ISLAND_HEIGHT])
    elif field_type == 'Horseshoe':
        pygame.draw.rect(SCREEN, (136,139,141), [SCREEN_WIDTH/12, SCREEN_HEIGHT/8, ISLAND_WIDTH, ISLAND_HEIGHT])
    elif field_type == 'Asphalt':
        pygame.draw.rect(SCREEN, (31,32,34), [SCREEN_WIDTH/12, SCREEN_HEIGHT/8, ISLAND_WIDTH, ISLAND_HEIGHT])
    elif field_type == 'Concrete':
        pygame.draw.rect(SCREEN, (118,134,146), [SCREEN_WIDTH/12, SCREEN_HEIGHT/8, ISLAND_WIDTH, ISLAND_HEIGHT])
    else:
        pygame.draw.rect(SCREEN, (48,200,0), [SCREEN_WIDTH/12, SCREEN_HEIGHT/8, ISLAND_WIDTH, ISLAND_HEIGHT])


def draw_background():
    # Draw Water
    SCREEN.fill((0, 94, 184))

    # Draw Buttons
    display_buttons()

    # Draw LOGO
    smallfont = pygame.font.SysFont('Corbel', 60)
    img = smallfont.render('KNOCKOUT', True, (255,255,255))
    textx, texty = img.get_size()
    SCREEN.blit(img, (SCREEN_WIDTH/12, SCREEN_HEIGHT/16 - texty/2))


def display_information(pucks):
    ''' Displays the live velocities of each puck in the side bar '''

    smallfont = pygame.font.SysFont('Corbel',20)
    for i in range(len(pucks)):
        if pucks[i].onField:
            text = smallfont.render("PUCK " + str(pucks[i].id) + " Velocity: "+ str(round(pucks[i].velocity[0], 2)) + ", " + str(round(-1*pucks[i].velocity[1], 2)) , True , (255,255,255))
        else:
            text = smallfont.render("PUCK " + str(pucks[i].id) + " Velocity: "+ str(round(pucks[i].velocity[0], 2)) + ", " + str(round(-1*pucks[i].velocity[1], 2)) , True , (255,0,0))
        SCREEN.blit(text, (72 * SCREEN_WIDTH/100 + 50, (i+1.1) * (SCREEN_HEIGHT/9)))

        # Display mass text
        text = smallfont.render('Mass: ' + str(PUCKS[i].mass), True , (255,255,255))
        textx, texty = text.get_size()
        SCREEN.blit(text, (84 * SCREEN_WIDTH/100 + 20 - (textx/2), (i+1.3) * (SCREEN_HEIGHT/9) + 5))

        # Display increase and decrease buttons
        text = smallfont.render('+' , True , (255,255,255))
        if 78 * SCREEN_WIDTH/100 <= pygame.mouse.get_pos()[0] <= 78 * SCREEN_WIDTH/100 + BUTTON_WIDTH/4 and (i+1.3) * (SCREEN_HEIGHT/9) <= pygame.mouse.get_pos()[1] <= (i+1.5) * (SCREEN_HEIGHT/9) + BUTTON_HEIGHT/2:
            pygame.draw.rect(SCREEN, (170,170,170),[78 * SCREEN_WIDTH/100, (i+1.3) * (SCREEN_HEIGHT/9), BUTTON_WIDTH/4, BUTTON_HEIGHT/2], border_radius = 10)
        else:
            pygame.draw.rect(SCREEN, (100,100,100),[78 * SCREEN_WIDTH/100, (i+1.3) * (SCREEN_HEIGHT/9), BUTTON_WIDTH/4, BUTTON_HEIGHT/2], border_radius = 10)
        SCREEN.blit(text, (82 * SCREEN_WIDTH/100 - BUTTON_WIDTH/8, (i+1.3) * (SCREEN_HEIGHT/9)))

        text = smallfont.render('-' , True , (255,255,255))
        if 91 * SCREEN_WIDTH/100 <= pygame.mouse.get_pos()[0] <= 91 * SCREEN_WIDTH/100 + BUTTON_WIDTH/4 and (i+1.3) * (SCREEN_HEIGHT/9) <= pygame.mouse.get_pos()[1] <= (i+1.5) * (SCREEN_HEIGHT/9) + BUTTON_HEIGHT/2:
            pygame.draw.rect(SCREEN, (170,170,170),[91 * SCREEN_WIDTH/100, (i+1.3) * (SCREEN_HEIGHT/9), BUTTON_WIDTH/4, BUTTON_HEIGHT/2], border_radius = 10)
        else:
            pygame.draw.rect(SCREEN, (100,100,100),[91 * SCREEN_WIDTH/100, (i+1.3) * (SCREEN_HEIGHT/9), BUTTON_WIDTH/4, BUTTON_HEIGHT/2], border_radius = 10)
        SCREEN.blit(text, (95 * SCREEN_WIDTH/100 - BUTTON_WIDTH/8, (i+1.3) * (SCREEN_HEIGHT/9)))

def game_end(pucks):
    ''' Renders game end screen if game is over '''
    cntp1 = 0
    cntp2 = 0
    for puck in pucks:
        if puck.player == 1 and puck.onField:
            cntp1 += 1
        if puck.player == 2 and puck.onField:
            cntp2 += 1
    if cntp1 == 0:
        SCREEN.fill((0, 94, 184))
        draw_island()

        for puck in PUCKS:
            if puck.onField:
                puck.draw(SCREEN)

        smallfont = pygame.font.SysFont('Corbel', 100)
        img = smallfont.render('Player 2 Won', True, (0,0,0))
        imgx, imgy = img.get_size()
        SCREEN.blit(img, (SCREEN_WIDTH/2 - imgx/2, SCREEN_HEIGHT/2 - imgy/2))

        smallfont = pygame.font.SysFont('Corbel', 30)
        img = smallfont.render('Press R to Restart', True, (255,0,0))
        SCREEN.blit(img, (SCREEN_WIDTH/2 - imgx/2, SCREEN_HEIGHT/2 + imgy/2))

        return True
    if cntp2 == 0:
        SCREEN.fill((0, 94, 184))
        draw_island()

        for puck in PUCKS:
            if puck.onField:
                puck.draw(SCREEN)

        smallfont = pygame.font.SysFont('Corbel', 100)
        img = smallfont.render('Player 1 Won', True, (0,0,0))
        imgx, imgy = img.get_size()
        SCREEN.blit(img, (SCREEN_WIDTH/2 - imgx/2, SCREEN_HEIGHT/2 - imgy/2))

        smallfont = pygame.font.SysFont('Corbel', 30)
        img = smallfont.render('Press R to Restart', True, (255,0,0))
        SCREEN.blit(img, (SCREEN_WIDTH/2 - imgx/2, SCREEN_HEIGHT/2 + imgy/2))
        return True
    return False


def outofbounds(coords):
    ''' Returns true if the puck is out of bounds '''

    x,y = coords

    if x > SCREEN_WIDTH/12 + ISLAND_WIDTH or x < SCREEN_WIDTH/12:
        return True

    if y > SCREEN_HEIGHT/8 + ISLAND_HEIGHT or y < SCREEN_HEIGHT/8:
        return True

    return False


def collision_response(puck1, puck2):
    '''Calculates the final velocities of two colliding pucks '''

    vx1i = puck1.velocity[0]
    vy1i = puck1.velocity[1]
    vx2i = puck2.velocity[0]
    vy2i = puck2.velocity[1]
    m1 =  puck1.mass
    m2 = puck2.mass
    x1,y1 = puck1.position
    x2,y2 = puck2.position
    #TODO Implement elasticity component
    print((elasticity ** 0.5))

    const1 = ((2*m2) / (m1 + m2)) * (dot_product([vx1i-vx2i, vy1i-vy2i], [x1-x2, y1-y2])) / (magnitude_squared([x1-x2, y1-y2])+.000001)
    vx1f = (elasticity ** 0.5) * (vx1i - (const1 * (x1-x2)))
    vy1f = (elasticity ** 0.5) * (vy1i - (const1 * (y1-y2)))

    const2 = ((2*m1) / (m1 + m2)) * (dot_product([vx2i-vx1i, vy2i-vy1i], [x2-x1, y2-y1])) / (magnitude_squared([x2-x1, y2-y1])+.000001)
    vx2f = (elasticity ** 0.5) * (vx2i - (const2 * (x2-x1)))
    vy2f = (elasticity ** 0.5) * (vy2i - (const2 * (y2-y1)))

    return [vx1f, vy1f], [vx2f, vy2f]


def display_buttons():
    ''' Display field and buttons to change physical variables '''

    # Display elasticity text
    smallfont = pygame.font.SysFont('Corbel', 35)
    text = smallfont.render('Elasticity: ' + str(elasticity), True , (255,255,255))
    textx, texty = text.get_size()
    SCREEN.blit(text, (3 * (SCREEN_WIDTH/6) - (textx/2), 5.1 * (SCREEN_HEIGHT/6) + 5))

    # Display elasticity buttons
    # +
    text = smallfont.render('+' , True , (255,255,255))
    if 2 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4 <= pygame.mouse.get_pos()[0] <= 2 * (SCREEN_WIDTH/6) + BUTTON_WIDTH/4 and 5.1 * (SCREEN_HEIGHT/6) <= pygame.mouse.get_pos()[1] <= 5.1 * (SCREEN_HEIGHT/6) + BUTTON_HEIGHT:
        pygame.draw.rect(SCREEN, (170,170,170),[2 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4, 5.1 * (SCREEN_HEIGHT/6), BUTTON_WIDTH/2, BUTTON_HEIGHT],border_radius = 10)
    else:
        pygame.draw.rect(SCREEN, (100,100,100),[2 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4, 5.1 * (SCREEN_HEIGHT/6), BUTTON_WIDTH/2, BUTTON_HEIGHT],border_radius = 10)
    SCREEN.blit(text, (2 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4 + 30, 5.1 * (SCREEN_HEIGHT/6) + 5))

    # -
    text = smallfont.render('-' , True , (255,255,255))
    if 4 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4 <= pygame.mouse.get_pos()[0] <= 4 * (SCREEN_WIDTH/6) + BUTTON_WIDTH/4 and 5.1 * (SCREEN_HEIGHT/6) <= pygame.mouse.get_pos()[1] <= 5.1 * (SCREEN_HEIGHT/6) + BUTTON_HEIGHT:
        pygame.draw.rect(SCREEN, (170,170,170),[4 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4, 5.1 * (SCREEN_HEIGHT/6), BUTTON_WIDTH/2, BUTTON_HEIGHT],border_radius = 10)
    else:
        pygame.draw.rect(SCREEN, (100,100,100),[4 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4, 5.1 * (SCREEN_HEIGHT/6), BUTTON_WIDTH/2, BUTTON_HEIGHT],border_radius = 10)
    SCREEN.blit(text, (4 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4 + 30, 5.1 * (SCREEN_HEIGHT/6) + 5))

    # Display field type buttons
    field_types = ['Ice', 'Horseshoe', 'Asphalt', 'Concrete']
    for i, mat in enumerate(field_types):
        text = smallfont.render(mat , True , (255,255,255))
        textx, texty = text.get_size()
        if i % 2 == 0:
            if (i+1) * (SCREEN_WIDTH/6) <= pygame.mouse.get_pos()[0] <= (i+1) * (SCREEN_WIDTH/6) + BUTTON_WIDTH and 5.5 * (SCREEN_HEIGHT/6) <= pygame.mouse.get_pos()[1] <= 4.8 * (SCREEN_HEIGHT/6) + BUTTON_HEIGHT:
                pygame.draw.rect(SCREEN, (170,170,170),[(i+1) * (SCREEN_WIDTH/6),5.5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
            else:
                pygame.draw.rect(SCREEN, (100,100,100),[(i+1) * (SCREEN_WIDTH/6),5.5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
            SCREEN.blit(text, ((i+1.5) * (SCREEN_WIDTH/6) - textx/2, 5.5 * (SCREEN_HEIGHT/6) + 5))
        else:
            if (i+1) * (SCREEN_WIDTH/6) <= pygame.mouse.get_pos()[0] <= (i+1) * (SCREEN_WIDTH/6) + BUTTON_WIDTH and 5.5 * (SCREEN_HEIGHT/6) <= pygame.mouse.get_pos()[1] <= 4.8 * (SCREEN_HEIGHT/6) + BUTTON_HEIGHT:
                pygame.draw.rect(SCREEN, (170,170,170),[(i+1) * (SCREEN_WIDTH/6),5.5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
            else:
                pygame.draw.rect(SCREEN, (50,50,50),[(i+1) * (SCREEN_WIDTH/6),5.5 * (SCREEN_HEIGHT/6), BUTTON_WIDTH, BUTTON_HEIGHT])
            SCREEN.blit(text, ((i+1.5) * (SCREEN_WIDTH/6) - textx/2, 5.5 * (SCREEN_HEIGHT/6) + 5))


def main():
    ''' Main Function'''

    DRAW_ARROW_STATE = True
    PLAYERONETURN = True
    global PUCKS
    global ARROWS

    # Set up the level
    setup_lvl1()
    display_information(PUCKS)


    # MAIN GAME LOOP
    running = True
    while running:
        clock.tick(30)

        # End game if no pucks are left
        if len(PUCKS) == 0:
            running = False

        if DRAW_ARROW_STATE: # Drawing arrows phase

            # Check whose turn it is
            drawn_p1_sprites = [puck for puck in PUCKS if (puck.player == 1 and not puck.hasLine and puck.onField)]
            drawn_p2_sprites = [puck for puck in PUCKS if (puck.player == 2 and not puck.hasLine and puck.onField)]
            if len(drawn_p1_sprites) == 0:
                PLAYERONETURN = False
            if len(drawn_p2_sprites) == 0:
                PLAYERONETURN = True

            if len(ARROWS) == len(PUCKS):
                PLAYERONETURN = False

            # Draw whose turn it is on the screen
            if PLAYERONETURN and len(ARROWS) != len(PUCKS):
                smallfont = pygame.font.SysFont('Corbel', 24)
                img = smallfont.render('Player 1\'s Turn', True, (255,0,0))
                imgx, imgy = img.get_size()
                SCREEN.blit(img, (SCREEN_WIDTH/12 + ISLAND_WIDTH - imgx, SCREEN_HEIGHT/16 - imgy/2))
            elif not PLAYERONETURN and len(ARROWS) != len(PUCKS):
                smallfont = pygame.font.SysFont('Corbel', 24)
                img = smallfont.render('Player 2\'s Turn', True, (255,0,0))
                imgx, imgy = img.get_size()
                SCREEN.blit(img, (SCREEN_WIDTH/12 + ISLAND_WIDTH - imgx, SCREEN_HEIGHT/16 - imgy/2))
            else:
                smallfont = pygame.font.SysFont('Corbel', 24)
                img = smallfont.render('Press the Shoot Button!', True, (255,0,0))
                imgx, imgy = img.get_size()
                SCREEN.blit(img, (SCREEN_WIDTH/12 + ISLAND_WIDTH - imgx, SCREEN_HEIGHT/16 - imgy/2))

            # Main Event Handling
            for event in pygame.event.get():
                global mu
                global elasticity
                global field_type

                smallfont = pygame.font.SysFont('Corbel', 25)
                text = smallfont.render('Shoot', True , (255,255,255))
                mybutton = button.Button(SCREEN,23*SCREEN_WIDTH/24 - BUTTON_WIDTH / 2, SCREEN_HEIGHT/16,BUTTON_WIDTH,BUTTON_HEIGHT,(255,0,0),(128,0,0),"Shoot",(0,0,0),smallfont)
                x,y = pygame.mouse.get_pos()
                mybutton.draw(x,y)

                if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse click
                    pos1 = pygame.mouse.get_pos()

                    clicked_sprites = [puck for puck in PUCKS if puck.col_mouse(pos1)]

                    for puck in clicked_sprites:
                        if ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            puck.click()

                if event.type == pygame.MOUSEBUTTONUP: # Draw arrow
                    pos2 = pygame.mouse.get_pos()
                    x,y = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])

                    # elasticity increase button
                    if elasticity < 1.0 and 2 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4 <= pygame.mouse.get_pos()[0] <= 2 * (SCREEN_WIDTH/6) + BUTTON_WIDTH/4 and 5.1 * (SCREEN_HEIGHT/6) <= pygame.mouse.get_pos()[1] <= 5.1 * (SCREEN_HEIGHT/6)+40:
                        elasticity += 0.05
                        elasticity = round(elasticity,2)
                        print("elasticity const was increased and is now " + str(elasticity))

                    # elasticity decrease button
                    if elasticity > 0.05 and 4 * (SCREEN_WIDTH/6) - BUTTON_WIDTH/4 <= pygame.mouse.get_pos()[0] <= 4 * (SCREEN_WIDTH/6) + BUTTON_WIDTH/4 and 5.1 * (SCREEN_HEIGHT/6) <= pygame.mouse.get_pos()[1] <= 5.1 * (SCREEN_HEIGHT/6)+40:
                        elasticity -= 0.05
                        elasticity = round(elasticity,2)
                        print("elasticity const was decreased and is now " + str(elasticity))

                    # ice button
                    if SCREEN_WIDTH/6 <= pos2[0] <= SCREEN_WIDTH/6+BUTTON_WIDTH and 5.5*SCREEN_HEIGHT/6 <= pos2[1] <= 5.5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.15
                        field_type = 'Ice'
                        print("mu was set to " + str(mu))

                    # horseshoe button
                    if 2*SCREEN_WIDTH/6 <= pos2[0] <= 2*SCREEN_WIDTH/6+BUTTON_WIDTH and 5.5*SCREEN_HEIGHT/6 <= pos2[1] <= 5.5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.7
                        field_type = 'Horseshoe'
                        print("mu was set to " + str(mu))

                    # asphalt button
                    if 3*SCREEN_WIDTH/6 <= pos2[0] <= 3*SCREEN_WIDTH/6+BUTTON_WIDTH and 5.5*SCREEN_HEIGHT/6 <= pos2[1] <= 5.5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.5
                        field_type = 'Asphalt'
                        print("mu was set to " + str(mu))

                    # concrete button
                    if 4*SCREEN_WIDTH/6 <= pos2[0] <= 4*SCREEN_WIDTH/6+BUTTON_WIDTH and 5.5*SCREEN_HEIGHT/6 <= pos2[1] <= 5.5*SCREEN_HEIGHT/6+BUTTON_HEIGHT:
                        mu = 0.8
                        field_type = 'Concrete'
                        print("mu was set to " + str(mu))

                    # mass buttons
                    for i in range(len(PUCKS)):
                        if PUCKS[i].mass < 3.0 and 78 * SCREEN_WIDTH/100 <= pygame.mouse.get_pos()[0] <= 78 * SCREEN_WIDTH/100 + BUTTON_WIDTH/4 and (i+1.3) * (SCREEN_HEIGHT/9) <= pygame.mouse.get_pos()[1] <= (i+1.3) * (SCREEN_HEIGHT/9) + BUTTON_HEIGHT/2:
                            PUCKS[i].mass += 0.1
                            PUCKS[i].mass = round(PUCKS[i].mass, 2)
                            print('mass for ' + str(i) + ' was increased and is now ' + str(round(PUCKS[i].mass,2)))

                        if PUCKS[i].mass > 1.0 and 91 * SCREEN_WIDTH/100 <= pygame.mouse.get_pos()[0] <= 91 * SCREEN_WIDTH/100 + BUTTON_WIDTH/4 and (i+1.3) * (SCREEN_HEIGHT/9) <= pygame.mouse.get_pos()[1] <= (i+1.3) * (SCREEN_HEIGHT/9) + BUTTON_HEIGHT/2:
                            PUCKS[i].mass -= 0.1
                            PUCKS[i].mass = round(PUCKS[i].mass, 2)
                            print('mass for ' + str(i) + ' was decreased and is now ' + str(round(PUCKS[i].mass,2)))

                    draw_background()
                    draw_island()
                    display_information(PUCKS)
                    mybutton.draw(x,y)

                    for puck in clicked_sprites:
                        if not puck.hasLine and ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            pygame.draw.line(SCREEN, (0,0,0), puck.get_pos(), pos2)
                            ARROWS.append((puck.get_pos(),(pos2[0]-puck.get_pos()[0], pos2[1] - puck.get_pos()[1])))
                            puck.hasLine = True
                        if puck.hasLine and ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            pos = puck.get_pos()
                            for arrow in ARROWS:
                                if arrow[0] == pos:
                                    ARROWS.remove(arrow)
                            ARROWS.append((puck.get_pos(),(pos2[0]-puck.get_pos()[0], pos2[1] - puck.get_pos()[1])))
                            for arrow in ARROWS:
                                pygame.draw.line(SCREEN, (0,0,0), puck.get_pos(), pos2)
                            puck.hasLine = True
                        if ((PLAYERONETURN and puck.player == 1) or (not PLAYERONETURN and puck.player == 2)):
                            puck.click()

                    if 23*SCREEN_WIDTH/24 - BUTTON_WIDTH <= x <= 23*SCREEN_WIDTH/24 and SCREEN_HEIGHT/16 - BUTTON_HEIGHT/2 <= y <= SCREEN_HEIGHT/16 + BUTTON_HEIGHT/2:
                        DRAW_ARROW_STATE = False
                        PLAYERONETURN = True

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_q) or event.type == pygame.QUIT: # Check for game quit()
                    running = False
                    sys.exit()

                display_information(PUCKS)
                display_buttons()

        else: # Check for collisions after shooting the pucks

            puckscopy = PUCKS.copy()
            for i in range(len(puckscopy)):
                x,y = puckscopy[i].position

                if outofbounds((x,y)):
                    PUCKS.remove(PUCKS[i])

            # Calculate the pucks initial velocities based on arrows
            for i in range(len(PUCKS)):
                for arrow in ARROWS:
                    if PUCKS[i].position == arrow[0]:
                        PUCKS[i].velocity = (arrow[1][0] * ARROW_SPEED_CONSTANT, arrow[1][1] * ARROW_SPEED_CONSTANT)
                PUCKS[i].hasLine = False

            ARROWS = []

            # Check for collisions
            for i in range(len(PUCKS)):
                for j in range(i+1, len(PUCKS)):
                    if PUCKS[i].col_circle(PUCKS[j]): # Check for collision
                        v1f, v2f = collision_response(PUCKS[i], PUCKS[j]) # Calculate the new velocities
                        PUCKS[i].velocity = v1f
                        PUCKS[j].velocity = v2f

                        print(PUCKS[i].velocity)
                        print(PUCKS[j].velocity)

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
                    if np.sign(vy - ay * 0.01) != np.sign(vy):
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
                puck.move()

            draw_background()
            draw_island()
            display_information(PUCKS)

            # Check if all pucks stopped (changing game state back)
            STOPPED = True
            for i in range(len(PUCKS)):
                if PUCKS[i].velocity[0] != 0 and PUCKS[i].velocity[1] != 0:
                    STOPPED = False
            if STOPPED:
                DRAW_ARROW_STATE = not DRAW_ARROW_STATE

        # Draw Pucks To Screen
        smallfont = pygame.font.SysFont('Corbel', 24)
        for puck in PUCKS:
            if puck.onField:
                puck.draw(SCREEN)
                img = smallfont.render(str(puck.id) , True , (255,255,255))
                imgx, imgy = img.get_size()
                SCREEN.blit(img , (puck.position[0] - 5, puck.position[1] - 5))
            else:
                puck.velocity = (0,0)

        if game_end(PUCKS):
            running = False

        # Flip / Update the Display
        pygame.display.flip()
        pygame.display.update()
        pygame.event.pump()

    # Game Restart
    RESTART = True
    while RESTART:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                PUCKS = []
                ARROWS = []
                main()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                RESTART = False
                break

    pygame.quit()


if __name__ == '__main__':
    main()
