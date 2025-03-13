import pygame
from Params import *


class Bonds:

    def __init__(self):
        self.List = []

    class Bond:
        def __init__(self, surface, circle1, circle2):
            self.surface = surface
            self.circle1 = circle1
            self.circle2 = circle2

        def render(self):
            c1_coords = self.circle1.get_coords()
            c2_coords = self.circle2.get_coords()
            pygame.draw.line(self.surface, BOND_OUTLINE_COLOR_2, c1_coords, c2_coords, BOND_OUTLINE_WIDTH_2)
            pygame.draw.line(self.surface, BOND_OUTLINE_COLOR_1, c1_coords, c2_coords, BOND_OUTLINE_WIDTH_1)
            pygame.draw.line(self.surface, BOND_COLOR_3, c1_coords, c2_coords, BOND_WIDTH)

        def get_circles(self):
            return [self.circle1, self.circle2]

    def add(self, surface, circle1, circle2):
        self.List.append(self.Bond(surface, circle1, circle2))

    def list(self):
        return self.List

    def render(self):
        for bond in self.list():
            bond.render()
