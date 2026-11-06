import pygame
import sys
import math

WIDTH = 800
HEIGHT = 600
FPS = 60

BG_COLOR = (30,30,30)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("newtons cradle")

clock = pygame.time.Clock()

def getPoint(start, direction, length):
    x, y = start
    direction = math.radians(direction)

    new_x = x + math.cos(direction) * length
    new_y = y + math.sin(direction) * length

    return (new_x, new_y)

PIVOT_COLOR = (83, 81, 87)
ROPE_COLOR = (175, 172, 181)
BALL_COLOR = (49, 48, 51)

class pendulum:
    def __init__(self, x, y, screen, radius = 20, length = 150, mass = 10, pivotRadius = 10, ropeWidth = 10):
        self.x = x
        self.y = y
        self.screen = screen
        
        self.pivotRadius = pivotRadius
        self.ropeWidth = ropeWidth
        self.radius = radius
        self.length = length
        self.mass = mass
        
        self.angle = 0
        self.angularMomentum = 0
    
    def render(self):
        ballPos = getPoint((self.x, self.y), self.angle + 90, self.length)
        pygame.draw.line(self.screen, ROPE_COLOR, (self.x, self.y), ballPos, self.ropeWidth)
        pygame.draw.circle(self.screen, PIVOT_COLOR, (self.x, self.y), self.pivotRadius)
        pygame.draw.circle(self.screen, BALL_COLOR, ballPos, self.radius)

testPendulum = pendulum(WIDTH/2, HEIGHT * 0.2, screen)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
    screen.fill(BG_COLOR)
    
    testPendulum.render()
    
    pygame.display.flip()

pygame.quit()
sys.exit()