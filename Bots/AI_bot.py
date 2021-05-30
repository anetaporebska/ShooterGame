from game.engine.Player import Player
from game.environment.Directions import Direction
from game.engine.weapons import Weapon
import numpy as np

UP = Direction.UP
DOWN = Direction.DOWN
LEFT = Direction.LEFT
RIGHT = Direction.RIGHT


DAMAGE_REWARD = -70  # jeśli zostanie trafiony
MOVE_REWARD = 5      # jeśli zbliży się do przeciwnika, -5 w przeciwnym przypadku
WIN_REWARD = 100     # jeśli wygra rundę, -100 wpp

WIDTH = 20
HEIGHT = 12

# co "widzi" bot:
# - różnicę po x jego i przeciwnika
# - różnicę po y jego i przeciwnika
# - różnicę po x jego i najbliższego pocisku
# - różnicę po y jego i najbliższego pocisku

start_q_table = None

# q_table : pierwsza para współrzędnych różnica po x i y do przeciwnika, druga do najbliższego pocisku


def euclid_dist(dist1, dist2):
    return np.sqrt((dist1[0]-dist2[0])**2 + (dist1[1]-dist2[1])**2)


class AI_bot(Player):
    def __init__(self, HP, initial_position, board, block_size, no, color, enemy, active_bullets, q_table=None):
        super().__init__(HP, initial_position, board, block_size, no, color)
        self.weapons = [Weapon(800, 1, 1, 200, (255, 0, 152))]
        self.enemy = enemy
        self.active_bullets = active_bullets
        self.q_table = q_table
        self.epsilon = 0.7
        self.eps_decay = 0.998
        self.learning_rate = 0.1
        self.discount = 0.95
        if self.q_table is None:
            self.q_table = {}
            for i in range(-WIDTH, WIDTH+1):
                for ii in range(-HEIGHT, HEIGHT+1):
                    for iii in range(-WIDTH, WIDTH+1):
                        for iiii in range(-HEIGHT, HEIGHT+1):
                            self.q_table[((i, ii), (iii, iiii))] = [np.random.uniform(-5, 0) for i in range(5)]

    def dist(self, other):
        return (self.position_x - other.position_x)//self.block_size, \
               (self.position_y - other.position_y)//self.block_size

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
        # jeśli przeciwnik na przeciwko to shoot()
        x = self.position_x
        y = self.position_y
        enemy_x = int(self.enemy.position_x + self.block_size/2)
        enemy_y = int(self.enemy.position_y + self.block_size/2)
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
            return enemy_dist, (WIDTH-1, HEIGHT-1)
        else:
            return enemy_dist, self.dist(min_bullet)

    def run(self):

        life = self.HP
        d = euclid_dist((self.position_x, self.position_y), (self.enemy.position_x, self.enemy.position_y))
        reward = 0

        obs = self.get_observation()
        if np.random.random() > self.epsilon:
            choice = np.argmax(self.q_table[obs])
        else:
            choice = np.random.randint(0, 5)
        self.action(choice)

        if life > self.HP:
            reward += DAMAGE_REWARD
        if not self.is_alive():
            reward -= WIN_REWARD
        if not self.enemy.is_alive():
            reward += WIN_REWARD
        if d > euclid_dist((self.position_x, self.position_y), (self.enemy.position_x, self.enemy.position_y)):
            reward += MOVE_REWARD
        else:
            reward -= MOVE_REWARD
        current_q = self.q_table[obs][choice]
        new_obs = self.get_observation()
        max_future_q = np.max(self.q_table[new_obs])
        new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (reward + self.discount * max_future_q )
        self.q_table[obs][choice] = new_q

    def update_epsilon(self):
        self.epsilon += self.eps_decay

    def set_epsilon(self, eps):
        self.epsilon = eps