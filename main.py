import pygame
import math
from collections import deque
from gravitational_object import GravitationalObject as Gravitational_object

WIDTH = 1250
HEIGHT = 750
FPS = 30
G = 6.6743e-11
SCALE = 1500000
delta_t = 100

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
LIGHT_BLUE = [150, 200, 255]
GREY = [127, 127, 127]

object_list = [Gravitational_object(0, 0, 5.9742e24, 0, 0, 6378137, GREEN),
               Gravitational_object(100000 + 6378137, 0, 1000,  0, 7844, 0, WHITE),
               Gravitational_object(429400000, 0, 7.3477e22,  0, 1023, 1737000, GREY)]
# ship_x = 100000 + 6378137
# ship_y = 0
# ship_render_x = ship_x // SCALE + WIDTH // 2
# ship_render_y = ship_y // SCALE + HEIGHT // 2
# ship_velocity_x = 0
# ship_velocity_y = 7844
# ship_mass = 1000
# earth_x = 0
# earth_y = 0
# earth_radius = 6378137
# earth_render_x = earth_x // SCALE + WIDTH // 2
# earth_render_y = earth_y // SCALE + HEIGHT // 2
# earth_mass = 5.9742e24

# orbit_data = deque([(ship_render_x, ship_render_y), (ship_render_x, ship_render_y)])
# future_orbit_data = deque([(ship_render_x, ship_render_y), (ship_render_x, ship_render_y)])
# max_orbit_data_len = 300
# line_start_pos_x = ship_render_x
# line_start_pos_y = ship_render_y
# lines_len = 2
#
# future_trajectory_steps = 10000
x_offset = 0
y_offset = 0

focus_id = 0


def render(surface):
    surface.fill(BLACK)
    # pygame.draw.lines(surface, BLUE, False, orbit_data)
    # pygame.draw.lines(surface, LIGHT_BLUE, False, future_orbit_data)
    # pygame.draw.circle(surface, GREEN, [earth.x_pos // SCALE + WIDTH // 2, earth.y_pos // SCALE + HEIGHT // 2], earth.radius // SCALE, 0)
    # pygame.draw.circle(surface, WHITE, [ship.x_pos // SCALE + WIDTH // 2, ship.y_pos // SCALE + HEIGHT // 2], 10, 0)
    for object in object_list:
        render_x = (object.x_pos + x_offset) // SCALE + WIDTH // 2
        render_y = (object.y_pos + y_offset) // SCALE + HEIGHT // 2
        pygame.draw.circle(surface, object.color, (render_x, render_y), object.radius // SCALE + (object.radius == 0), 0)
        scaled_data = []
        for i in object.orbit_data:
            scaled_data.append(((i[0] + x_offset) // SCALE + WIDTH // 2, (i[1] + y_offset) // SCALE + HEIGHT // 2))
        pygame.draw.lines(surface, object.color, False, scaled_data)
    ship_velocity = math.sqrt(object_list[1].velocity_x ** 2 + object_list[1].velocity_y ** 2)
    distance_from_earth = math.sqrt(object_list[1].x_pos ** 2 + object_list[1].y_pos ** 2)
    img = font.render(f"velocity = {ship_velocity:.10}", True, WHITE)
    screen.blit(img, (20, 20))
    img = font.render(f"altitude = {distance_from_earth:.10}", True, WHITE)
    screen.blit(img, (20, 50))


# def calc_and_draw_plan(pos):
#     closest = orbit_data[0]
#     for c in orbit_data:
#         dist = abs(c[0] - pos[0]) + abs(c[1] - pos[1])
#         if dist > closest[0] + closest[1]:
#             closest = c
#     if abs(closest[0] - pos[0]) + abs(closest[1] - pos[1]) < 100:
#         pygame.draw.circle(screen, BLUE, closest, 10, 0)


# def get_future_trajectory(force_x=0, force_y=0):
#     global future_orbit_data
#     future_orbit_data = []
#     trajectory_calc_x = ship_x
#     trajectory_calc_y = ship_y
#     trajectory_calc_velocity_x = ship_velocity_x + force_x
#     trajectory_calc_velocity_y = ship_velocity_y + force_y
#     future_line_start_pos_x = ship_render_x
#     future_line_start_pos_y = ship_render_y
#     for i in range(future_trajectory_steps):
#         calc_angle = math.atan2((trajectory_calc_x - earth_x), (trajectory_calc_y - earth_y)) + math.pi
#         calc_distance = math.sqrt((trajectory_calc_x - earth_x) ** 2 + (trajectory_calc_y - earth_y) ** 2)
#         trajectory_calc_velocity_x += (math.sin(calc_angle) * G * earth_mass) / calc_distance ** 2
#         trajectory_calc_velocity_y += (math.cos(calc_angle) * G * earth_mass) / calc_distance ** 2
#         trajectory_calc_x += trajectory_calc_velocity_x
#         trajectory_calc_y += trajectory_calc_velocity_y
#         calc_render_x = trajectory_calc_x // SCALE + WIDTH // 2
#         calc_render_y = trajectory_calc_y // SCALE + HEIGHT // 2
#         if abs(calc_render_x - future_line_start_pos_x) > lines_len or abs(calc_render_y - future_line_start_pos_y) > lines_len:
#             future_orbit_data.append((future_line_start_pos_x, future_line_start_pos_y))
#             future_line_start_pos_x = calc_render_x
#             future_line_start_pos_y = calc_render_y


running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_r:
        #         # print(f"vx={ship_velocity_x}\nvy={ship_velocity_y}\nx={ship_x}\ny={ship_y}")
            if event.key == pygame.K_PLUS:
                focus_id = (focus_id + 1) % len(object_list)
            if event.key == pygame.K_MINUS:
                focus_id = (focus_id - 1) % len(object_list)
        # if event.type == pygame.MOUSEMOTION:
        #     calc_and_draw_plan(event.pos)

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_w]:
        object_list[1].velocity_y -= 100
        # get_future_trajectory(0, 0)
    if keys_pressed[pygame.K_s]:
        object_list[1].velocity_y += 100
        # get_future_trajectory(0, 0)
    if keys_pressed[pygame.K_a]:
        object_list[1].velocity_x -= 100
        # get_future_trajectory(0, 0)
    if keys_pressed[pygame.K_d]:
        object_list[1].velocity_x += 100
        # get_future_trajectory(0, 0)
    if keys_pressed[pygame.K_RIGHT]:
        x_offset -= 5 * SCALE
        # get_future_trajectory(0, 0)
    if keys_pressed[pygame.K_LEFT]:
        x_offset += 5 * SCALE
    if keys_pressed[pygame.K_UP]:
        y_offset += 5 * SCALE
    if keys_pressed[pygame.K_DOWN]:
        y_offset -= 5 * SCALE
    if keys_pressed[pygame.K_i]:
        SCALE /= 1.01
    if keys_pressed[pygame.K_o]:
        SCALE *= 1.01

    for obj1 in object_list:
        for obj2 in object_list:
            if obj1 != obj2:
                obj1.calc_grav_force(obj2.mass, obj2.x_pos, obj2.y_pos, G, delta_t)
        obj1.move_one_step(delta_t, 300000)

    x_offset -= object_list[focus_id].velocity_x * delta_t
    y_offset -= object_list[focus_id].velocity_y * delta_t
    # angle = math.atan2((ship_x - earth_x), (ship_y - earth_y)) + math.pi
    # distance = math.sqrt((ship_x - earth_x)**2 + (ship_y - earth_y)**2)
    # ship_velocity_x += (math.sin(angle) * G * earth_mass * delta_t) / distance**2
    # ship_velocity_y += (math.cos(angle) * G * earth_mass * delta_t) / distance**2

    # ship_render_x = ship_x // SCALE + WIDTH // 2
    # ship_render_y = ship_y // SCALE + HEIGHT // 2

    # if abs(line_start_pos_x - ship_render_x) >= lines_len or abs(line_start_pos_y - ship_render_y) >= lines_len:
    #     orbit_data.append((ship_render_x, ship_render_y))
    #     line_start_pos_x = ship_render_x
    #     line_start_pos_y = ship_render_y
    # if len(orbit_data) > max_orbit_data_len:
    #     orbit_data.popleft()

    # ship_x += ship_velocity_x * delta_t
    # ship_y += ship_velocity_y * delta_t

    render(screen)
    pygame.display.flip()
