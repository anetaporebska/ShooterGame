from game.engine.Player import Player
from game.environment.Directions import Direction
from game.engine.weapons import Weapon
import numpy as np

UP = Direction.UP
DOWN = Direction.DOWN
LEFT = Direction.LEFT
RIGHT = Direction.RIGHT

WIDTH = 20
HEIGHT = 12


def euclid_dist(dist1, dist2):
    return np.sqrt((dist1[0] - dist2[0]) ** 2 + (dist1[1] - dist2[1]) ** 2)


class Bot(Player):
    def __init__(self, HP, initial_position, board, block_size, no, color, enemy, active_bullets):
        super().__init__(HP, initial_position, board, block_size, no, color)
        self.weapons = [Weapon(800, 1, 1, 200, (255, 0, 152))]
        self.enemy = enemy
        self.active_bullets = active_bullets

    def dist(self, other):
        return (self.position_x - other.position_x) // self.block_size, \
               (self.position_y - other.position_y) // self.block_size

    def action(self, choice):
        if choice == 0:
            self.move(UP, self.enemy)
        elif choice == 1:
            self.move(DOWN, self.enemy)
        elif choice == 2:
            self.move(LEFT, self.enemy)
        elif choice == 3:
            self.move(RIGHT, self.enemy)
        elif choice == 4:
            pass

    def shoot_decision(self):
        x = self.position_x
        y = self.position_y
        enemy_x = int(self.enemy.position_x + self.block_size / 2)
        enemy_y = int(self.enemy.position_y + self.block_size / 2)
        if self.orientation == UP:
            if enemy_y < y and x < enemy_x < x + self.block_size:
                return True
        elif self.orientation == DOWN:
            if enemy_y > y and x < enemy_x < x + self.block_size:
                return True
        if self.orientation == LEFT:
            if enemy_x < x and y < enemy_y < y + self.block_size:
                return True
        if self.orientation == RIGHT:
            if enemy_x > x and y < enemy_y < y + self.block_size:
                return True
        return False

    def get_observation(self):
        min_dist = 10000
        min_bullet = None

        for bullet in self.active_bullets.bullets:
            if bullet.player == 1:
                e_d = euclid_dist((self.position_x, self.position_y), self.dist(bullet))
                if e_d < min_dist:
                    min_dist = e_d
                    min_bullet = bullet
        enemy_dist = self.dist(self.enemy)

        if min_bullet is None:
            return (enemy_dist, (WIDTH - 1, HEIGHT - 1)), min_bullet
        else:
            return (enemy_dist, self.dist(min_bullet)), min_bullet

    def dodge_bullet(self, bullet, obs):
        if bullet.orientation == RIGHT and self.position_y < bullet.position_y < self.position_y + self.block_size and self.position_x > bullet.position_x:
            self.action(0)
        elif bullet.orientation == LEFT and self.position_y < bullet.position_y < self.position_y + self.block_size and self.position_x < bullet.position_x:
            self.action(1)
        elif bullet.orientation == UP and self.position_x < bullet.position_x < self.position_x + self.block_size and self.position_y < bullet.position_y:
            self.action(3)
        elif bullet.orientation == DOWN and self.position_x < bullet.position_x < self.position_x + self.block_size and self.position_y > bullet.position_y:
            self.action(4)
        else:
            self.move_choice(obs)

    def move_choice(self, obs):
        if abs(obs[0][0]) > abs(obs[0][1]):
            if obs[0][0] > 0:
                self.action(2)
            else:
                self.action(3)
        else:
            if obs[0][1] > 0:
                self.action(0)
            else:
                self.action(1)

    def run(self):
        obs, bullet = self.get_observation()

        if abs(obs[1][0]) + abs(obs[1][1]) <= 3:
            self.dodge_bullet(bullet, obs)
        else:
            self.move_choice(obs)
