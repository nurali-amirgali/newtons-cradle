import pygame
import sys

WIDTH = 800
HEIGHT = 600
FPS = 60

BG_COLOR = (30,30,30)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("newtons cradle")

clock = pygame.time.Clock()

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
        pygame.draw.circle(self.screen, (255,255,255), (self.x, self.y), self.pivotRadius)

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