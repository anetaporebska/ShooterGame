import pygame

class Field:
    def __init__(self, x, y, block_size):
        #TODO ?: pole FieldType mozna sie niby pobawic np w wode, 
        #przechodzenie przez ktora by spowalnialo, albo jakies rozne kolory plansz?
        self.position_x = x
        self.position_y = y
        self.block_size = block_size

    def draw(self, window):
        pygame.draw.rect(window, (0,0,0), (self.position_x, self.position_y, self.block_size, self.block_size))

    def get_type(self):
        return "field"

    #TODO: Stworzenie tekstur, no na pewno zrobiłbym coś na gracza i boostery, może ściany i podłoże
