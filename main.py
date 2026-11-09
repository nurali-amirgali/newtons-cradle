import pygame
import sys
import math

WIDTH = 600
HEIGHT = 400
FPS = 120

BG_COLOR = (40, 40, 40) #(237, 235, 240)
PIVOT_COLOR = (122, 121, 115) #83, 81, 87
ROPE_COLOR = (255,255,255) #175, 172, 181
BALL_COLOR = (255,255,255) #49, 48, 51
BALL_OUTLINE = (0,0,0)

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

def isCircleColliding(pointA, radiusA, pointB, radiusB):
    distance = math.dist(pointA, pointB)
    return distance <= radiusA + radiusB

class newtonsCradle:
    def __init__(self, x, y, screen, numPendulums = 7, radius = 20, length = 150, 
                 mass = 10, period = 1.5, pivotRadius = 10, ropeWidth = 13):
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
        
        self.collisionIterations = 3
        self.restitution = 0.999
        
        self.lastMouseState = False
        self.lastMousePos = (0,0)
        self.dragging = False
        self.dragIndex = 0
    
        self.initPendulums()
        #self.pendulums[-1].angle = math.radians(-40)
        #self.pendulums[0].angle = math.radians(35)
        #self.pendulums[1].angle = math.radians(25)
        #self.pendulums[2].angle = math.radians(15)
    
    def initPendulums(self):
        for i in range(self.numPendulums):
            x = self.x + (i * self.radius * 2)
            newPendulum = pendulum(x, self.y, self.screen, self.radius, self.length, 
                                   self.mass, self.pivotRadius, self.ropeWidth, self.period)
            self.pendulums.append(newPendulum)
    
    def update(self, dt):
        dt = min(dt, 1/30)
        steps = 8
        self.handleMouse()
        for _ in range(steps):
            for i, p in enumerate(self.pendulums):
                if self.dragging and i == self.dragIndex:
                    continue
                p.update(dt / steps)
            self.collisionCheck()
    
    def render(self):
        for pendulumObj in self.pendulums:
            pendulumObj.render()
    
    def startDrag(self):
        self.dragging = True
        
    def endDrag(self):
        self.dragging = False
            
    def handleMouse(self):
        mouseButtons = pygame.mouse.get_pressed()
        
        if mouseButtons[0] != self.lastMouseState:
            if mouseButtons[0]:
                x, y = pygame.mouse.get_pos()
                for i, pendulumObj in enumerate(self.pendulums):
                    ballPos = pendulumObj.getBallPos()
                    distance = math.dist(ballPos, (x, y))
                    
                    if distance <= self.radius:
                        print("startDrag")     
                        self.startDrag()
                        self.dragIndex = i
                        break
            else:
                print("endDrag")
                self.endDrag()
            
        self.lastMouseState = mouseButtons[0]
        if self.dragging:
            pendulumObj = self.pendulums[self.dragIndex]
            pendulumObj.angularVelocity = 0
            x, y = pendulumObj.x, pendulumObj.y
            mouseX, mouseY = pygame.mouse.get_pos()
            
            dx = x - mouseX
            dy = y - mouseY
            
            angleRad = math.atan2(dx, -dy) #+ math.radians(90)
            angleRad = min(max(angleRad, math.radians(-90)), math.radians(90))
            
            pendulumObj.angle = angleRad
            
    def collisionCheck(self):
        for _ in range(self.collisionIterations):
            for i in range(self.numPendulums - 1):
                current = self.pendulums[i]
                next = self.pendulums[i + 1]

                currentPos = current.getBallPos()
                nextPos = next.getBallPos()

                distance = math.dist(currentPos, nextPos)
                overlap = (self.radius * 2) - distance
                if overlap <= 0:
                    continue
                
                correction = overlap / 2 / self.length
                if self.dragging and i != self.dragIndex:
                    current.angle += correction
                if self.dragging and (i + 1) != self.dragIndex:
                    next.angle -= correction
                
                if current.angularVelocity >= next.angularVelocity:
                    continue
                
                if self.dragging and i != self.dragIndex:
                    continue
                
                m1, m2 = current.mass, next.mass
                w1, w2 = current.angularVelocity, next.angularVelocity
                total = m1 + m2
                momentum = m1 * w1 + m2 * w2
                
                current.angularVelocity = (momentum + m2 * self.restitution * (w2 - w1)) / total
                next.angularVelocity = (momentum + m1 * self.restitution * (w1 - w2)) / total

class pendulum:
    def __init__(self, x, y, screen, radius = 20, length = 150, mass = 10, pivotRadius = 10, 
                 ropeWidth = 10, period = 1.5, friction = 0.005):
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
        self.friction = friction 
        self.gravity = length * (2 * math.pi / self.period) ** 2
    
    def getBallPos(self):
        return getPoint((self.x, self.y), math.degrees(self.angle) + 90, self.length)
    
    def render(self):
        ballPos = self.getBallPos()
        pygame.draw.line(self.screen, BALL_OUTLINE, (self.x, self.y), ballPos, self.ropeWidth)
        pygame.draw.line(self.screen, ROPE_COLOR, (self.x, self.y), ballPos, self.ropeWidth - 4)
        
        pygame.draw.circle(self.screen, PIVOT_COLOR, (self.x, self.y), self.pivotRadius)
        pygame.draw.circle(self.screen, BALL_OUTLINE, (self.x, self.y), self.pivotRadius, width=2)
        
        pygame.draw.circle(self.screen, BALL_COLOR, ballPos, self.radius)
        pygame.draw.circle(self.screen, BALL_OUTLINE, ballPos, self.radius, width=2)
        
    def update(self, dt):
        self.angularAcceleration = -(self.gravity / self.length) * math.sin(self.angle) - self.friction * self.angularVelocity
        self.angularVelocity += self.angularAcceleration * dt
        self.angle += self.angularVelocity * dt

numBalls = 7
ballRadius = 20
testPendulum = newtonsCradle(WIDTH/2 - (ballRadius * numBalls * 2)/2 + ballRadius, HEIGHT * 0.3, screen, numPendulums = numBalls, radius = ballRadius)

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