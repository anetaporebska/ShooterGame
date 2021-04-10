from random import randrange
from pygame import draw

class RapidFire:
    def __init__(self, time=100):
        self.time = time
        self.color = (0, 125, 225)
    def get_name(self):
        return "rapidFire"
    def get_time(self):
        return self.time


class FasterBullets:
    def __init(self,time=100):
        self.time = time
        self.color = (125,125,125)
        def get_name(self):
            return "fasterBullets"
        def get_time(self):
            return self.time


class Healing:
    def __init__(self,HP_rate=4):
        self.color = (0, 125, 0) #ciemnozielony
        self.HP_rate=HP_rate #określa przez ile dzielimy maxHP
    def get_name(self):
        return "healing"
    def get_extraHP(self,maxHP,currHP):
        if currHP + maxHP/self.HP_rate > maxHP:
            return maxHP - currHP
        return maxHP/self.HP_rate


class NewShoes:
    def __init__(self, time=100):
        self.time = time
        self.color = (225, 225, 0)#Żółty
    def get_name(self):
        return "newShoes"
    def get_time(self):
        return self.time


class Boosters:
    def __init__(self, position_x, position_y, block_size):
        type = randrange(0, 4, 1)
        if type == 0:
            self.type=RapidFire()
        elif type == 1:
            self.type=Healing(100)
        else:
            self.type = NewShoes()
        self.position_x = position_x
        self.position_y = position_y
        self.block_size = block_size
    def draw(self, window):
        draw.rect(window, self.type.color, (self.position_x, self.position_y, self.block_size, self.block_size))
    def get_type(self):
        return "booster"
