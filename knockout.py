import pygame
pygame.init()

# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400
PUCK_RADIUS = 10

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pucks = pygame.sprite.Group()

# Defines a class for the pucks
class Puck(object):
    def __init__(self):
        self.position = (250,250)
        self.color = (255,0,255)
        self.onIsland = True


    def set_pos(self, x, y):
        ''' Set the x,y position of the puck '''
        self.position = (x,y)

    def set_color(self, color):
        ''' Set the color of the puck '''
        self.color = color

    def move(self):
        ''' Calculate the velocities and stuff '''
        pass

    def draw(self, surface):
        ''' Draw puck to the surface '''
        pygame.draw.circle(surface, self.color, (self.position[0], self.position[1]), PUCK_RADIUS)

    def get_pos(self):
        '''Get puck position'''
        return (self.positions[0],self.position[1])

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
    puck1 = Puck()
    pucks.add(puck1)
    puck2 = Puck()
    puck3 = Puck()
    puck4 = Puck()
    puck5 = Puck()
    puck6 = Puck()

    puck1.set_pos(300, 500)
    puck2.set_pos(300, 400)
    puck3.set_pos(300, 300)
    puck4.set_pos(500, 500)
    puck5.set_pos(500, 400)
    puck6.set_pos(500, 300)
    puck4.set_color((255,0,0))
    puck5.set_color((255,0,0))
    puck6.set_color((255,0,0))

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

    # Run until the user asks to quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Collision detection
        for puck in pucks:
            col(puck, pucks)

        # Flip the display
        pygame.display.flip()
        pygame.display.update()

if __name__ == '__main__':
    main()
