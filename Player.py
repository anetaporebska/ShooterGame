INITIAL_SHOOT_DAMAGE = 10


class Player:

    def __init__(self, HP: int, initial_position):
        self.HP = HP
        self.movementSpeed = 1
        self.shootingSpeed = 1
        self.direction = None
        self.position_x = initial_position[0]
        self.position_y = initial_position[1]
        self.shoot_damage = INITIAL_SHOOT_DAMAGE
        # TODO shoot range

    def take_damage(self, damage):
        self.HP -= damage

    def isAlive(self):
        if self.HP > 0:
            return True
        return False

    def move(self, change_x, change_y):
        self.position_x += change_x*self.movementSpeed
        self.position_y += change_y*self.movementSpeed

    def shoot(self):
        # TODO
        pass
