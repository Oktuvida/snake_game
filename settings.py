import pygame


class Display:
    SURFACE: pygame.Surface = None
    CLOCK: pygame.time.Clock = None
    SNAKE_SPEED = 120
    WIDTH = 800
    HEIGHT = WIDTH
    CELL_NUMBER = 20
    CELL_SIZE = WIDTH // CELL_NUMBER
    FONT_SIZE = WIDTH // 17
    FPS = 60
    CAPTION = "Snake Game"

    @staticmethod
    def set_surface() -> None:
        Display.SURFACE = pygame.display.set_mode(
            (Display.WIDTH, Display.HEIGHT))

    @staticmethod
    def set_clock() -> None:
        Display.CLOCK = pygame.time.Clock()

    @staticmethod
    def update() -> None:
        Display.HEIGHT = Display.WIDTH
        Display.FONT_SIZE = Display.WIDTH // 17
        Display.CELL_SIZE = Display.WIDTH // Display.CELL_NUMBER


class Path:
    IMAGES = "./assets/images"
    FONTS = "./assets/fonts"
    SOUNDS = "./assets/sounds"


class FontFamily:
    POETSEN_ONE_REGULAR = f"{Path.FONTS}/PoetsenOne-Regular.ttf"
    DEFAULT = POETSEN_ONE_REGULAR
