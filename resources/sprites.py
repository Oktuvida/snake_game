import pygame
from collections import deque
from enum import Enum
from random import randint
from resources.commons import Colors, Directions, Vector
from resources.images import Images
from settings import Display, FontFamily, Path


class Fruit:
    def __init__(self) -> None:
        self.position: Vector | pygame.Rect = None

    def draw(self, display: pygame.Surface) -> None:
        if self.position is None:
            self.randomize()
        if isinstance(self.position, pygame.Rect):
            display.blit(Images.Fruits.DEFAULT, self.position)
        else:
            display.blit(Images.Fruits.DEFAULT,
                         self.position * Display.CELL_SIZE)

    def randomize(self) -> None:
        self.position = Vector(
            randint(0, Display.CELL_NUMBER - 1), randint(0, Display.CELL_NUMBER - 1))


class Snake:
    class Component:
        class Type(Enum):
            HEAD = 0
            BODY = 1
            TAIL = 2

        def __init__(self, position: Vector, direction: list[Vector, Vector], type: Type) -> None:
            self.position = position
            self.direction = direction
            self.type = type

        def draw(self, display: pygame.Surface) -> None:
            match self.type:
                case self.type.HEAD:
                    display.blit(Images.Snake.HEAD[tuple(
                        self.direction)], self.position * Display.CELL_SIZE)
                case self.Type.BODY:
                    display.blit(Images.Snake.BODY[tuple(
                        self.direction)], self.position * Display.CELL_SIZE)
                case self.type.TAIL:
                    display.blit(Images.Snake.TAIL[tuple(
                        self.direction)], self.position * Display.CELL_SIZE)

    def __init__(self) -> None:
        self.direction = Vector(0, 0)
        initial_direction = Directions.LEFT
        initial_position = Vector(
            Display.CELL_NUMBER // 6, Display.CELL_NUMBER // 2)
        self.body = deque([
            self.Component(initial_position, [
                           initial_direction] * 2, self.Component.Type.HEAD),
            self.Component(initial_position + (1, 0),
                           [initial_direction] * 2, self.Component.Type.BODY),
            self.Component(initial_position + (2, 0),
                           [initial_direction] * 2, self.Component.Type.TAIL)
        ])
        self.fruit_eaten = False
        self.crunch_fruit = pygame.mixer.Sound(
            f"{Path.SOUNDS}/crunch_fruit.wav")

    def draw(self, display: pygame.Surface) -> None:
        for component in self.body:
            component.draw(display)

    def move(self) -> None:
        if self.direction == Vector(0, 0):
            return
        self.body.appendleft(self.Component(Vector(
            self.body[0].position + self.direction) % Display.CELL_NUMBER, [self.direction] * 2, self.Component.Type.HEAD))
        self.body[1].direction = [self.direction, self.body[2].direction[0]]
        self.body[1].type = self.Component.Type.BODY
        if self.fruit_eaten:
            self.fruit_eaten = False
            self.crunch_fruit.play()
        else:
            self.body.pop()
            self.body[-1].direction = [self.body[-1].direction[0]] * 2
            self.body[-1].type = self.Component.Type.TAIL

    def set_direction(self, key: pygame.key) -> None:
        if key in Directions.BY_KEY and not self.body[0].direction[0] + Directions.BY_KEY[key] == Vector(0, 0):
            self.direction = Directions.BY_KEY[key]


class ScoreBox:
    def __init__(self) -> None:
        self.score = 0
        self.fruit = Fruit()

    def draw(self, display: pygame.Surface) -> None:
        font = pygame.font.Font(
            f"{FontFamily.DEFAULT}", Display.FONT_SIZE)
        render = font.render(str(self.score), 1, Colors.PRIMARY_BLACK)
        render_rect = render.get_rect(center=Vector(
            Display.CELL_NUMBER - 1, Display.CELL_NUMBER - 1) * Display.CELL_SIZE)
        self.fruit.position = Images.Fruits.DEFAULT.get_rect(
            midright=(render_rect.left, render_rect.centery))

        display.blit(render, render_rect)
        self.fruit.draw(display)
