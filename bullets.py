import pygame


class Bullet:
    def __init__(self, x, y, movement_speed, color, player, orientation):
        # pozycja początkowa pocisku to niech będzie może środek gracza (z tej strony w którą jest skierowany)

        self.position_x = x
        self.position_y = y
        self.movement_speed = movement_speed
        self.color = color # kolor chyba powinna mieć taki jak gracz
        self.size_x = 5
        self.size_y = 5
        self.player = player   # 1 lub 2 w zależności który gracz wystrzelił
        self.orientation = orientation

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.position_x, self.position_y, self.size_x, self.size_y))

    def move(self):
        new_position_x = self.position_x + self.orientation[0]*self.movement_speed
        new_position_y = self.position_y + self.orientation[1]*self.movement_speed
        self.position_x = new_position_x
        self.position_y = new_position_y



class ActiveBullets:
    def __init__(self):
        # TODO docelowo to musi być inna struktura (nie lista), bo musimy w łatwy sposób usuwać/dodawać nowe pociski
        self.bullets = []

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def draw(self, window):
        for bullet in self.bullets:
            bullet.move()
            bullet.draw(window)