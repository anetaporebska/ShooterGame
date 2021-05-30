import pygame
from pygame.locals import *
from game.engine.Game import run_game
from QBot.AI_game import run_AI_game
from Bot1.Bot1 import Bot


def main_menu():
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("Shooter game")
    window = pygame.display.set_mode((500, 500))
    click = False
    run = True

    font = pygame.font.SysFont('Constantia', 20)

    while run:
        window.fill((0, 0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        two_player_game = pygame.Rect(150, 100, 200, 50)
        simple_bot_game = pygame.Rect(150, 200, 200, 50)
        AI_bot_game = pygame.Rect(150, 300, 200, 50)

        pygame.draw.rect(window, (69, 69, 69), two_player_game)
        pygame.draw.rect(window, (69, 69, 69), simple_bot_game)
        pygame.draw.rect(window, (69, 69, 69), AI_bot_game)

        two_player_text = font.render("Two players game", True, (255, 255, 255))
        window.blit(two_player_text, (175, 115))

        two_player_text = font.render("Simple bot game", True, (255, 255, 255))
        window.blit(two_player_text, (175, 215))

        two_player_text = font.render("AI bot game", True, (255, 255, 255))
        window.blit(two_player_text, (175, 315))

        if two_player_game.collidepoint((mouse_x, mouse_y)) and click:
            run = False
            run_game()

        if simple_bot_game.collidepoint((mouse_x, mouse_y)) and click:
            run = False
            run_AI_game(Bot)

        if AI_bot_game.collidepoint((mouse_x, mouse_y)) and click:
            run = False
            run_AI_game()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)
