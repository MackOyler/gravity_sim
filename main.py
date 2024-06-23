import pygame
import sys
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

class Particle:
    def __init__(self, x, y, mass, radius):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.vx = 0
        self.vy = 0

    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
    
class Simulation:
    def __init__(self):
        self.particles = []
    
    def add_particle(self, particle):
        pass
    
    def update(self):
        #need to set gravitational constant; add for loop
        pass
    
    def draw(self, screen):
        pass
    
# Need main game loop
running = True
simulation = Simulation()

while running:
    pass