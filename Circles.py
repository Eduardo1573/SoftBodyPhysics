import pygame
from Params import *

class Circles:

    def __init__(self):
        self.List = []

    class Circle:

        def __init__(self, surface, x, y):
            self.surface = surface
            self.x = x
            self.y = y
            self.X = x
            self.Y = y
            self.state = 'Under_Cursor'
            self.net = []
            self.forces = 0, 0
            self.neighbors = []

        def get_coords(self):
            return self.x, self.y

        def set_state(self, new_state):
            self.state = new_state

        def set_coords(self, x, y):
            self.x = x
            self.y = y
            self.X = x
            self.Y = y

        def move(self, x, y):
            self.x = x
            self.y = y

        def render(self):
            if self.state == 'None':
                pygame.draw.circle(self.surface, CIRCLE_COLOR, (self.x, self.y), CIRCLE_RADIUS)
            elif self.state == 'Under_Cursor':
                pygame.draw.circle(self.surface, OUTLINE_COLOR_1, (self.x, self.y), OUTLINE_RADIUS)
                pygame.draw.circle(self.surface, CIRCLE_COLOR, (self.x, self.y), CIRCLE_RADIUS)
            elif self.state == 'Captured':
                pygame.draw.circle(self.surface, OUTLINE_COLOR_2, (self.x, self.y), OUTLINE_RADIUS)
                pygame.draw.circle(self.surface, CIRCLE_COLOR, (self.x, self.y), CIRCLE_RADIUS)
            # elif self.state == ''



    def add(self, surface, x, y):
        self.List.append(self.Circle(surface, x, y))

    def list(self):
        return self.List

    def render(self):
        for circle in self.list():
            circle.render()
