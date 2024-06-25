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
DEFAULT_PARTICLE_MASS = 1e10
MERGE_THRESHOLD = 100  # Number of close interactions before merging

# Predefined colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
          (255, 0, 255), (0, 255, 255), (255, 165, 0), (128, 0, 128)]

# Create a color cycle iterator
color_cycle = itertools.cycle(COLORS)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulator")

class Particle:
    def __init__(self, x, y, mass, color):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = PARTICLE_RADIUS
        self.color = color
        self.vx = 0
        self.vy = 0
        self.close_interactions = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Simulation:
    def __init__(self):
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def remove_particle(self, particle):
        if particle in self.particles:
            self.particles.remove(particle)

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
                    else:
                        p1.close_interactions += 1
                        if p1.close_interactions > MERGE_THRESHOLD:
                            self.merge_particles(p1, p2)

            p1.vx += fx / p1.mass
            p1.vy += fy / p1.mass
            p1.x += p1.vx
            p1.y += p1.vy

    def merge_particles(self, p1, p2):
        if p2 in self.particles:
            p1.mass += p2.mass
            p1.vx = (p1.vx * p1.mass + p2.vx * p2.mass) / (p1.mass + p2.mass)
            p1.vy = (p1.vy * p1.mass + p2.vy * p2.mass) / (p1.mass + p2.mass)
            self.remove_particle(p2)
            p1.close_interactions = 0  # Reset the counter after merging

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def calculate_total_energy(self):
        kinetic_energy = 0
        potential_energy = 0
        G = 6.67430e-11  # Gravitational constant

        for i, p1 in enumerate(self.particles):
            kinetic_energy += 0.5 * p1.mass * (p1.vx ** 2 + p1.vy ** 2)
            for j, p2 in enumerate(self.particles):
                if i != j:
                    dx = p2.x - p1.x
                    dy = p2.y - p1.y
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    potential_energy -= G * p1.mass * p2.mass / distance

        return kinetic_energy, potential_energy

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
            mass = DEFAULT_PARTICLE_MASS  # You can modify this to vary masses
            particle = Particle(x, y, mass, color)
            simulation.add_particle(particle)

    screen.fill(BLACK)
    simulation.update()
    simulation.draw(screen)
    
    # Calculate and display energy
    ke, pe = simulation.calculate_total_energy()
    total_energy = ke + pe
    font = pygame.font.SysFont(None, 24)
    energy_text = font.render(f'KE: {ke:.2e}, PE: {pe:.2e}, Total: {total_energy:.2e}', True, WHITE)
    screen.blit(energy_text, (10, 10))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
