import pygame
import math
from collections import deque

WIDTH = 480
HEIGHT = 480
FPS = 30
G = 6.6743e-11
SCALE = 50000
delta_t = 5

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('ptsans', 24)
pygame.display.set_caption("Modeling space")
clock = pygame.time.Clock()


BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]

ship_x = 100000 + 6378137
ship_y = 0
ship_render_x = ship_x // SCALE + WIDTH // 2
ship_render_y = ship_y // SCALE + HEIGHT // 2
ship_velocity_x = 0 * delta_t
ship_velocity_y = 7844 * delta_t
ship_mass = 1000
earth_x = 0
earth_y = 0
earth_radius = 6378137
earth_render_x = earth_x // SCALE + WIDTH // 2
earth_render_y = earth_y // SCALE + HEIGHT // 2
earth_mass = 5.9742e24

orbit_data = deque([(ship_render_x, ship_render_y), (ship_render_x, ship_render_y)])
max_orbit_data_len = 300
line_start_pos_x = ship_render_x
line_start_pos_y = ship_render_y
lines_len = 2


def render(surface):
    surface.fill(BLACK)
    pygame.draw.lines(screen, BLUE, False, orbit_data)
    pygame.draw.circle(surface, GREEN, [earth_render_x, earth_render_y], earth_radius // SCALE, 0)
    pygame.draw.circle(surface, WHITE, [ship_render_x, ship_render_y], 10, 0)

    ship_velocity = math.sqrt(ship_velocity_x ** 2 + ship_velocity_y ** 2)
    distance_from_earth = math.sqrt(ship_x ** 2 + ship_y ** 2)
    img = font.render(f"velocity = {ship_velocity:.10}", True, WHITE)
    screen.blit(img, (20, 20))
    img = font.render(f"altitude = {distance_from_earth:.10}", True, WHITE)
    screen.blit(img, (20, 50))


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                print(f"vx={ship_velocity_x}\nvy={ship_velocity_y}\nx={ship_x}\ny={ship_y}")

    # keys_pressed = pygame.key.get_pressed()
    # if keys_pressed[pygame.K_w]:
    #     ship_velocity_y -= 0.5
    # if keys_pressed[pygame.K_s]:
    #     ship_velocity_y += 0.5
    # if keys_pressed[pygame.K_a]:
    #     ship_velocity_x -= 0.5
    # if keys_pressed[pygame.K_d]:
    #     ship_velocity_x += 0.5

    angle = math.atan2((ship_x - earth_x), (ship_y - earth_y)) + math.pi
    distance = math.sqrt((ship_x - earth_x)**2 + (ship_y - earth_y)**2)
    ship_velocity_x += (math.sin(angle) * G * earth_mass * delta_t**3) / distance**2
    ship_velocity_y += (math.cos(angle) * G * earth_mass * delta_t**3) / distance**2

    ship_render_x = ship_x // SCALE + WIDTH // 2
    ship_render_y = ship_y // SCALE + HEIGHT // 2

    if abs(line_start_pos_x - ship_render_x) >= lines_len or abs(line_start_pos_y - ship_render_y) >= lines_len:
        orbit_data.append((ship_render_x, ship_render_y))
        line_start_pos_x = ship_render_x
        line_start_pos_y = ship_render_y
    if len(orbit_data) > max_orbit_data_len:
        orbit_data.popleft()

    ship_x += ship_velocity_x * delta_t
    ship_y += ship_velocity_y * delta_t

    render(screen)
    pygame.display.flip()
