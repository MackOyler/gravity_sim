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
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = int(math.sqrt(mass) / 1000)  # Radius based on mass
        self.color = (min(255, int(mass / 1e9)), 0, 255 - min(255, int(mass / 1e9)))  # Color based on mass
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
            mass = 1e10 + pygame.mouse.get_pressed()[0] * 1e11  # Adjust mass based on mouse button
            particle = Particle(x, y, mass)
            simulation.add_particle(particle)

    screen.fill(BLACK)
    simulation.update()
    simulation.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
