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

    def isAlive(self):
        if self.HP > 0:
            return True
        return False

    def move(self, change_x, change_y):
        # TODO sprawdzać czy nie wchodzi poza planszę lub w drugiego gracza + czy nie zebrał boosta

        # w tym miejscu sprawdzam lewy górny "wierzchołek gracza"
        upper_object_type = self.board.check_position(self.position_x +change_x * self.movementSpeed,
                                         self.position_y + change_y*self.movementSpeed)

        # prawy dolny wierzchołek
        lower_object_type_= self.board.check_position(self.position_x +change_x * self.movementSpeed + self.block_size,
                                         self.position_y + change_y*self.movementSpeed + self.block_size)

        if upper_object_type == "field" and lower_object_type_=="field":
            self.position_x += change_x*self.movementSpeed
            self.position_y += change_y*self.movementSpeed





    def shoot(self):
        # TODO
        pass

    def draw(self, window):
        pygame.draw.rect(window, (0,255, 0), (self.position_x, self.position_y, self.block_size, self.block_size))
