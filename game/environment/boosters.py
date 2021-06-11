from random import randrange
from pygame import image


class RapidFire:
    def __init__(self, time=100):
        self.time = time
        self.image = image.load("images/fire.png").convert()

    @staticmethod
    def get_name():
        return "rapidFire"

    def get_time(self):
        return self.time


class FasterBullets:
    def __init__(self, time=100):
        self.time = time
        self.image = image.load("images/bullets.png").convert()

    @staticmethod
    def get_name():
        return "fasterBullets"

    def get_time(self):
        return self.time


class Healing:
    def __init__(self, HP_rate=4):
        self.HP_rate = HP_rate
        self.image = image.load("images/health.png").convert()

    @staticmethod
    def get_name():
        return "healing"

    def get_extraHP(self, maxHP, currHP):
        if currHP + maxHP / self.HP_rate > maxHP:
            return maxHP - currHP
        return maxHP / self.HP_rate


class NewShoes:
    def __init__(self, time=100):
        self.time = time
        self.image = image.load("images/speed.png").convert()

    @staticmethod
    def get_name():
        return "newShoes"

    def get_time(self):
        return self.time


class Boosters:
    def __init__(self, position_x, position_y, block_size):
        type = randrange(0, 4, 1)
        if type == 0:
            self.type = RapidFire()
        elif type == 1:
            self.type = Healing(100)
        elif type == 2:
            self.type = NewShoes()
        else:
            self.type = FasterBullets()
        self.position_x = position_x
        self.position_y = position_y
        self.block_size = block_size

    def draw(self, window):
        window.blit(self.type.image, (self.position_x, self.position_y))

    @staticmethod
    def get_type():
        return "booster"
