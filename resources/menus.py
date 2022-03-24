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
        self.background = Backgrounds.Grass()
        self.mouse = Mouse()

    def draw(self) -> None:
        self.background.draw(Display.SURFACE)
        self.title.draw(Display.SURFACE)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            Functions.exit()

    def update(self) -> None:
        self.background.update()
        self.mouse.update()


class MainMenu(AbstractMenu):
    TITLE_TEXT = 'Snake'
    START_BUTTON_TEXT = 'Start'

    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.HEIGHT / 8)
        self.title = TextBox(
            MainMenu.TITLE_TEXT, self.title_font, Colors.PRIMARY_BLACK, self.title_position)
        self.start_button = Button(
            MainMenu.START_BUTTON_TEXT, self.title.position + position_difference)
        self.settings_button = Button(
            'Settings', self.start_button.position + position_difference)
        self.exit_button = Button(
            'Exit', self.settings_button.position + position_difference)

    def draw(self) -> None:
        super().draw()
        self.start_button.draw(Display.SURFACE)
        self.settings_button.draw(Display.SURFACE)
        self.exit_button.draw(Display.SURFACE)

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

    def update(self) -> None:
        super().update()
        self.title.text = MainMenu.TITLE_TEXT
        self.start_button.text_box.text = MainMenu.START_BUTTON_TEXT
        match State.MENU:
            case MenuState.START:
                self.start_button.collide = not self.settings_button.is_colliding(
                    self.mouse) and not self.exit_button.is_colliding(self.mouse)
            case MenuState.SETTINGS:
                self.settings_button.collide = not self.start_button.is_colliding(
                    self.mouse) and not self.exit_button.is_colliding(self.mouse)
            case MenuState.EXIT:
                self.exit_button.collide = not self.start_button.is_colliding(
                    self.mouse) and not self.settings_button.is_colliding(self.mouse)
        self.title.update()
        self.start_button.update()
        self.settings_button.update()
        self.exit_button.update()

    def run(self) -> None:
        while State.GAME == GameState.MENU:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            self.update()
            Functions.update_display()


class SettingsMenu(AbstractMenu):
    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.HEIGHT / 8)
        self.title = TextBox(
            'Settings', self.title_font, Colors.PRIMARY_BLACK, self.title_position)
        self.resolution_button = Button(
            'Resolution', self.title.position + position_difference)
        self.back_button = Button(
            'Back', self.resolution_button.position + position_difference)

    def draw(self) -> None:
        super().draw()
        self.resolution_button.draw(Display.SURFACE)
        self.back_button.draw(Display.SURFACE)

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

    def update(self) -> None:
        super().update()
        match State.SETTINGS:
            case SettingsState.RESOLUTION:
                self.resolution_button.collide = not self.back_button.is_colliding(
                    self.mouse)
            case SettingsState.BACK:
                self.back_button.collide = not self.resolution_button.is_colliding(
                    self.mouse)
        self.resolution_button.update()
        self.back_button.update()

    def run(self) -> None:
        while State.GAME == GameState.SETTINGS:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            self.update()
            Functions.update_display()


class ResolutionMenu(AbstractMenu):
    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.HEIGHT / 8)
        self.title = TextBox('Resolution', self.title_font,
                             Colors.PRIMARY_BLACK, self.title_position)
        self.r600x600_button = Button(
            '600x600', self.title_position + position_difference)
        self.r800x800_button = Button(
            '800x800', self.r600x600_button.position + position_difference)
        self.r1000x1000_button = Button(
            '1000x1000', self.r800x800_button.position + position_difference)
        self.back_button = Button(
            'Back', self.r1000x1000_button.position + position_difference)

    def draw(self) -> None:
        super().draw()
        self.r600x600_button.draw(Display.SURFACE)
        self.r800x800_button.draw(Display.SURFACE)
        self.r1000x1000_button.draw(Display.SURFACE)
        self.back_button.draw(Display.SURFACE)

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

    def update(self) -> None:
        super().update()
        if self.title_position != Vector(Display.WIDTH / 2, Display.HEIGHT / 4):
            self.__init__()
        match State.RESOLUTION:
            case ResolutionState.R600X600:
                self.r600x600_button.collide = not self.r800x800_button.is_colliding(
                    self.mouse) and not self.r1000x1000_button.is_colliding(self.mouse) and not self.back_button.is_colliding(self.mouse)
            case ResolutionState.R800X800:
                self.r800x800_button.collide = not self.r600x600_button.is_colliding(
                    self.mouse) and not self.r1000x1000_button.is_colliding(self.mouse) and not self.back_button.is_colliding(self.mouse)
            case ResolutionState.R1000X1000:
                self.r1000x1000_button.collide = not self.r600x600_button.is_colliding(
                    self.mouse) and not self.r800x800_button.is_colliding(self.mouse) and not self.back_button.is_colliding(self.mouse)
            case ResolutionState.BACK:
                self.back_button.collide = not self.r600x600_button.is_colliding(self.mouse) and not self.r800x800_button.is_colliding(
                    self.mouse) and not self.r1000x1000_button.is_colliding(self.mouse)
        self.r600x600_button.update()
        self.r800x800_button.update()
        self.r1000x1000_button.update()
        self.back_button.update()

    def run(self) -> None:
        while State.GAME == GameState.RESOLUTION:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            self.update()
            Functions.update_display()


class GameOverMenu(AbstractMenu):
    def __init__(self) -> None:
        super().__init__()
        position_difference = Vector(0, Display.WIDTH / 8)
        self.title = TextBox('Game Over', self.title_font,
                             Colors.PRIMARY_BLACK, self.title_position)
        self.restart_button = Button(
            'Restart', self.title.position + position_difference)
        self.exit_button = Button(
            'Exit', self.restart_button.position + position_difference)

    def draw(self) -> None:
        super().draw()
        self.restart_button.draw(Display.SURFACE)
        self.exit_button.draw(Display.SURFACE)

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

    def update(self) -> None:
        super().update()
        match State.GAME_OVER:
            case GameOverState.RESTART:
                self.restart_button.collide = not self.exit_button.is_colliding(
                    self.mouse)
            case GameOverState.EXIT:
                self.exit_button.collide = not self.restart_button.is_colliding(
                    self.mouse)
        self.restart_button.update()
        self.exit_button.update()

    def run(self) -> None:
        while State.GAME == GameState.GAME_OVER:
            for event in pygame.event.get():
                self.handle_event(event)
            self.draw()
            self.update()
            Functions.update_display()
