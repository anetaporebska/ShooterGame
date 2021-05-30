import pygame
from pygame.locals import *


def end_game(text, col):
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

        try_again = pygame.Rect(150, 200, 200, 50)
        quit_button = pygame.Rect(150, 300, 200, 50)

        pygame.draw.rect(window, (70, 70, 70), try_again)
        pygame.draw.rect(window, (70, 70, 70), quit_button)

        two_player_text = font.render(text, True, col)
        window.blit(two_player_text, (175, 115))

        two_player_text = font.render("Try again?", True, (255, 255, 255))
        window.blit(two_player_text, (175, 215))

        two_player_text = font.render("Quit", True, (255, 255, 255))
        window.blit(two_player_text, (195, 315))

        if try_again.collidepoint((mouse_x, mouse_y)) and click:
            run = False
            pygame.quit()
            from game.gui.welcomeWindow import run_main_menu
            run_main_menu()

        if quit_button.collidepoint((mouse_x, mouse_y)) and click:
            pygame.quit()
            return 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return 0
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)
