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
        self.player = player   # 1 lub 2 w zależności który gracz wystrzelił pocisk
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
        self.bullets = set()

    def add_bullet(self, bullet):
        self.bullets.add(bullet)

    def remove_bullet(self, bullet):
        self.bullets.remove(bullet)

    def move(self, board, player1, player2):
        bullets_to_delete = set()
        for bullet in self.bullets:
            bullet.move()
            if board.check_position(bullet.position_x, bullet.position_y) == "wall":
                bullets_to_delete.add(bullet)

            if bullet.player == 1 and player2.check_if_wounded(bullet, player1.shoot_damage):
                bullets_to_delete.add(bullet)
            elif bullet.player == 2 and player1.check_if_wounded(bullet, player2.shoot_damage):
                bullets_to_delete.add(bullet)

        for bullet in bullets_to_delete:
            self.bullets.remove(bullet)

    def draw(self, window):
        for bullet in self.bullets:
            bullet.draw(window)

