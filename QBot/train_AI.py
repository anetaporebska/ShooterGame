import pickle
import pygame
from Player import Player
from Board import Board
from bullets import ActiveBullets
from health_bar import HealthBar
from Directions import Direction
from QBot.AI_bot import AI_bot
import numpy as np

INITIAL_HP = 100

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

MAP_VERSION = 2

board = Board(BOARD_WIDTH, BOARD_HEIGHT, MAP_VERSION, BLOCK_SIZE)

active_bullets = ActiveBullets()

clock = pygame.time.Clock()

player1 = Player(INITIAL_HP, INITIAL_POSITION_1, board, BLOCK_SIZE,1, (255, 0, 0))
player2 = AI_bot(INITIAL_HP, INITIAL_POSITION_2, board, BLOCK_SIZE,2, (0, 255, 0), player1, active_bullets)
q_table = player2.q_table

SHOOT_COOLDOWN = 250
SWITCH_COOLDOWN = 100

player1_health_bar = HealthBar(INITIAL_HP, 50, HEIGHT, player1.color)
player2_health_bar = HealthBar(INITIAL_HP, WIDTH-150, HEIGHT, player2.color)


DOWN = Direction.DOWN
UP = Direction.UP
LEFT = Direction.LEFT
RIGHT = Direction.RIGHT

# player1 - AWSD + Space + left shift

player1_shoot_time = None
player2_shoot_time = None
player1_switch_time = None


def redraw_window():
    board.draw(WINDOW)
    active_bullets.move(board, player1, player2)
    active_bullets.draw(WINDOW)
    player1.draw(WINDOW)
    player2.draw(WINDOW)
    player1_health_bar.update(player1.HP, WINDOW)
    player2_health_bar.update(player2.HP, WINDOW)
    pygame.display.update()


HM_EPISODES = 1000


def point_inside(x, y, point_x, point_y):
    return x < point_x < x + BLOCK_SIZE and y < point_y < y + BLOCK_SIZE


def possible_position(x, y, obj_x, obj_y):
    if point_inside(x, y, obj_x, obj_y) or point_inside(x + BLOCK_SIZE, y, obj_x, obj_y) or point_inside(x, y + BLOCK_SIZE, obj_x, obj_y) or point_inside(x + BLOCK_SIZE, y + BLOCK_SIZE, obj_x, obj_y):
        return False
    return True


def random_moves():
    global player1_shoot_time
    choice = np.random.randint(0,4)
    if choice == 0:
        player1.move(UP, player2)
    if choice == 1:
        player1.move(DOWN, player2)
    if choice == 2:
        player1.move(LEFT, player2)
    if choice == 0:
        player1.move(RIGHT, player2)

    t = pygame.time.get_ticks()
    if player1_shoot_time + SHOOT_COOLDOWN//2 < t:
        player1.shoot(active_bullets)
        player1_shoot_time = t


def initialize_players():
    global player1, player2, q_table

    ai_x = np.random.randint(51, 899)
    ai_y = np.random.randint(51, 499)

    x = np.random.randint(51, 899)
    y = np.random.randint(51, 499)

    while not possible_position(x, y, ai_x, ai_y):
        x = np.random.randint(51, 899)
        y = np.random.randint(51, 499)

    player1 = Player(INITIAL_HP, (x,y), board, BLOCK_SIZE, 1, (255, 0, 0))
    player2 = AI_bot(INITIAL_HP, (ai_x, ai_y), board, BLOCK_SIZE, 2, (0, 255, 0), player1, active_bullets, q_table)


def train_AI(ep):
    initialize_players()
    global player2_shoot_time, player1_shoot_time, active_bullets
    active_bullets = ActiveBullets()

    for i in range(2000): # ruchów do zakończenia rundy
        player2.run()
        random_moves()
        t = pygame.time.get_ticks()
        if player2_shoot_time + SHOOT_COOLDOWN < t and player2.shoot_decision():
            player2.shoot(active_bullets)
            player2_shoot_time = t
        if not player1.is_alive() or not player2.is_alive():
            break
        if ep % 100 == 0:
            redraw_window()


def run_train_AI():
    global player1, player2, player1_shoot_time, player2_shoot_time
    q_tabl = player2.q_table
    player2_shoot_time = pygame.time.get_ticks()
    player1_shoot_time = pygame.time.get_ticks()
    for i in range(HM_EPISODES):
        print("Episode: ", i+1, )
        train_AI(i)
        player2.update_epsilon()
    with open("q_table.pickle", "wb") as f:
        pickle.dump(q_tabl, f)


