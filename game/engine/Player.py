import pygame
from game.engine.bullets import Bullet
from game.engine.weapons import Weapon
from game.environment.Directions import Direction

INITIAL_SHOOT_DAMAGE = 10


class Player:

    def __init__(self, HP: int, initial_position, board, block_size, no, color):
        self.no = no
        self.maxHP = HP
        self.HP = HP
        self.movementSpeed = 1
        self.movementBoost = 0
        self.shootingSpeed = 1.5
        self.shootingSpeedBoost = 0
        self.orientation = Direction.UP
        self.position_x = initial_position[0]
        self.position_y = initial_position[1]
        self.block_size = block_size
        self.shoot_damage = INITIAL_SHOOT_DAMAGE
        self.board = board
        self.color = color
        self.weapons = [Weapon(200, 1, 1, 100, (255, 0, 152)), Weapon(100, 2, 2, 10, (255, 0, 82)),
                        Weapon(500, 1, 2, 20, (152, 0, 82))]
        self.weapon_idx = 0
        self.current_weapon = self.weapons[self.weapon_idx]
        if self.no == 1:
            self.image = "images/player1.png"
        else:
            self.image = "images/player2.png"
        self.image = pygame.image.load(self.image).convert()
        self.image_LEFT = pygame.transform.flip(self.image, True, False)
        self.image_RIGHT = self.image

        self.image_UP = pygame.transform.rotate(self.image, 90)
        self.image_DOWN = pygame.transform.rotate(self.image, 270)

    def take_damage(self, damage):
        self.HP -= damage

    def is_alive(self):
        return self.HP > 0

    def check_collision(self, new_x, new_y, other_player):
        y = other_player.position_y
        x = other_player.position_x

        lower_right_x = new_x + self.block_size
        lower_right_y = new_y + self.block_size

        if y <= new_y <= y + self.block_size and x <= new_x <= x + self.block_size:
            return True

        if y <= lower_right_y <= y + self.block_size and x <= lower_right_x <= x + self.block_size:
            return True

        if y <= new_y <= y + self.block_size and x <= lower_right_x <= x + self.block_size:
            return True

        if y <= lower_right_y <= y + self.block_size and x <= new_x <= x + self.block_size:
            return True

        return False

    def check_inside_window(self, new_position_x, new_position_y):
        lower_right_x = new_position_x + self.block_size
        lower_right_y = new_position_y + self.block_size

        if new_position_x < 0 or new_position_y < 0:
            return False

        if lower_right_x >= self.board.width * self.block_size or lower_right_y >= self.board.height * self.block_size:
            return False
        return True

    def check_wall(self, new_position_x, new_position_y):
        lower_right_x = new_position_x + self.block_size
        lower_right_y = new_position_y + self.block_size

        upper_left_object_type = self.board.check_position(new_position_x, new_position_y)
        lower_right_object_type = self.board.check_position(lower_right_x, lower_right_y)
        upper_right_object_type = self.board.check_position(new_position_x, lower_right_y)
        lower_left_object_type = self.board.check_position(lower_right_x, new_position_y)

        if upper_left_object_type != "wall" and lower_right_object_type != "wall" \
                and upper_right_object_type != "wall" and lower_left_object_type != "wall":
            return True

        return False

    def use_booster(self, booster):
        if booster.type.get_name() == "healing":
            self.HP += booster.type.get_extraHP(self.maxHP, self.HP)
        elif booster.type.get_name() == "newShoes":
            self.movementSpeed += 0.5
            self.movementBoost = booster.type.get_time()
        elif booster.type.get_name() == "fasterBullets":
            self.shootingSpeed += 0.5
            self.shootingSpeedBoost = booster.type.get_time()
        elif booster.type.get_name() == "extraDamage":
            self.shoot_damage *= 1, 5

    def collect_booster(self, new_position_x, new_position_y):
        lower_right_x = new_position_x + self.block_size
        lower_right_y = new_position_y + self.block_size

        upper_left_object_type = self.board.check_position(new_position_x, new_position_y)
        lower_right_object_type = self.board.check_position(lower_right_x, lower_right_y)
        upper_right_object_type = self.board.check_position(new_position_x, lower_right_y)
        lower_left_object_type = self.board.check_position(lower_right_x, new_position_y)

        if upper_left_object_type == "booster":
            self.use_booster(self.board.get_booster(new_position_x, new_position_y))
        elif lower_right_object_type == "booster":
            self.use_booster(self.board.get_booster(lower_right_x, lower_right_y))
        elif upper_right_object_type == "booster":
            self.use_booster(self.board.get_booster(new_position_x, lower_right_y))
        elif lower_left_object_type == "booster":
            self.use_booster(self.board.get_booster(lower_right_x, new_position_y))

    def move(self, direction, other_player):
        change_x = direction.value[0]
        change_y = direction.value[1]

        self.update_orientation(direction)

        new_position_x = self.position_x + change_x * self.movementSpeed
        new_position_y = self.position_y + change_y * self.movementSpeed

        if self.check_collision(new_position_x, new_position_y, other_player):
            return

        if not self.check_inside_window(new_position_x, new_position_y):
            return

        if not self.check_wall(new_position_x, new_position_y):
            return

        self.collect_booster(new_position_x, new_position_y)
        self.position_x = new_position_x
        self.position_y = new_position_y

    def shoot(self, active_bullets):
        if self.current_weapon.ammunition <= 0:
            return
        x = int(self.position_x + self.block_size / 2)
        y = int(self.position_y + self.block_size / 2)
        speed = self.shootingSpeed * self.current_weapon.speed
        bullet = Bullet(x, y, speed, self.color, self.no, self.orientation, self.current_weapon.range)
        active_bullets.add_bullet(bullet)
        self.current_weapon.use_ammunition()

    def update_orientation(self, direction):
        self.orientation = direction
        if self.orientation == Direction.UP:
            self.image = self.image_UP
        if self.orientation == Direction.DOWN:
            self.image = self.image_DOWN
        if self.orientation == Direction.LEFT:
            self.image = self.image_LEFT
        if self.orientation == Direction.RIGHT:
            self.image = self.image_RIGHT

    def draw(self, window):
        window.blit(self.image, (self.position_x, self.position_y))
        if self.no == 1:
            x = 0
        else:
            x = 700
        self.current_weapon.draw(window, x, 620)

    def check_if_wounded(self, bullet, damage):
        x = bullet.position_x
        y = bullet.position_y

        def point_inside(point_x, point_y):
            return (self.position_x < point_x < self.position_x + self.block_size and
                    self.position_y < point_y < self.position_y + self.block_size)

        if point_inside(x, y) or point_inside(x + bullet.size_x, y) or point_inside(x, y + bullet.size_y) \
                or point_inside(x + bullet.size_x, y + bullet.size_y):
            self.take_damage(damage)
            return True

        return False

    def switch_weapon(self):
        if self.weapon_idx + 1 == len(self.weapons):
            self.weapon_idx = 0
        else:
            self.weapon_idx += 1
        self.current_weapon = self.weapons[self.weapon_idx]

    def get_damage(self):
        return self.shoot_damage * self.current_weapon.damage
