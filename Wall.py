import pygame


class Wall:
    def __init__(self, x, y, block_size):
        self.position_x = x
        self.position_y = y
        self.color = (255, 255, 255)
        self.block_size = block_size

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.position_x, self.position_y, self.block_size, self.block_size))

    @staticmethod
    def get_type():
        return "wall"
