from game.minesweeper import Minesweeper
import pygame
pygame.init()

a = Minesweeper(30, 20)
playing = True
while playing:
    a.draw_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            a.player_action(pygame.mouse.get_pos(), pygame.mouse.get_pressed())
