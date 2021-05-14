import pygame


class Field:
    def __init__(self, x, y, block_size):
        self.position_x = x
        self.position_y = y
        self.block_size = block_size
        #self.image = pygame.image.load("images/field.png")

    def draw(self, window):
        #window.blit(self.image, (self.position_x, self.position_y))
        pygame.draw.rect(window, (169,169,169), (self.position_x, self.position_y, self.block_size, self.block_size))

    def get_type(self):
        return "field"

