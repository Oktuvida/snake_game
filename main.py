#!/usr/bin/env python3.10
import pygame
from resources.game import Game
from resources.menus import GameOverMenu, MainMenu, ResolutionMenu, SettingsMenu
from settings import Display


class SnakeGame:
    def __init__(self) -> None:
        pygame.mixer.pre_init()
        pygame.init()
        Display.set_surface()
        Display.set_clock()

        self.actual_resolution = Display.SURFACE.get_size()
        self.game = Game()
        self.main_menu = MainMenu()
        self.settings = SettingsMenu()
        self.resolution = ResolutionMenu()
        self.game_over = GameOverMenu()

        pygame.display.set_caption(Display.CAPTION)

    def check_resolution(self) -> None:
        if Display.SURFACE.get_size() != self.actual_resolution:
            self.actual_resolution = Display.SURFACE.get_size()
            self.main_menu = MainMenu()
            self.settings = SettingsMenu()
            self.resolution = ResolutionMenu()
            self.game_over = GameOverMenu()

    def run(self) -> None:
        while True:
            self.check_resolution()
            self.game.run()
            self.main_menu.run()
            self.settings.run()
            self.resolution.run()
            self.game_over.run()


if __name__ == "__main__":
    snake_game = SnakeGame()
    snake_game.run()
