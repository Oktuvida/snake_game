from enum import Enum
from typing import Any


class EnumExtend(Enum):
    @classmethod
    def list(cls) -> list:
        return [x.value for x in cls]

    @classmethod
    def get_next(cls, actual_value: Any) -> Any:
        values = cls.list()
        for index, value in enumerate(values):
            if cls(value) == actual_value:
                return cls(values[(index + 1) % len(values)])

    @classmethod
    def get_prev(cls, actual_value: Any) -> Any:
        values = cls.list()
        for index, value in enumerate(values):
            if cls(value) == actual_value:
                return cls(values[(index - 1) % len(values)])


class GameOverState(EnumExtend):
    RESTART = 0
    EXIT = 1


class ResolutionState(EnumExtend):
    R600X600 = 0
    R800X800 = 1
    R1000X1000 = 2
    BACK = 3


class SettingsState(EnumExtend):
    RESOLUTION = 0
    BACK = 1


class MenuState(EnumExtend):
    START = 0
    SETTINGS = 1
    EXIT = 2


class GameState(EnumExtend):
    MENU = 0
    PLAYING = 1
    SETTINGS = 2
    RESOLUTION = 3
    GAME_OVER = 4


class State:
    MENU = MenuState.START
    GAME = GameState.MENU
    SETTINGS = SettingsState.RESOLUTION
    RESOLUTION = ResolutionState.R800X800
    GAME_OVER = GameOverState.RESTART
