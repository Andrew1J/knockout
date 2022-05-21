import pygame
import sys
pygame.init()


# Global Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400
PUCK_RADIUS = 10
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
PUCKS = pygame.sprite.Group()


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
        ''' User clicked the puck '''
        self.isClicked = not self.isClicked

    def draw(self, surface):
        ''' Draw puck to the surface '''
        if self.isClicked:
            pygame.draw.circle(surface, (0,0,0), (self.position[0], self.position[1]), PUCK_RADIUS)
        else:
            pygame.draw.circle(surface, self.color, (self.position[0], self.position[1]), PUCK_RADIUS)

    def get_pos(self):
        '''Get puck position'''
        return (self.position[0],self.position[1])

    def col_circle(self, circlepos):
        '''Checking for collision with a circle'''
        x1, y1 = self.position
        x2, y2 = circlepos

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        if distance <= PUCK_RADIUS:
            return True
        return False

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


def main():
    ''' Main Function'''

    # Set up the level
    setup_lvl1()
    
    DRAW_ARROW_STATE = True

    # MAIN GAME LOOP
    running = True
    while running:

        if DRAW_ARROW_STATE:
            # Main Event Handling
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN and event.key == pygame.K_q: # Check for game quit()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN: # Check for mouse click
                    pos1 = pygame.mouse.get_pos()
                    clicked_sprites = [puck for puck in PUCKS if puck.col_circle(pos1)]
                    
                    for puck in clicked_sprites:
                        print(puck.get_pos())
                        puck.click()

                if event.type == pygame.MOUSEBUTTONUP: # Draw arrow
                    # TODO reset arrow, store arrow magnitude + direction
                    pos2 = pygame.mouse.get_pos()

                    for puck in clicked_sprites:
                        pygame.draw.line(SCREEN, (0,0,0), puck.get_pos(), pos2)
                        puck.click()
        else:
            # Check for collisions

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
