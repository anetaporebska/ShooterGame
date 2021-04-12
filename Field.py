import pygame


class Field:
    def __init__(self, x, y, block_size):
        self.position_x = x
        self.position_y = y
        self.block_size = block_size

    def draw(self, window):
        pygame.draw.rect(window, (0,0,0), (self.position_x, self.position_y, self.block_size, self.block_size))

    def get_type(self):
        return "field"

