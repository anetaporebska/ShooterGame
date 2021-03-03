import pygame
from Player import Player
from Board import Board

INITIAL_HP = 100
INITIAL_POSITION_1 = (50,50)
INITIAL_POSITION_2 = (900,900)

WIDTH = 1000
HEIGHT = 1000

BLOCK_SIZE = 50

BOARD_WIDTH = int( WIDTH/BLOCK_SIZE)
BOARD_HEIGHT = int(HEIGHT/BLOCK_SIZE)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

FPS = 100

player1 = Player(INITIAL_HP, INITIAL_POSITION_1)
player2 = Player(INITIAL_HP, INITIAL_POSITION_2)

board = Board(BOARD_HEIGHT, BOARD_WIDTH,2, BLOCK_SIZE)

def redraw_window(): #TODO
    board.draw(WINDOW)
    player1.draw(WINDOW)
    player2.draw(WINDOW)
    pygame.display.update()



# player1 - AWSD + Space
# player2 - arrows + Enter


def run_game():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # TODO: zrobić to ładniej; na razie działa
        keys = pygame.key.get_pressed()     # dictionary
        if keys[pygame.K_DOWN]:
            player2.move(0, 1)
        if keys[pygame.K_UP]:
            player2.move(0, -1)
        if keys[pygame.K_LEFT]:
            player2.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player2.move(1,0)
        if keys[pygame.K_RETURN]:
            player2.shoot()

        if keys[pygame.K_s]:
            player1.move(0, 1)
        if keys[pygame.K_w]:
            player1.move(0, -1)
        if keys[pygame.K_a]:
            player1.move(-1, 0)
        if keys[pygame.K_d]:
            player1.move(1, 0)
        if keys[pygame.K_SPACE]:
            player1.shoot()

        # print(player1.position_x, player1.position_y, player2.position_x, player2.position_y)


run_game()