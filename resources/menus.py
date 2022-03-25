import pygame
from resources.commons import Backgrounds, Button, Colors, Functions, Mouse, TextBox, Vector
from resources.state import GameOverState, GameState, MenuState, ResolutionState, SettingsState, State
from settings import Display, FontFamily


class AbstractMenu:
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(
            FontFamily.DEFAULT, Display.FONT_SIZE * 2)
        self.title_position = Vector(Display.WIDTH / 2, Display.HEIGHT / 4)
        self.title: TextBox = None
        self.buttons: dict[int, Button] = {}
        self.background = Backgrounds.Grass()
        self.mouse = Mouse()

    def draw(self) -> None:
        self.background.draw(Display.SURFACE)
        self.title.draw(Display.SURFACE)
        for value in self.buttons.values():
            value.draw(Display.SURFACE)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            Functions.exit()

    def is_active(self) -> bool:
        return False

    def get_selected_button(self) -> int:
        return -1

    def update(self) -> None:
        if self.title_position != Vector(Display.WIDTH / 2, Display.HEIGHT / 4):
            self.__init__()
        self.background.update()
        self.mouse.update()
        self.title.update()
        self.buttons[self.get_selected_button()].collide = True
        for key in self.buttons.keys():
            if key != self.get_selected_button():
                self.buttons[self.get_selected_button()].collide = self.buttons[self.get_selected_button()] and not self.buttons[key].is_colliding(
                    self.mouse)
            self.buttons[key].update()

    def run(self) -> None:
        while self.is_active():
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.draw()
            Functions.update_display()


class MainMenu(AbstractMenu):
    TITLE_TEXT = 'Snake'
    START_BUTTON_TEXT = 'Start'

    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.HEIGHT / 8)
        self.title = TextBox(
            MainMenu.TITLE_TEXT, self.title_font, Colors.PRIMARY_BLACK, self.title_position)
        self.buttons = {
            MenuState.START: Button(
                MainMenu.START_BUTTON_TEXT, self.title.position + position_difference
            ),
            MenuState.SETTINGS: Button(
                'Settings', self.title.position + (position_difference * 2)
            ),
            MenuState.EXIT: Button(
                'Exit', self.title.position + (position_difference * 3)
            )
        }

    def get_selected_button(self) -> int:
        return State.MENU

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    if MainMenu.START_BUTTON_TEXT != "Start":
                        State.GAME = GameState.PLAYING
                case pygame.K_UP:
                    State.MENU = MenuState.get_prev(State.MENU)
                case pygame.K_DOWN:
                    State.MENU = MenuState.get_next(State.MENU)
                case pygame.K_RETURN:
                    match State.MENU:
                        case MenuState.START:
                            State.GAME = GameState.PLAYING
                        case MenuState.SETTINGS:
                            State.GAME = GameState.SETTINGS
                        case MenuState.EXIT:
                            Functions.exit()

    def is_active(self) -> bool:
        return State.GAME == GameState.MENU

class SettingsMenu(AbstractMenu):
    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.HEIGHT / 8)
        self.title = TextBox(
            'Settings', self.title_font, Colors.PRIMARY_BLACK, self.title_position)
        self.buttons = {
            SettingsState.RESOLUTION : Button(
                'Resolution',self.title_position + position_difference
            ),
            SettingsState.BACK : Button(
                'Back', self.title_position + (position_difference * 2)
            )
        }

    def get_selected_button(self) -> int:
        return State.SETTINGS

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    State.GAME = GameState.MENU
                case pygame.K_UP:
                    State.SETTINGS = SettingsState.get_prev(State.SETTINGS)
                case pygame.K_DOWN:
                    State.SETTINGS = SettingsState.get_next(State.SETTINGS)
                case pygame.K_RETURN:
                    match State.SETTINGS:
                        case SettingsState.RESOLUTION:
                            State.GAME = GameState.RESOLUTION
                        case SettingsState.BACK:
                            State.GAME = GameState.MENU

    def is_active(self) -> bool:
        return State.GAME == GameState.SETTINGS

class ResolutionMenu(AbstractMenu):
    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.HEIGHT / 8)
        self.title = TextBox('Resolution', self.title_font,
                             Colors.PRIMARY_BLACK, self.title_position)
        self.buttons = {
            ResolutionState.R600X600 : Button(
                '600x600', self.title_position + position_difference
            ),
            ResolutionState.R800X800 : Button(
                '800x800', self.title_position + (position_difference * 2)
            ),
            ResolutionState.R1000X1000 : Button(
                '1000x1000', self.title_position + (position_difference * 3)
            ),
            ResolutionState.BACK : Button(
                'Back', self.title_position + (position_difference * 4)
            )
        }

    def get_selected_button(self) -> int:
        return State.RESOLUTION

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_ESCAPE:
                    State.GAME = GameState.SETTINGS
                case pygame.K_UP:
                    State.RESOLUTION = ResolutionState.get_prev(
                        State.RESOLUTION)
                case pygame.K_DOWN:
                    State.RESOLUTION = ResolutionState.get_next(
                        State.RESOLUTION)
                case pygame.K_RETURN:
                    match State.RESOLUTION:
                        case ResolutionState.R600X600:
                            Display.WIDTH = 600
                        case ResolutionState.R800X800:
                            Display.WIDTH = 800
                        case ResolutionState.R1000X1000:
                            Display.WIDTH = 1000
                        case ResolutionState.BACK:
                            State.GAME = GameState.SETTINGS
                    Display.update()
                    Display.set_surface()

    def is_active(self) -> bool:
        return State.GAME == GameState.RESOLUTION

class GameOverMenu(AbstractMenu):
    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.WIDTH / 8)
        self.title = TextBox('Game Over', self.title_font,
                             Colors.PRIMARY_BLACK, self.title_position)
        self.buttons = {
            GameOverState.RESTART : Button(
                'Restart', self.title_position + position_difference
            ),
            GameOverState.EXIT : Button(
                'Exit', self.title_position + (position_difference * 2)
            )
        }

    def get_selected_button(self) -> int:
        return State.GAME_OVER

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    State.GAME_OVER = GameOverState.get_prev(State.GAME_OVER)
                case pygame.K_DOWN:
                    State.GAME_OVER = GameOverState.get_next(State.GAME_OVER)
                case pygame.K_RETURN:
                    match State.GAME_OVER:
                        case GameOverState.RESTART:
                            State.GAME = GameState.PLAYING
                        case GameOverState.EXIT:
                            Functions.exit()

    def is_active(self) -> bool:
        return State.GAME == GameState.GAME_OVER
