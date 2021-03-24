import pygame
from Player import Player
from Board import Board
from bullets import ActiveBullets
from health_bar import HealthBar

INITIAL_HP = 100
INITIAL_POSITION_1 = (50,475)
INITIAL_POSITION_2 = (900,475)

WIDTH = 1000
HEIGHT = 1000

BLOCK_SIZE = 50

BOARD_WIDTH = int(WIDTH/BLOCK_SIZE)
BOARD_HEIGHT = int(HEIGHT/BLOCK_SIZE)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT+20))    # +20 wysokości na paski życia
pygame.display.set_caption("Shooter Game")

FPS = 100

MAP_VERSION = 2

board = Board(BOARD_HEIGHT, BOARD_WIDTH,MAP_VERSION, BLOCK_SIZE)

player1 = Player(INITIAL_HP, INITIAL_POSITION_1, board, BLOCK_SIZE,1, (255, 0, 0))
player2 = Player(INITIAL_HP, INITIAL_POSITION_2, board, BLOCK_SIZE,2, (0, 255, 0))

active_bullets = ActiveBullets()

SHOOT_COOLDOWN = 500

player1_health_bar = HealthBar(INITIAL_HP, 50, 1000, player1.color)
player2_health_bar = HealthBar(INITIAL_HP, 850, 1000, player2.color)


def redraw_window():
    board.draw(WINDOW)
    active_bullets.move(board, player1, player2)
    active_bullets.draw(WINDOW)
    player1.draw(WINDOW)
    player2.draw(WINDOW)

    player1_health_bar.update(player1.HP, WINDOW)
    player2_health_bar.update(player2.HP, WINDOW)

    pygame.display.update()



# player1 - AWSD + Space
# player2 - arrows + Enter


def run_game():
    run = True

    clock = pygame.time.Clock()

    player1_shoot_time = pygame.time.get_ticks()
    player2_shoot_time = pygame.time.get_ticks()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # TODO: zrobić to ładniej; na razie działa
        keys = pygame.key.get_pressed()     # dictionary
        if keys[pygame.K_DOWN]:
            player2.move(0, 1, player1)
        if keys[pygame.K_UP]:
            player2.move(0, -1, player1)
        if keys[pygame.K_LEFT]:
            player2.move(-1, 0, player1)
        if keys[pygame.K_RIGHT]:
            player2.move(1,0, player1)
        if keys[pygame.K_RETURN]:
            t = pygame.time.get_ticks()
            if player2_shoot_time + SHOOT_COOLDOWN < t:
                player2.shoot(active_bullets)
                player2_shoot_time = t

        if keys[pygame.K_s]:
            player1.move(0, 1, player2)
        if keys[pygame.K_w]:
            player1.move(0, -1, player2)
        if keys[pygame.K_a]:
            player1.move(-1, 0, player2)
        if keys[pygame.K_d]:
            player1.move(1, 0, player2)
        if keys[pygame.K_SPACE]:
            t = pygame.time.get_ticks()
            if player1_shoot_time + SHOOT_COOLDOWN < t:
                player1.shoot(active_bullets)
                player1_shoot_time = t

        if not player1.is_alive():
            print("Player 2 won!!!")
            run = False

        if not player2.is_alive():
            print("Player 1 won!!!")
            run = False


