from Field import Field
from Wall import Wall

"""
w Board będziemy mieć wszystkie obiekty z mapy i na każdym z nich podczas przerysowywania mapy będę wywoływać draw()

w aktualnej wersji Board jest 20x20, a okno aplikacji 1000x1000, każdy obiekt na mapie ma 50x50

proponuję, żeby w Board trzymać wszystkie obiekty poza Player, bo jemu wtedy możemy pozwolić na większy zakres ruchów -
może się przesuwać co 1 piksel; reszta obiektów może leżeć w tych kwadracikach wyznaczanych przez Board

"""

class Board:
    def __init__(self, width: int, height: int, mapVersion: int):
        self.height=height
        self.width=width
        self.board=[]
        for i in range(width):
            self.board.append([])
#        TODO: wygenerowanie najlepiej paru plansz, w sensie wstawienie scian
        if(mapVersion == 1):
            for row in self.board:
                for j in range(height):
                    row.append(Field(False, None, None)) # proponuję zamiast Field wstawiać rzeczywiste obiekty typu Player, Wall etc
                                                        # każdy obiekt mógłby mieć metodę get_type() która zwracała by np. stringa

        # to jest jakaś przykładowa mapa, która ma ściany na obrzeżach
        elif(mapVersion==2):
            for i in range(len(self.board)):
                for j in range(height):
                    if i==0 or j==0 or i==height-1 or j==width-1:
                        self.board[i].append(Wall(i*50, j*50))
                    else:
                        self.board[i].append(Field(False, i*50, j*50))

    def draw(self, window):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j].draw(window)




