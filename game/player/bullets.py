import pygame


class Bullet:
    def __init__(self, x, y, movement_speed, color, player, orientation, range):
        self.position_x = x
        self.position_y = y
        self.movement_speed = movement_speed
        self.color = color
        self.size_x = 5
        self.size_y = 5
        self.player = player
        self.orientation = orientation
        self.range = range
        self.distance = 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.position_x, self.position_y, self.size_x, self.size_y))

    def move(self):
        new_position_x = self.position_x + self.orientation.value[0]*self.movement_speed
        new_position_y = self.position_y + self.orientation.value[1]*self.movement_speed
        self.position_x = new_position_x
        self.position_y = new_position_y
        self.distance = self.distance + abs(self.orientation.value[0]*self.movement_speed + self.orientation.value[1]*self.movement_speed)


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

            if bullet.distance >= bullet.range:
                bullets_to_delete.add(bullet)
            damage1 = player1.get_damage()
            damage2 = player2.get_damage()
            if bullet.player == 1 and player2.check_if_wounded(bullet, damage1):
                bullets_to_delete.add(bullet)
            elif bullet.player == 2 and player1.check_if_wounded(bullet, damage2):
                bullets_to_delete.add(bullet)

        for bullet in bullets_to_delete:
            self.bullets.remove(bullet)

    def draw(self, window):
        for bullet in self.bullets:
            bullet.draw(window)

