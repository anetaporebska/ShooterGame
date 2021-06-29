import pygame
import pickle

from game.bots.ai_bot import AI_bot
from game.player.player import Player
from game.environment.board import Board
from game.player.bullets import ActiveBullets
from game.player.health_bar import HealthBar
from random import random
from game.environment.directions import Direction
from game.gui.finish_window import end_game


DOWN = Direction.DOWN
UP = Direction.UP
LEFT = Direction.LEFT
RIGHT = Direction.RIGHT


def run_game(bot=None, map=1):
    player1 = None
    player2 = None
    player1_health_bar = None
    player2_health_bar = None
    q_table = None
    board = None

    initial_hp = 100
    boosters_per_second = 0.1

    width = 1000
    height = 600

    initial_position_1 = (51, 51)
    initial_position_2 = (width - 101, height - 101)

    block_size = 50
    board_width = int(width / block_size)
    board_height = int(height / block_size)

    window = pygame.display.set_mode((width, height + 40))
    pygame.display.set_caption("Shooter Game")

    fps = 100
    active_bullets = ActiveBullets()
    shoot_cooldown = 500
    switch_cooldown = 100

    player1_shoot_time = None
    player2_shoot_time = None
    player1_switch_time = None
    player2_switch_time = None

    board = Board(board_width, board_height, map, block_size)

    def initialize_bot_game(bot):
        nonlocal player1, player2, player1_health_bar, player2_health_bar, q_table, board

        player1 = Player(initial_hp, initial_position_1, board, block_size, 1, (255, 175, 0))

        if bot == AI_bot:
            with open("game/bots/q_table.pickle", "rb") as f:
                q_table = pickle.load(f)
            player2 = bot(initial_hp, initial_position_2, board, block_size, 2, (54, 52, 255), player1, active_bullets)
            q_table = player2.q_table
        else:
            player2 = bot(initial_hp, initial_position_2, board, block_size, 2, (54, 52, 255), player1, active_bullets)

    def initialize_game():
        nonlocal player1, player2, player1_health_bar, player2_health_bar, board

        player1 = Player(initial_hp, initial_position_1, board, block_size, 1, (255, 175, 0))
        player2 = Player(initial_hp, initial_position_2, board, block_size, 2, (54, 52, 255))

    def redraw_window():
        window.fill((0, 0, 0))
        board.draw(window)
        active_bullets.move(board, player1, player2)
        active_bullets.draw(window)
        player1.draw(window)
        player2.draw(window)
        player1_health_bar.update(player1.HP, window)
        player2_health_bar.update(player2.HP, window)
        pygame.display.update()

    def manage_keys_pressed():

        nonlocal player1_shoot_time, player2_shoot_time, player1_switch_time, player2_switch_time
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
            if player1_shoot_time + shoot_cooldown < t:
                player1.shoot(active_bullets)
                player1_shoot_time = t
        if keys[pygame.K_LSHIFT]:
            t = pygame.time.get_ticks()
            if player1_switch_time + switch_cooldown < t:
                player1.switch_weapon()
                player1_switch_time = t

        if not bot:
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
                if player2_shoot_time + shoot_cooldown < t:
                    player2.shoot(active_bullets)
                    player2_shoot_time = t
            if keys[pygame.K_RSHIFT]:
                t = pygame.time.get_ticks()
                if player2_switch_time + switch_cooldown < t:
                    player2.switch_weapon()
                    player2_switch_time = t

    def run_players():
        run = True

        clock = pygame.time.Clock()

        nonlocal player1_shoot_time, player2_shoot_time, player1_switch_time, player2_switch_time

        player1_shoot_time = pygame.time.get_ticks()
        player2_shoot_time = pygame.time.get_ticks()
        player1_switch_time = pygame.time.get_ticks()
        player2_switch_time = pygame.time.get_ticks()

        while run:
            clock.tick(fps)
            redraw_window()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            manage_keys_pressed()
            if bot:
                t = pygame.time.get_ticks()
                if player2_shoot_time + shoot_cooldown < t and player2.shoot_decision():
                    player2.shoot(active_bullets)
                    player2_shoot_time = t
                player2.run()

            if not player1.is_alive():
                pygame.quit()
                end_game("Player 2 won!", player2.color)
                run = False

            if not player2.is_alive():
                pygame.quit()
                end_game("Player 1 won!", player1.color)
                run = False
            a = random()
            if a < boosters_per_second / fps:
                board.spawn_booster(player1, player2)

    if bot:
        initialize_bot_game(bot)
    else:
        initialize_game()

    player1_health_bar = HealthBar(initial_hp, 50, height, player1.color)
    player2_health_bar = HealthBar(initial_hp, width - 150, height, player2.color)

    if bot == AI_bot:
        q_table = player2.q_table
        player2.set_epsilon(0.1)

    run_players()

    if bot == AI_bot:
        with open("bots/q_table.pickle", "wb") as f:
            pickle.dump(q_table, f)