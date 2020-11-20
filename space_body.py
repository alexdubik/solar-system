from pygame import *
import math

DELTA_T = 0.01


class SpaceBody:
    mass = 0.0
    x, y, vx, vy, ax, ay = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    radius = 0.0
    color = "black"
    space_color = "black"
    others = []
    image = ""
    name = ''

    def __init__(self, name, mass, x, y, vx, vy):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.name = name
        self.others = []

        print("{0}, ({1}, {2}) v=({3}, {4}), mass={5}".format(name, x, y, vx, vy, mass))

    def set_view_model(self, r, color, space_color):
        self.radius = r
        self.space_color = space_color
        self.color = color
        self.image = Surface((r * 2, r * 2))
        self.image.fill(Color(space_color))
        draw.circle(self.image, Color(color), (r, r), r)

    def dist(self, other):
        return math.hypot((self.x - other.x),
                          (self.y - other.y))

    def calc_acceleration_to(self, other):
        self.others.append((other.mass, other.x, other.y))

    def fx(self, local_x):
        a = 0
        for (mass, x, y) in self.others:
            r = math.hypot(x - local_x, y - self.y)
            a += mass * (x - local_x) / r ** 3

        return a

    def fy(self, local_y):
        a = 0
        for (mass, x, y) in self.others:
            r = math.hypot(x - self.x, y - local_y)
            a += mass * (y - local_y) / r ** 3

        return a

    def calc_x(self):
        k1 = DELTA_T * self.fx(self.x)
        q1 = DELTA_T * self.vx

        k2 = DELTA_T * self.fx(self.x + q1 / 2)
        q2 = DELTA_T * (self.vx + k1 / 2)

        k3 = DELTA_T * self.fx(self.x + q2 / 2)
        q3 = DELTA_T * (self.vx + k2 / 2)

        k4 = DELTA_T * self.fx(self.x + q3)
        q4 = DELTA_T * (self.vx + k3)

        self.vx += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.x += (q1 + 2 * q2 + 2 * q3 + q4) / 6

    def calc_y(self):
        k1 = DELTA_T * self.fy(self.y)
        q1 = DELTA_T * self.vy

        k2 = DELTA_T * self.fy(self.y + q1 / 2)
        q2 = DELTA_T * (self.vy + k1 / 2)

        k3 = DELTA_T * self.fy(self.y + q2 / 2)
        q3 = DELTA_T * (self.vy + k2 / 2)

        k4 = DELTA_T * self.fy(self.y + q3)
        q4 = DELTA_T * (self.vy + k3)

        self.vy += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        self.y += (q1 + 2 * q2 + 2 * q3 + q4) / 6

    def update(self):
        self.calc_x()
        self.calc_y()
        self.others.clear()

        print("{0}, ({1}, {2}) v=({3}, {4}), mass={5}".format(self.name, self.x, self.y, self.vx, self.vy, self.mass))

    def draw(self, screen, offset_x=0, offset_y=0):
        screen.blit(self.image, (int(self.x - self.radius) + offset_x, int(self.y - self.radius) + offset_y))
