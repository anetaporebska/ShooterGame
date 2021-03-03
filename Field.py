import pygame

class Field:
    def __init__(self,isWall, x, y):
        #TODO ?: pole FieldType mozna sie niby pobawic np w wode, 
        #przechodzenie przez ktora by spowalnialo, albo jakies rozne kolory plansz?
        self.isWall=isWall
        self.booster=None
        self.player=None
        self.position_x = x
        self.position_y = y

    def is_empty(self):
        if(not self.isWall and self.booster==None and self.player==None):
            return True
        return False

    def is_wall(self):
        return self.isWall

    def is_booster(self):
        return self.booster==None

    def is_player(self):
        return self.player==None

    def draw(self, window):
        pygame.draw.rect(window, (0,0,0), (self.position_x, self.position_y, 50, 50))

    #TODO: Stworzenie tekstur, no na pewno zrobiłbym coś na gracza i boostery, może ściany i podłoże
