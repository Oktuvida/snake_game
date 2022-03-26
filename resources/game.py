import pygame
from itertools import islice
from resources.commons import Backgrounds, Functions
from resources.images import Images
from resources.menus import MainMenu
from resources.sprites import Fruit, ScoreBox, Snake
from resources.state import GameState, State
from settings import Display


class Game:
    def __init__(self) -> None:
        self.background = Backgrounds.Grass()
        self.fruit = Fruit()
        self.snake = Snake()
        self.score_box = ScoreBox()

        self.time_to_update = False
        self.snake_updater = pygame.USEREVENT
        pygame.time.set_timer(self.snake_updater, Display.SNAKE_SPEED)

    def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.QUIT:
                Functions.exit()
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        State.GAME = GameState.MENU
                    case _:
                        self.snake.set_direction(event.key)
            case self.snake_updater:
                self.time_to_update = True

    def draw(self) -> None:
        self.background.draw(Display.SURFACE)
        self.score_box.draw(Display.SURFACE)
        self.fruit.draw(Display.SURFACE)
        self.snake.draw(Display.SURFACE)

    def update(self) -> None:
        self.background.update()
        if self.time_to_update:
            self.time_to_update = False
            self.check_collision()
            self.snake.move()

    def check_collision(self) -> None:
        head = self.snake.body[0]
        if head.position == self.fruit.position:
            self.fruit.randomize()
            self.snake.fruit_eaten = True
            self.score_box.score += 1
        for component in islice(self.snake.body, 1, len(self.snake.body)):
            if self.fruit.position == component.position:
                self.fruit.randomize()
            if component.position == head.position:
                State.GAME = GameState.GAME_OVER
                self.__init__()
                return

    def run(self) -> None:
        if State.GAME == GameState.PLAYING:
            MainMenu.TITLE_TEXT = 'Menu'
            MainMenu.START_BUTTON_TEXT = 'Resume'
            Images.Fruits.load()
            Images.Snake.load()
            while State.GAME == GameState.PLAYING:
                for event in pygame.event.get():
                    self.handle_event(event)
                self.update()
                self.draw()
                Functions.update_display()
            Images.Fruits.unload()
            Images.Snake.unload()
