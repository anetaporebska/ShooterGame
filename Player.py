import pygame
from bullets import Bullet
INITIAL_SHOOT_DAMAGE = 10


class Player:

    def __init__(self, HP: int, initial_position, board, block_size, no, color):
        self.no = no    # numer gracza (1 lub 2)
        self.HP = HP
        self.movementSpeed = 1
        self.shootingSpeed = 1
        self.orientation = (0,1)   # orientacja, w która stronę jest zwrócony (zależna od ostatniego ruchu)
        self.position_x = initial_position[0]
        self.position_y = initial_position[1]
        self.block_size = block_size
        self.shoot_damage = INITIAL_SHOOT_DAMAGE
        # TODO shoot range?
        self.board = board
        self.color = color

    def take_damage(self, damage):
        self.HP -= damage

    def is_alive(self):
        if self.HP > 0:
            return True
        return False

    def move(self, change_x, change_y):
        # TODO sprawdzać czy nie wchodzi w drugiego gracza + czy nie zebrał boosta
        self.update_orientation(change_x, change_y)

        new_position_x = self.position_x + change_x * self.movementSpeed
        new_position_y = self.position_y + change_y*self.movementSpeed

        lower_right_x = new_position_x+self.block_size
        lower_right_y = new_position_y + self.block_size

        # czy nie wychodzi poza mapę (okienko)
        # lewy górny
        if new_position_x < 0 or new_position_y < 0:
            return

        # prawy dolny
        if lower_right_x >= self.board.width*self.block_size or lower_right_y >= self.board.height*self.block_size:
            return

        # w tym miejscu sprawdzam lewy górny "wierzchołek gracza"
        upper_object_type = self.board.check_position(new_position_x, new_position_y)

        # prawy dolny wierzchołek
        lower_object_type = self.board.check_position(lower_right_x, lower_right_y)

        if upper_object_type == "field" and lower_object_type == "field":
            self.position_x = new_position_x
            self.position_y = new_position_y


    def shoot(self, active_bullets):
        x = int(self.position_x + self.block_size/2)
        y = int(self.position_y + self.block_size/2)
        bullet = Bullet(x, y, self.shootingSpeed, self.color, self.no, self.orientation)
        active_bullets.add_bullet(bullet)

    def update_orientation(self, x, y):
        self.orientation = (x,y)

    def draw(self, window):
        pygame.draw.rect(window, self.color , (self.position_x, self.position_y, self.block_size, self.block_size))

    def check_if_wounded(self, bullet, damage):
        x = bullet.position_x
        y = bullet.position_y

        def point_inside(point_x, point_y):
            return (self.position_x < point_x < self.position_x + self.block_size and
                    self.position_y < point_y < self.position_y + self.block_size)

        if point_inside(x, y) or point_inside(x + bullet.size_x, y) or point_inside(x, y+bullet.size_y) \
                or point_inside(x + bullet.size_x, y + bullet.size_y):
            self.take_damage(damage)
            return True

        return False
