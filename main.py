import pygame
import sys
import math

WIDTH = 800
HEIGHT = 600
FPS = 120

BG_COLOR = (237, 235, 240)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
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

class newtonsCradle:
    def __init__(self, x, y, screen, numPendulums = 7, radius = 20, length = 150, 
                 mass = 10, period = 1.5, pivotRadius = 10, ropeWidth = 10):
        self.x = x
        self.y = y
        self.screen = screen
        self.numPendulums = 7
        self.pendulums = []
        
        self.numPendulums = numPendulums
        self.radius = radius
        self.length = length
        self.mass = mass
        self.period = period
        self.pivotRadius = pivotRadius
        self.ropeWidth = ropeWidth
        
        self.initPendulums()
    
    def initPendulums(self):
        for i in range(self.numPendulums):
            x = self.x + (i * self.radius * 2)
            newPendulum = pendulum(x, self.y, self.screen, self.radius, self.length, 
                                   self.mass, self.pivotRadius, self.ropeWidth, self.period)
            self.pendulums.append(newPendulum)
    
    def update(self, dt):
        for pendulumObj in self.pendulums:
            pendulumObj.update(dt)
    
    def render(self):
        for pendulumObj in self.pendulums:
            pendulumObj.render()
            
    def collisionCheck(self):
        for i in range(self.numPendulums - 1):
            current = self.pendulums[i]
            next = self.pendulums[i + 1]
            
            currentPos = getPoint((current.x, current.y), math.degrees(current.angle) + 90, current.length)
            nextPos = getPoint((next.x, next.y), math.degrees(next.angle) + 90, next.length)
            
            

class pendulum:
    def __init__(self, x, y, screen, radius = 20, length = 150, mass = 10, pivotRadius = 10, ropeWidth = 10, period = 1.5):
        self.x = x
        self.y = y
        self.screen = screen
        
        self.pivotRadius = pivotRadius
        self.ropeWidth = ropeWidth
        self.radius = radius
        self.length = length
        self.period = period #the time it takes to complete one full swing
        self.mass = mass
        
        self.angle = 0 #stored in radians
        self.angularVelocity = 0
        self.angularAcceleration = 0
        self.friction = 0.1
        self.gravity = length * (2 * math.pi / self.period) ** 2
    
    def render(self):
        ballPos = getPoint((self.x, self.y), math.degrees(self.angle) + 90, self.length)
        pygame.draw.line(self.screen, ROPE_COLOR, (self.x, self.y), ballPos, self.ropeWidth)
        pygame.draw.circle(self.screen, PIVOT_COLOR, (self.x, self.y), self.pivotRadius)
        pygame.draw.circle(self.screen, BALL_COLOR, ballPos, self.radius)
        
    def update(self, dt):
        self.angularAcceleration = -(self.gravity / self.length) * math.sin(self.angle) - self.friction * self.angularVelocity
        self.angularVelocity += self.angularAcceleration * dt
        self.angle += self.angularVelocity * dt

testPendulum = newtonsCradle(WIDTH/2, HEIGHT * 0.2, screen)

running = True
while running:
    dt = clock.tick(FPS)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
    screen.fill(BG_COLOR)
    
    testPendulum.render()
    testPendulum.update(dt)
    
    pygame.display.flip()

pygame.quit()
sys.exit()