import pygame
from resources.commons import Directions, Vector
from settings import Display, Path


class Images:
    class Fruits:
        APPLE: pygame.Surface = None
        DEFAULT: pygame.Surface = None

        @staticmethod
        def load() -> None:
            Images.Fruits.APPLE = Images.get_image(f"fruits/apple.png")
            Images.Fruits.DEFAULT = Images.Fruits.APPLE

        @staticmethod
        def unload() -> None:
            Images.Fruits.APPLE = None
            Images.Fruits.DEFAULT = None

    class Snake:
        HEAD: dict[tuple[Vector, Vector], pygame.Surface] = None
        BODY: dict[tuple[Vector, Vector], pygame.Surface] = None
        TAIL: dict[tuple[Vector, Vector], pygame.Surface] = None

        @staticmethod
        def load() -> None:
            Images.Snake.HEAD = {
                tuple([Directions.UP, Directions.UP]): Images.get_image('snake/head_up.png'),
                tuple([Directions.DOWN, Directions.DOWN]): Images.get_image('snake/head_down.png'),
                tuple([Directions.LEFT, Directions.LEFT]): Images.get_image('snake/head_left.png'),
                tuple([Directions.RIGHT, Directions.RIGHT]): Images.get_image('snake/head_right.png')
            }
            Images.Snake.BODY = {
                tuple([Directions.UP, Directions.UP]): Images.get_image('snake/body_vertical.png'),
                tuple([Directions.DOWN, Directions.DOWN]): Images.get_image('snake/body_vertical.png'),

                tuple([Directions.LEFT, Directions.LEFT]): Images.get_image('snake/body_horizontal.png'),
                tuple([Directions.RIGHT, Directions.RIGHT]): Images.get_image('snake/body_horizontal.png'),

                tuple([Directions.LEFT, Directions.DOWN]): Images.get_image('snake/body_topleft.png'),
                tuple([Directions.UP, Directions.RIGHT]): Images.get_image('snake/body_topleft.png'),

                tuple([Directions.RIGHT, Directions.DOWN]): Images.get_image('snake/body_topright.png'),
                tuple([Directions.UP, Directions.LEFT]): Images.get_image('snake/body_topright.png'),

                tuple([Directions.LEFT, Directions.UP]): Images.get_image('snake/body_bottomleft.png'),
                tuple([Directions.DOWN, Directions.RIGHT]): Images.get_image('snake/body_bottomleft.png'),

                tuple([Directions.DOWN, Directions.LEFT]): Images.get_image('snake/body_bottomright.png'),
                tuple([Directions.RIGHT, Directions.UP]): Images.get_image('snake/body_bottomright.png')
            }
            Images.Snake.TAIL = {
                tuple([Directions.UP, Directions.UP]): Images.get_image('snake/tail_down.png'),
                tuple([Directions.DOWN, Directions.DOWN]): Images.get_image('snake/tail_up.png'),
                tuple([Directions.LEFT, Directions.LEFT]): Images.get_image('snake/tail_right.png'),
                tuple([Directions.RIGHT, Directions.RIGHT]): Images.get_image('snake/tail_left.png')
            }

        @staticmethod
        def unload() -> None:
            Images.Snake.HEAD = None
            Images.Snake.BODY = None
            Images.Snake.TAIL = None

    @staticmethod
    def scale(image: pygame.Surface, size: tuple = None) -> pygame.Surface:
        if not size:
            return pygame.transform.scale(image, (Display.CELL_SIZE, Display.CELL_SIZE))
        return pygame.transform.scale(image, size)

    @staticmethod
    def get_image(path: str) -> pygame.Surface:
        image = pygame.image.load(f"{Path.IMAGES}/{path}")
        return Images.scale(image)
