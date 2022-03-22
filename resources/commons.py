import pygame
import sys
from pygame.math import Vector2
from settings import Display, FontFamily


class Vector(Vector2):
    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __mod__(self, number: int) -> 'Vector':
        return Vector(self.x % number, self.y % number)


class Functions:
    @staticmethod
    def exit() -> None:
        pygame.quit()
        sys.exit()

    @staticmethod
    def update_display() -> None:
        pygame.display.update()
        Display.CLOCK.tick(Display.FPS)


class Colors:
    PRIMARY_WHITE = (240, 240, 240)
    PRIMARY_BLACK = (30, 30, 30)
    PRIMARY_GREEN = (175, 215, 70)
    SECONDARY_GREEN = (167, 209, 61)


class TextBox:
    def __init__(self, text: str, font: pygame.font.Font, color: tuple, position: Vector) -> None:
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.render = self.font.render(self.text, 1, self.color)
        self.render_rect = self.render.get_rect(center=self.position)

    def draw(self, display: pygame.Surface) -> None:
        display.blit(self.render, self.render_rect)

    def update(self) -> None:
        self.render = self.font.render(self.text, 1, self.color)
        self.render_rect = self.render.get_rect(center=self.position)


class Button:
    def __init__(self, text: str, position: Vector) -> None:
        self.font = pygame.font.Font(FontFamily.DEFAULT, Display.FONT_SIZE)
        self.position = position
        self.size = Vector(self.font.size(text))
        self.text_box = TextBox(
            text, self.font, Colors.PRIMARY_BLACK, self.position)
        self.background = pygame.Rect(0, 0, *self.size * 1.1)
        self.background.center = self.position
        self.collide = False

    def draw(self, display: pygame.Surface) -> None:
        if self.collide:
            pygame.draw.rect(display, Colors.PRIMARY_BLACK,
                             self.background, 0, 5)
            self.text_box.color = Colors.PRIMARY_WHITE
        else:
            self.text_box.color = Colors.PRIMARY_BLACK
        self.text_box.draw(display)

    def update(self) -> None:
        self.text_box.update()
        size = Vector(self.font.size(self.text_box.text))
        if self.size != size:
            self.size = size
            self.background = pygame.Rect(0, 0, *self.size * 1.1)
            self.background.center = self.position

    def is_colliding(self, rect: pygame.Rect, save_value: bool = True) -> bool:
        collide = self.text_box.render_rect.colliderect(rect)
        if save_value:
            self.collide = collide
        return collide

    def set_text(self, text: str) -> None:
        self.text_box.text = text


class Backgrounds:
    class Grass:
        def __init__(self) -> None:
            self.surface = pygame.Surface(
                (Display.WIDTH, Display.HEIGHT))
            self.surface_rect = self.surface.get_rect(
                center=(Display.WIDTH / 2, Display.HEIGHT / 2))
            self.surface.fill(Colors.PRIMARY_GREEN)
            self.rects = [pygame.Rect(col * Display.CELL_SIZE, row * Display.CELL_SIZE, Display.CELL_SIZE, Display.CELL_SIZE)
                          for row in range(Display.CELL_NUMBER) for col in range(row % 2, Display.CELL_NUMBER, 2)]

        def draw(self, display: pygame.Surface) -> None:
            display.blit(self.surface, self.surface_rect)
            for rect in self.rects:
                pygame.draw.rect(display, Colors.SECONDARY_GREEN, rect)

        def update(self) -> None:
            if self.surface.get_width() != Display.WIDTH:
                self.__init__()


class Mouse(pygame.Rect):
    def __init__(self) -> None:
        super().__init__(0, 0, 1, 1)
        self.buttoms_pressed: list[int] = None

    def update(self) -> None:
        self.buttoms_pressed = pygame.mouse.get_pressed()
        self.left, self.top = pygame.mouse.get_pos()


class Directions:
    UP = Vector(0, -1)
    DOWN = Vector(0, 1)
    RIGHT = Vector(1, 0)
    LEFT = Vector(-1, 0)
    BY_KEY = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_RIGHT: RIGHT,
        pygame.K_LEFT: LEFT
    }
