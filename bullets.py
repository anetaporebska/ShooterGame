import pygame


class Bullet:
    def __init__(self, x, y, movement_speed, color):
        # pozycja początkowa pocisku to niech będzie może środek gracza (z tej strony w którą jest skierowany)

        self.position_x = x
        self.position_y = y
        self.movement_speed = movement_speed
        self.color = color # kolor chyba powinna mieć taki jak gracz
        self.size_x = 2
        self.size_y = 2

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.position_x, self.position_y, self.size_x, self.size_y))


class ActiveBullets:
    def __init__(self):
        # TODO docelowo to musi być inna struktura (nie lista), bo musimy w łatwy sposób usuwać/dodawać nowe pociski
        self.bullets = []

    def add_bullet(self, bullet):
        self.bullets.append(bullet)