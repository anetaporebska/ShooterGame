import pygame


class Wall:
    def __init__(self, x, y, block_size):
        self.position_x = x
        self.position_y = y
        self.block_size = block_size
        self.image = pygame.image.load("images/wall.png").convert()

    def draw(self, window):
        window.blit(self.image, (self.position_x, self.position_y))

    @staticmethod
    def get_type():
        return "wall"
