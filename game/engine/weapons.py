from pygame import draw


class Weapon:
    def __init__(self, range, damage, speed, ammunition, color):
        self.range = range
        self.damage = damage
        self.speed = speed
        self.max_ammo = ammunition
        self.ammunition = ammunition
        self.color = color

    def use_ammunition(self):
        self.ammunition -= 1

    def add_ammunition(self, amount):
        self.ammunition += amount

    def draw(self, window, x, y):
        size = 300  # szerokość paska na amunicję
        single_width = size // self.max_ammo - 1
        single_height = 20
        draw.rect(window, (0, 0, 0), (x, y, size, single_height))
        for i in range(self.ammunition):
            draw.rect(window, self.color, (x, y, single_width, single_height))
            draw.rect(window, (0, 0, 0), (x, y, 1, single_height))
            x = x + single_width + 1
