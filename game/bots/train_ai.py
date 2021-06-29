import pickle
import pygame
from game.player.player import Player
from game.environment.board import Board
from game.player.bullets import ActiveBullets
from game.player.health_bar import HealthBar
from game.environment.directions import Direction
from game.bots.ai_bot import AI_bot
import numpy as np


def run_train_AI():
    initial_hp = 100

    width = 1000
    height = 600

    initial_position_1 = (51, 51)
    initial_position_2 = (width - 101, height - 101)

    block_size = 50

    board_width = int(width / block_size)
    board_height = int(height / block_size)

    window = pygame.display.set_mode((width, height + 40))  # +20 wysokości na paski życia +20 na amunicję
    pygame.display.set_caption("Shooter Game")

    map_version = 2

    board = Board(board_width, board_height, map_version, block_size)

    active_bullets = ActiveBullets()

    player1 = Player(initial_hp, initial_position_1, board, block_size, 1, (255, 0, 0))
    player2 = AI_bot(initial_hp, initial_position_2, board, block_size, 2, (0, 255, 0), player1, active_bullets)
    q_table = player2.q_table

    shoot_cooldown = 250

    player1_health_bar = HealthBar(initial_hp, 50, height, player1.color)
    player2_health_bar = HealthBar(initial_hp, width - 150, height, player2.color)

    DOWN = Direction.DOWN
    UP = Direction.UP
    LEFT = Direction.LEFT
    RIGHT = Direction.RIGHT

    # player1 - AWSD + Space + left shift

    player1_shoot_time = None
    player2_shoot_time = None

    hm_episodes = 1000

    def redraw_window():
        board.draw(window)
        active_bullets.move(board, player1, player2)
        active_bullets.draw(window)
        player1.draw(window)
        player2.draw(window)
        player1_health_bar.update(player1.HP, window)
        player2_health_bar.update(player2.HP, window)
        pygame.display.update()

    def point_inside(x, y, point_x, point_y):
        return x < point_x < x + block_size and y < point_y < y + block_size

    def possible_position(x, y, obj_x, obj_y):
        if point_inside(x, y, obj_x, obj_y) or point_inside(x + block_size, y, obj_x, obj_y) \
                or point_inside(x, y + block_size, obj_x, obj_y) or point_inside(x + block_size, y + block_size, obj_x, obj_y):
            return False
        return True

    def random_moves():
        nonlocal player1_shoot_time
        choice = np.random.randint(0, 4)
        if choice == 0:
            player1.move(UP, player2)
        if choice == 1:
            player1.move(DOWN, player2)
        if choice == 2:
            player1.move(LEFT, player2)
        if choice == 0:
            player1.move(RIGHT, player2)

        t = pygame.time.get_ticks()
        if player1_shoot_time + shoot_cooldown // 2 < t:
            player1.shoot(active_bullets)
            player1_shoot_time = t

    def initialize_players():
        nonlocal player1, player2, q_table

        ai_x = np.random.randint(51, 899)
        ai_y = np.random.randint(51, 499)

        x = np.random.randint(51, 899)
        y = np.random.randint(51, 499)

        while not possible_position(x, y, ai_x, ai_y):
            x = np.random.randint(51, 899)
            y = np.random.randint(51, 499)

        player1 = Player(initial_hp, (x, y), board, block_size, 1, (255, 0, 0))
        player2 = AI_bot(initial_hp, (ai_x, ai_y), board, block_size, 2, (0, 255, 0), player1, active_bullets, q_table)

    def train_AI(ep):
        initialize_players()
        nonlocal player2_shoot_time, player1_shoot_time, active_bullets
        active_bullets = ActiveBullets()

        for i in range(2000):
            player2.run()
            random_moves()
            t = pygame.time.get_ticks()
            if player2_shoot_time + shoot_cooldown < t and player2.shoot_decision():
                player2.shoot(active_bullets)
                player2_shoot_time = t
            if not player1.is_alive() or not player2.is_alive():
                break
            if ep % 100 == 0:
                redraw_window()

    q_tabl = player2.q_table
    player2_shoot_time = pygame.time.get_ticks()
    player1_shoot_time = pygame.time.get_ticks()
    for i in range(hm_episodes):
        print("Episode: ", i + 1, )
        train_AI(i)
        player2.update_epsilon()
    with open("bots/q_table.pickle", "wb") as f:
        pickle.dump(q_tabl, f)
