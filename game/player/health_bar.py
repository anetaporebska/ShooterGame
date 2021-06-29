from pygame import draw


class HealthBar:
    def __init__(self, max_hp, x, y, color):
        self.max_hp = max_hp
        self.hp = max_hp
        self.position_x = x
        self.position_y = y
        self.size_x = 100
        self.size_y = 20
        self.color = color

    def draw(self, window):
        draw.rect(window, (0,0,0), (self.position_x, self.position_y, self.size_x, self.size_y))
        width = int(self.hp * 100 / self.max_hp)
        draw.rect(window, self.color, (self.position_x, self.position_y, width , self.size_y))

    def update(self, hp, window):
        self.hp = hp
        self.draw(window)