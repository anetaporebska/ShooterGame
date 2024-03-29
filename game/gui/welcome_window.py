import pygame
from pygame.locals import *
from game.engine.game import run_game
from game.bots.simple_bot import Bot
from game.bots.ai_bot import AI_bot


def run_main_menu():
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

        pygame.draw.rect(window, (70, 70, 70), two_player_game)
        pygame.draw.rect(window, (70, 70, 70), simple_bot_game)
        pygame.draw.rect(window, (70, 70, 70), AI_bot_game)

        two_player_text = font.render("Two player game", True, (255, 255, 255))
        window.blit(two_player_text, (175, 115))

        two_player_text = font.render("Simple bot game", True, (255, 255, 255))
        window.blit(two_player_text, (175, 215))

        two_player_text = font.render("AI bot game", True, (255, 255, 255))
        window.blit(two_player_text, (195, 315))

        if two_player_game.collidepoint((mouse_x, mouse_y)) and click:
            run = False
            pygame.quit()
            run_game()

        if simple_bot_game.collidepoint((mouse_x, mouse_y)) and click:
            run = False
            pygame.quit()
            run_game(Bot)

        if AI_bot_game.collidepoint((mouse_x, mouse_y)) and click:
            run = False
            pygame.quit()
            run_game(AI_bot)

        if run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return 0
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
        pygame.display.update()
        clock.tick(50)
