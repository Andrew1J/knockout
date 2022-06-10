import pygame


PUCK_RADIUS = 10
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
ISLAND_WIDTH, ISLAND_HEIGHT = 400, 400

# Defines a class for the pucks
class Puck(pygame.sprite.Sprite):
    def __init__(self, position, velocity, color, mass, player, radius, id):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.color = color
        self.radius = radius
        self.isClicked = False
        self.hasLine = False
        self.velocity = velocity
        self.onField = True
        self.mass = mass
        self.acceleration = (0,0)
        self.player = player
        self.id = id

    def set_pos(self, x, y):
        ''' Set the x,y position of the puck '''
        self.position = (x,y)

    def set_color(self, color):
        ''' Set the color of the puck '''
        self.color = color

    def move(self):
        ''' Calculate the velocities and apply them frame by frame '''
        x,y = self.position
        vx,vy = self.velocity
        x += vx
        y += vy
        self.position = (x,y)

    def click(self):
        ''' User clicked the puck '''
        self.isClicked = not self.isClicked

    def draw(self, surface):
        ''' Draw puck to the surface '''
        if self.isClicked:
            pygame.draw.circle(surface, (0,0,0), (self.position[0], self.position[1]), round(self.mass**0.5 * PUCK_RADIUS, 2))
            self.radius = self.mass**0.5 * PUCK_RADIUS
        else:
            pygame.draw.circle(surface, self.color, (self.position[0], self.position[1]), round(self.mass**0.5 * PUCK_RADIUS, 2))
            self.radius = self.mass**0.5 * PUCK_RADIUS

    def get_pos(self):
        '''Get puck position'''
        return (self.position[0],self.position[1])

    def col_circle(self, PUCK):
        '''Checking for collision with another puck'''
        x1, y1 = self.position
        x2, y2 = PUCK.position

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        if distance <= self.radius + PUCK.radius:
            return True
        return False

    def col_mouse(self, pos):
        '''Checking for collision with another puck'''
        x1, y1 = self.position
        x2, y2 = pos

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        if distance <= 2*PUCK_RADIUS:
            return True
        return False
