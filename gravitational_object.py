from collections import deque


class GravitationalObject:
    def __init__(self, x_pos, y_pos, mass, velocity_x, velocity_y, radius, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.radius = radius
        self.color = color
        self.orbit_data = deque([(x_pos, y_pos), (x_pos, y_pos)])

    def calc_grav_force(self, mass, x, y, g, delta_time):
        dist_2 = (self.x_pos - x) ** 2 + (self.y_pos - y) ** 2
        dist = dist_2 ** 0.5
        self.velocity_x += ((x - self.x_pos) * mass * g * delta_time) / (dist_2 * dist)
        self.velocity_y += ((y - self.y_pos) * mass * g * delta_time) / (dist_2 * dist)

    def move_one_step(self, delta_time, lines_len=0):
        self.x_pos += self.velocity_x * delta_time
        self.y_pos += self.velocity_y * delta_time
        if lines_len and (self.orbit_data[-1][0] - self.x_pos) ** 2 + (self.orbit_data[-1][1] - self.y_pos) ** 2 > lines_len ** 2:
            self.orbit_data.append((self.x_pos, self.y_pos))
            if len(self.orbit_data) > 1000:
                self.orbit_data.popleft()
