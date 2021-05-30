import pickle
import pygame
from game.engine.Player import Player
from game.environment.Board import Board
from game.engine.bullets import ActiveBullets
from game.engine.health_bar import HealthBar
from random import random
from game.environment.Directions import Direction
from QBot.AI_bot import AI_bot

player1 = None
player2 = None
player1_health_bar = None
player2_health_bar = None
q_table = None
board = None
MAP_VERSION = None

INITIAL_HP = 100
BOOSTERS_PER_SECOND = 0.1 #Statystycznie

WIDTH = 1000
HEIGHT = 600

INITIAL_POSITION_1 = (51, 51)
INITIAL_POSITION_2 = (WIDTH-101, HEIGHT-101)

BLOCK_SIZE = 50
BOARD_WIDTH = int(WIDTH/BLOCK_SIZE)
BOARD_HEIGHT = int(HEIGHT/BLOCK_SIZE)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT+40))    # +20 wysokości na paski życia +20 na amunicję
pygame.display.set_caption("Shooter Game")

FPS = 100
active_bullets = ActiveBullets()
SHOOT_COOLDOWN = 500
SWITCH_COOLDOWN = 100


DOWN = Direction.DOWN
UP = Direction.UP
LEFT = Direction.LEFT
RIGHT = Direction.RIGHT

# player1 - AWSD + Space + left shift

player1_shoot_time = None
player2_shoot_time = None
player1_switch_time = None


def initialize_game(bot):
    global player1, player2, player1_health_bar, player2_health_bar, q_table, board

    board = Board(BOARD_WIDTH, BOARD_HEIGHT, MAP_VERSION, BLOCK_SIZE)
    player1 = Player(INITIAL_HP, INITIAL_POSITION_1, board, BLOCK_SIZE, 1, (255, 175, 0))

    if bot == AI_bot:
        with open("QBot/q_table.pickle", "rb") as f:
            q_table = pickle.load(f)
        player2 = bot(INITIAL_HP, INITIAL_POSITION_2, board, BLOCK_SIZE, 2, (54, 52, 255), player1, active_bullets)
        q_table = player2.q_table
    else:
        player2 = bot(INITIAL_HP, INITIAL_POSITION_2, board, BLOCK_SIZE, 2, (54, 52, 255), player1, active_bullets)

    player1_health_bar = HealthBar(INITIAL_HP, 50, HEIGHT, player1.color)
    player2_health_bar = HealthBar(INITIAL_HP, WIDTH - 150, HEIGHT, player2.color)


def redraw_window():
    WINDOW.fill((0, 0, 0))
    board.draw(WINDOW)
    active_bullets.move(board, player1, player2)
    active_bullets.draw(WINDOW)
    player1.draw(WINDOW)
    player2.draw(WINDOW)
    player1_health_bar.update(player1.HP, WINDOW)
    player2_health_bar.update(player2.HP, WINDOW)
    pygame.display.update()


def manage_keys_pressed():

    global player1_shoot_time, player2_shoot_time, player1_switch_time

    keys = pygame.key.get_pressed()  # dictionary

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
    t = pygame.time.get_ticks()
    if player2_shoot_time + SHOOT_COOLDOWN < t and player2.shoot_decision():
        player2.shoot(active_bullets)
        player2_shoot_time = t


def run_game():
    run = True

    clock = pygame.time.Clock()

    global player1_shoot_time, player2_shoot_time, player1_switch_time

    player1_shoot_time = pygame.time.get_ticks()
    player2_shoot_time = pygame.time.get_ticks()
    player1_switch_time = pygame.time.get_ticks()

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        manage_keys_pressed()
        player2.run()

        if not player1.is_alive():
            print("Player 2 won!!!")
            run = False

        if not player2.is_alive():
            print("Player 1 won!!!")
            run = False
        a = random()
        if a < BOOSTERS_PER_SECOND / FPS:
            board.spawn_booster(player1, player2)


def run_AI_game(bot=AI_bot, map=1):
    global player1, player2, q_table, MAP_VERSION
    MAP_VERSION = map
    initialize_game(bot)
    if bot == AI_bot:
        q_table = player2.q_table
        player2.set_epsilon(0.1)
    run_game()

    if bot == AI_bot:
        with open("QBot/q_table.pickle", "wb") as f:
            pickle.dump(q_table, f)
