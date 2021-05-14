import pygame
from Player import Player
from Board import Board
from bullets import ActiveBullets
from health_bar import HealthBar
from random import random
from Directions import Direction


INITIAL_HP = 100
BOOSTERS_PER_SECOND = 0.1 #Statystycznie

WIDTH = 1000
HEIGHT = 600

INITIAL_POSITION_1 = (51,51)
INITIAL_POSITION_2 = (WIDTH-101,HEIGHT-101)

BLOCK_SIZE = 50

BOARD_WIDTH = int(WIDTH/BLOCK_SIZE)
BOARD_HEIGHT = int(HEIGHT/BLOCK_SIZE)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT+40))    # +20 wysokości na paski życia +20 na amunicję
pygame.display.set_caption("Shooter Game")

FPS = 100

MAP_VERSION = 1

board = Board(BOARD_WIDTH, BOARD_HEIGHT, MAP_VERSION, BLOCK_SIZE)

player1 = Player(INITIAL_HP, INITIAL_POSITION_1, board, BLOCK_SIZE,1, (255, 0, 0))
player2 = Player(INITIAL_HP, INITIAL_POSITION_2, board, BLOCK_SIZE,2, (0, 255, 0))

active_bullets = ActiveBullets()

SHOOT_COOLDOWN = 500
SWITCH_COOLDOWN = 100

player1_health_bar = HealthBar(INITIAL_HP, 50, HEIGHT, player1.color)
player2_health_bar = HealthBar(INITIAL_HP, WIDTH-150, HEIGHT, player2.color)


DOWN = Direction.DOWN
UP = Direction.UP
LEFT = Direction.LEFT
RIGHT = Direction.RIGHT

# player1 - AWSD + Space + left shift
# player2 - arrows + Enter + right shift

player1_shoot_time = None
player2_shoot_time = None
player1_switch_time = None
player2_switch_time = None


def redraw_window():
    board.draw(WINDOW)
    active_bullets.move(board, player1, player2)
    active_bullets.draw(WINDOW)
    player1.draw(WINDOW)
    player2.draw(WINDOW)
    player1_health_bar.update(player1.HP, WINDOW)
    player2_health_bar.update(player2.HP, WINDOW)
    pygame.display.update()


def manage_keys_pressed():

    global player1_shoot_time, player2_shoot_time, player1_switch_time, player2_switch_time

    keys = pygame.key.get_pressed()  # dictionary
    if keys[pygame.K_DOWN]:
        player2.move(DOWN, player1)
    if keys[pygame.K_UP]:
        player2.move(UP, player1)
    if keys[pygame.K_LEFT]:
        player2.move(LEFT, player1)
    if keys[pygame.K_RIGHT]:
        player2.move(RIGHT, player1)
    if keys[pygame.K_RETURN]:
        t = pygame.time.get_ticks()
        if player2_shoot_time + SHOOT_COOLDOWN < t:
            player2.shoot(active_bullets)
            player2_shoot_time = t
    if keys[pygame.K_RSHIFT]:
        t = pygame.time.get_ticks()
        if player2_switch_time + SWITCH_COOLDOWN < t:
            player2.switch_weapon()
            player2_switch_time = t

    if keys[pygame.K_s]:
        player1.move(DOWN, player2)
    if keys[pygame.K_w]:
        player1.move(UP, player2)
    if keys[pygame.K_a]:
        player1.move(LEFT, player2)
    if keys[pygame.K_d]:
        player1.move(RIGHT, player2)
    if keys[pygame.K_SPACE]:
        t = pygame.time.get_ticks()
        if player1_shoot_time + SHOOT_COOLDOWN < t:
            player1.shoot(active_bullets)
            player1_shoot_time = t
    if keys[pygame.K_LSHIFT]:
        t = pygame.time.get_ticks()
        if player1_switch_time + SWITCH_COOLDOWN < t:
            player1.switch_weapon()
            player1_switch_time = t


def run_game():
    run = True

    clock = pygame.time.Clock()

    global player1_shoot_time, player2_shoot_time, player1_switch_time, player2_switch_time

    player1_shoot_time = pygame.time.get_ticks()
    player2_shoot_time = pygame.time.get_ticks()
    player1_switch_time = pygame.time.get_ticks()
    player2_switch_time = pygame.time.get_ticks()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        manage_keys_pressed()

        if not player1.is_alive():
            print("Player 2 won!!!")
            run = False

        if not player2.is_alive():
            print("Player 1 won!!!")
            run = False
        a = random()
        if a < BOOSTERS_PER_SECOND / FPS:
            board.spawn_booster(player1, player2)


