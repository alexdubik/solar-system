import pygame
import random
from controller import Controller
from space_body import *
from config import *


def main():
    cfg = Config()

    pygame.init()
    screen = pygame.display.set_mode(cfg.get_display())
    pygame.display.set_caption("Solar System")

    bg = Surface(cfg.get_display())
    bg.fill(Color(cfg.get_space_color()))

    for _ in range(cfg.get_stars()):
        draw.circle(bg, Color(random.sample(cfg.get_star_colors(), 1)[0]),
                    (random.randrange(bg.get_width()),
                     random.randrange(bg.get_height())),
                    0)

    timer = pygame.time.Clock()

    control = Controller(timer, screen, bg, cfg)
    control.run()


if __name__ == "__main__":
    main()

