import pygame
INITIAL_SHOOT_DAMAGE = 10


class Player:

    def __init__(self, HP: int, initial_position, board, block_size):
        self.HP = HP
        self.movementSpeed = 1
        self.shootingSpeed = 1
        self.direction = None
        self.position_x = initial_position[0]
        self.position_y = initial_position[1]
        self.block_size = block_size
        self.shoot_damage = INITIAL_SHOOT_DAMAGE
        # TODO shoot range?
        self.board = board

    def take_damage(self, damage):
        self.HP -= damage

    def is_alive(self):
        if self.HP > 0:
            return True
        return False

    def move(self, change_x, change_y):
        # TODO sprawdzać czy nie wchodzi w drugiego gracza + czy nie zebrał boosta
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



    def shoot(self):
        # TODO
        pass

    def draw(self, window):
        pygame.draw.rect(window, (0,255, 0), (self.position_x, self.position_y, self.block_size, self.block_size))
