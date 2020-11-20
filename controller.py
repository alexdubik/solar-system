import pygame
from space_body import *

CRASH_DIST = .5
OUT_DIST = 10000
STEPS = 5
R_MIN_MAX = 99999.0
KEY_MOVE_PX = 20


class Controller:
    timer = ""
    cfg = ""
    screen = ""
    bg = ""
    screen_number = 0

    def __init__(self, timer, screen, background, cfg):
        self.timer = timer
        self.cfg = cfg
        self.screen = screen
        self.bg = background

    def run(self):
        r_min = R_MIN_MAX
        r_max = 0.0

        offset_x = 0
        offset_y = 0

        collapsed_object1 = None
        collapsed_object2 = None

        system = self.cfg.get_system()

        done = False
        paused = False
        while not done:
            self.timer.tick(60)
            for e in pygame.event.get():
                if e.type == QUIT:
                    done = True
                    break

            if not paused:
                for st in range(STEPS):
                    for i in system:
                        for j in system:
                            if i.name != j.name:
                                dist = i.dist(j)
                                dist -= (i.radius + j.radius)
                                i.calc_acceleration_to(j)
                                r_max = max(r_min, dist)

                                if dist < r_min:
                                    r_min = dist
                                    collapsed_object1 = i
                                    collapsed_object2 = j

                    if r_min < CRASH_DIST:
                        if self.cfg.onCollision == "stop":
                            done = True
                            print("Collision detected")

                    for i in system:
                        i.update()

                self.screen.blit(self.bg, (0, 0))

                for i in system:
                    i.draw(self.screen, offset_x, offset_y)

                pygame.display.update()

                if r_max > OUT_DIST:
                    print("Out of system")
                    done = True
                    break
