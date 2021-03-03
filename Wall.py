import pygame


class Wall:
    def __init__(self, x, y):
        self.position_x = x
        self.position_y = y
        self.color = (255, 255, 255)

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.position_x, self.position_y, 50, 50))