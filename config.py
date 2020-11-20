import configparser
import argparse
import textwrap
from space_body import SpaceBody


class Config:
    width = 0
    height = 0
    starts = 0
    display = (0, 0)
    stopOnCollision = True
    star_colors = []
    generators = []

    def __init__(self):
        parser = argparse.ArgumentParser(description='Solar mechanics simulator',
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog=textwrap.dedent('\            '))

        parser.add_argument('-f', '--file',
                            dest='file',
                            default='config.ini',
                            help='configuration file')

        args = parser.parse_args()

        self.config = configparser.ConfigParser()
        self.config.read(args.file)

        sys = self.config['System']
        self.width = int(sys.get("WIN_WIDTH", 800))
        self.height = int(sys.get("WIN_HEIGHT", 640))
        self.stars = int(sys.get("STAR_NUM", 10))

        self.display = (self.width, self.height)

        colors = sys.get("STAR_COLORS")
        self.star_colors = colors.split(',')

        self.space_color = sys.get("SPACE_COLOR")

        self.onCollision = sys.get("ON_COLLISION", "stop")

        gens = sys.get("GENERATORS")

        if gens is not None:
            self.generators = gens.split(',')

    def get_system(self):
        s = []

        for i in self.config.sections():
            if i != "System" and not (i in set(self.generators)):
                obj = SpaceBody(i,
                                int(self.config[i]["Mass"]),
                                float(self.config[i]["X"]),
                                float(self.config[i]["Y"]),
                                float(self.config[i]["VX"]),
                                float(self.config[i]["VY"]))

                obj.set_view_model(int(self.config[i]["R"]),
                                   self.config[i]["color"],
                                   self.space_color)

                s.append(obj)
        return s

    def get_display(self):
        return self.display

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_stars(self):
        return self.stars

    def get_star_colors(self):
        return self.star_colors

    def get_space_color(self):
        return self.space_color
