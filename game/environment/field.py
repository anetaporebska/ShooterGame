import pygame


class Field:
    def __init__(self, x, y, block_size):
        self.position_x = x
        self.position_y = y
        self.block_size = block_size

    def draw(self, window):
        pygame.draw.rect(window, (64, 64, 64), (self.position_x, self.position_y, self.block_size, self.block_size))

    @staticmethod
    def get_type():
        return "field"

