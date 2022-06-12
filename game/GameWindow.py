import pygame
pygame.init()

INFO_PANEL_HEIGHT = 50
FIELD_SIZE = 40


class GameWindow:
    def __init__(self, window_w, window_h):
        self.__width = window_w
        self.__height = window_h
        self.__game_window = pygame.display.set_mode((window_w * FIELD_SIZE, window_h * FIELD_SIZE + INFO_PANEL_HEIGHT))
        self.__icon = pygame.image.load("images\\icon.png")
        pygame.display.set_icon(self.__icon)
        pygame.display.set_caption("Minesweeper")

    def get_game_window(self):
        return self.__game_window
