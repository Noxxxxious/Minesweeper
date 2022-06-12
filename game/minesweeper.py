from game.Field import Field
from game.GameWindow import GameWindow
import random
import math
import pygame

pygame.init()
pygame.font.init()

font = pygame.font.SysFont('Yu Gothic Medium', 30)
font_color = (150, 150, 150)

dir_x = [1, 0, -1, 0, -1, 1, 1, -1]
dir_y = [0, 1, 0, -1, -1, -1, 1, 1]

mine_image = pygame.image.load("images\\mine.png")
flag_image = pygame.image.load("images\\flag.png")
covered_image = pygame.image.load("images\\covered.png")
number_image = list()
for i in range(0, 8):
    number_image.append(pygame.image.load("images\\" + str(i) + ".png"))
number_image_of = list()
for i in range(0, 7):
    number_image_of.append(pygame.image.load("images\\" + str(i) + "_of.png"))


class Minesweeper:
    def __init__(self, height, width):
        self.__height = height
        self.__width = width
        self.__alive = True
        self.__flagCount = 0
        self.__mineCount = 0
        self.__board = [[Field(False) for x in range(width + 2)] for y in range(height + 2)]
        self.__mineList = list()
        self.__window = GameWindow(height, width)
        self.__firstClick = True

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_alive(self):
        return self.__alive

    def get_board(self):
        return self.__board

    def get_field(self, x, y):
        return self.__board[y][x]

    def set_width(self, width):
        self.__width = width

    def set_height(self, height):
        self.__height = height

    def set_alive(self, alive):
        self.__alive = alive

    def inc_flag_count(self):
        self.__flagCount += 1

    def dec_flag_count(self):
        self.__flagCount -= 1

    def add_mine(self, x, y):
        self.__board[x][y].set_mine(True)
        self.__mineList.append(self.__board[x][y])
        self.__mineCount += 1
        for dx, dy in zip(dir_x, dir_y):
            self.__board[x + dx][y + dy].inc_tangent_mine_count()

    def del_mine(self, x, y):
        self.__board[x][y].set_mine(False)
        self.__mineList.remove(self.__board[x][y])
        self.__mineCount -= 1
        for dx, dy in zip(dir_x, dir_y):
            self.__board[x + dx][y + dy].dec_tangent_mine_count()

    def game_generator(self, x, y):
        for row in range(1, self.__height + 1):
            for col in range(1, self.__width + 1):
                fortune = random.randint(0, 4)
                if not fortune:
                    self.add_mine(row, col)
        if self.__board[x][y].is_mined():
            self.del_mine(x, y)
        for dx, dy in zip(dir_x, dir_y):
            if self.__board[x + dx][y + dy].is_mined():
                self.del_mine(x + dx, y + dy)

    def draw_game(self):
        self.__window.get_game_window().fill((50, 50, 50))
        for i in range(1, self.__height + 1):
            for j in range(1, self.__width + 1):
                x = (i - 1) * 40
                y = (j - 1) * 40
                if self.__board[i][j].is_revealed():
                    if self.__board[i][j].is_mined():
                        image = mine_image
                    elif self.__board[i][j].get_tangent_mine_count() >= self.__board[i][j].get_tangent_flag_count():
                        image = number_image[self.__board[i][j].get_tangent_mine_count()]
                    else:
                        image = number_image_of[self.__board[i][j].get_tangent_mine_count()]
                else:
                    if self.__board[i][j].is_flagged():
                        image = flag_image
                    else:
                        image = covered_image
                self.__window.get_game_window().blit(image, (x, y))
        self.draw_info_panel()
        pygame.display.update()

    def draw_info_panel(self):
        info_surface = font.render("Marked: " + str(self.__flagCount) + " / " + str(self.__mineCount), False, font_color)
        self.__window.get_game_window().blit(info_surface, (10, self.__width * 40 + 10))
        pygame.display.update()

    def reveal(self, x, y):
        if x == 0 or y == 0 or x >= self.__height + 1 or y >= self.__width + 1:
            return
        self.__board[x][y].set_revealed()
        if not self.__board[x][y].is_mined():
            if self.__board[x][y].get_tangent_mine_count() == 0:
                for dx, dy in zip(dir_x, dir_y):
                    if not (self.__board[x + dx][y + dy].is_revealed() or self.__board[x + dx][y + dy].is_flagged()):
                        self.reveal(x + dx, y + dy)
        else:
            self.__alive = False
            for field in self.__mineList:
                field.set_revealed()

    def player_action(self, mouse_pos, mouse_state):
        x = math.floor(mouse_pos[0] / 40) + 1
        y = math.floor(mouse_pos[1] / 40) + 1
        left_click = mouse_state[0]
        right_click = mouse_state[2]
        clicked_field = self.__board[x][y]

        if right_click:
            if not clicked_field.is_revealed():
                clicked_field.toggle_flag()
                if clicked_field.is_flagged():
                    self.inc_flag_count()
                else:
                    self.dec_flag_count()
                for dx, dy in zip(dir_x, dir_y):
                    if not clicked_field.is_flagged():
                        self.__board[x + dx][y + dy].dec_tangent_flag_count()
                    else:
                        self.__board[x + dx][y + dy].inc_tangent_flag_count()
        if left_click:
            if self.__firstClick:
                self.__firstClick = False
                self.game_generator(x, y)
            if not (clicked_field.is_revealed() or clicked_field.is_flagged()):
                self.reveal(x, y)
            elif clicked_field.get_tangent_mine_count() == clicked_field.get_tangent_flag_count():
                for dx, dy in zip(dir_x, dir_y):
                    if not self.__board[x + dx][y + dy].is_flagged():
                        self.reveal(x + dx, y + dy)

    def print_board(self):
        for i in range(1, self.__height + 1):
            for j in range(1, self.__width + 1):
                if self.__board[i][j].is_mined():
                    print("x", end="  ")
                else:
                    print("_", end="  ")
            print("\n")
