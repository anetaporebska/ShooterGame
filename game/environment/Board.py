from game.environment.Field import Field
from game.environment.Wall import Wall
from game.environment.boosters import Boosters
from random import randrange


class Board:
    def __init__(self, width: int, height: int, map_version: int, block_size: int):
        self.height = height
        self.width = width
        self.board = []
        self.block_size = block_size

        if map_version == 1:
            for i in range(width):
                self.board.append([])
                for j in range(height):
                    if i==0 or j==0 or j==height-1 or i==width-1 or (i%4==0 and j%4 !=1 and j%4!=2):
                        self.board[i].append(Wall(i * block_size, j*block_size, block_size))
                    else:
                        self.board[i].append(Field(i*block_size, j*block_size, block_size))

        elif map_version == 2:
            for i in range(width):
                self.board.append([])
                for j in range(height):
                    if i==0 or j==0 or j==height-1 or i==width-1:
                        self.board[i].append(Wall(i * block_size, j*block_size, block_size))
                    else:
                        self.board[i].append(Field(i*block_size, j*block_size, block_size))
        elif map_version == 3:
            for i in range(width):
                self.board.append([])
                for j in range(height):
                    if i==0 or j==0 or j==height-1 or i==width-1 or (i%4==0 and j%4 == 0):
                        self.board[i].append(Wall(i * block_size, j*block_size, block_size))
                    else:
                        self.board[i].append(Field(i*block_size, j*block_size, block_size))

    def draw(self, window):
        for i in range(self.width):
            for j in range(self.height):
                self.board[i][j].draw(window)

    # zwraca informację o tym jaki obiekt znajduje się na danej pozycji
    # x i y są współrzędnymi lewego górnego wierzchołka postaci (w pikselach)
    def check_position(self, x, y):
        board_x = int(x / self.block_size)
        board_y = int(y / self.block_size)
        return self.board[board_x][board_y].get_type()

    def spawn_booster(self,player1,player2):
        for i in range(100):
            x=randrange(0,self.width,1)
            y=randrange(0,self.height,1)
            if self.board[x][y].get_type() == "field" and is_far_enough(self.block_size, x, y, player1, player2):
                self.board[x][y]=Boosters(x*self.block_size,y*self.block_size,self.block_size)
                break

    def get_booster(self,x,y):
        board_x = int(x / self.block_size)
        board_y = int(y / self.block_size)
        boost=self.board[board_x][board_y]
        self.board[board_x][board_y] = Field(board_x*self.block_size,board_y*self.block_size, self.block_size)
        return boost


def is_far_enough(block_size, x, y, player1, player2):
    d=block_size*3
    if (abs(x * block_size - player1.position_x)>d and abs(x * block_size - player2.position_x) > d and
            abs(y * block_size - player1.position_y) >d and abs(y * block_size - player2.position_y) > d):
        return True
    return False

