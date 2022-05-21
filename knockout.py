import pygame
import sys
pygame.init()

# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400
PUCK_RADIUS = 10

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pucks = pygame.sprite.Group()

# Defines a class for the pucks
class Puck(pygame.sprite.Sprite):
    def __init__(self, position, color):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.color = color
        self.onIsland = True
        self.isClicked = False

    def set_pos(self, x, y):
        ''' Set the x,y position of the puck '''
        self.position = (x,y)

    def set_color(self, color):
        ''' Set the color of the puck '''
        self.color = color

    def move(self):
        ''' Calculate the velocities and stuff '''
        pass

    def click(self):
        self.isClicked = not self.isClicked
        self.set_color((255,255,255))

    def draw(self, surface):
        ''' Draw puck to the surface '''
        pygame.draw.circle(surface, self.color, (self.position[0], self.position[1]), PUCK_RADIUS)

    def get_pos(self):
        '''Get puck position'''
        return (self.position[0],self.position[1])

    def col(self, pucks):
        '''Checking for collision'''
        return (self, pygame.sprite.spritecollideany(self, pucks, collided = None))


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
    screen.fill((0, 0, 255))

    # Draw Island
    pygame.draw.rect(screen, (0,255,0), [SCREEN_WIDTH/2 - ISLAND_WIDTH/2, SCREEN_HEIGHT/2 - ISLAND_HEIGHT/2, ISLAND_WIDTH, ISLAND_HEIGHT])

    # Draw Pucks
    puck1 = Puck((300, 500), (255,0,255))
    puck2 = Puck((300, 400), (255,0,255))
    puck3 = Puck((300, 300), (255,0,255))
    puck4 = Puck((500, 500), (255,0,0))
    puck5 = Puck((500, 400), (255,0,0))
    puck6 = Puck((500, 300), (255,0,0))

    pucks.add(puck1)
    pucks.add(puck2)
    pucks.add(puck3)
    pucks.add(puck4)
    pucks.add(puck5)
    pucks.add(puck6)

    puck1.draw(screen)
    puck2.draw(screen)
    puck3.draw(screen)
    puck4.draw(screen)
    puck5.draw(screen)
    puck6.draw(screen)


def display_information():
    ''' Displays the velocities after each collision in the side bar '''
    pass

def main():
    ''' Main Function'''

    # Set up the level
    setup_lvl1()
    
    SETUPSTATE = True

    # Run until the user asks to quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check for game quit()
                pygame.quit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and pucks.rect.collidepoint(pygame.mouse.get_pos()):
                pos = pygame.mouse.get_pos()


            

        # Collision detection
        for puck in pucks:
            # col(puck, pucks)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()

        if SETUPSTATE:
            pass
            # able to click on balls and draw arrows
        else:
            pass
            # balls shoot

        # Flip the display
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()
if __name__ == '__main__':
    main()
