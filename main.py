import pygame
import sys
import math
import itertools

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PARTICLE_RADIUS = 5
PARTICLE_MASS = 1e10

# Predefined colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
          (255, 0, 255), (0, 255, 255), (255, 165, 0), (128, 0, 128)]

# Create a color cycle iterator
color_cycle = itertools.cycle(COLORS)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.mass = PARTICLE_MASS
        self.radius = PARTICLE_RADIUS
        self.color = color
        self.vx = 0
        self.vy = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Simulation:
    def __init__(self):
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def update(self):
        G = 6.67430e-11  # Gravitational constant

        for i, p1 in enumerate(self.particles):
            fx, fy = 0, 0
            for j, p2 in enumerate(self.particles):
                if i != j:
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    if distance > p1.radius + p2.radius:
                        force = G * p1.mass * p2.mass / distance ** 2
                        fx += force * dx / distance
                        fy += force * dy / distance

            p1.vx += fx / p1.mass
            p1.vy += fy / p1.mass
            p1.x += p1.vx
            p1.y += p1.vy

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

# Main game loop
running = True
simulation = Simulation()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            color = next(color_cycle)  # Get the next color from the cycle
            particle = Particle(x, y, color)
            simulation.add_particle(particle)

    screen.fill(BLACK)
    simulation.update()
    simulation.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
