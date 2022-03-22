# Snake Game
Based on the project developed by [Clear Code](https://github.com/clear-code-projects/Snake).

<p align="center">
    <img src="./screenshots/gameplay.gif" alt="gameplay"/>
</p>

## How does it work?
Basically the operation of the code lies in the continuous use and modification of static variables between multiple files.

For example, in the case of the multiple menus, they are always running in a while loop (the "run" method of the SnakeGame class).  These are toggled by a variable, "GAME", present in the "State" class.

Another example could be the images. These do not belong to a specific sprite, but are static variables, being called directly by the sprites when they are drawn. By default they are initialized to None to occupy as little space as possible (16 bytes), but once they are going to be used, they are loaded by a static method called "load". Once they are no longer used, another static method, "unload", is called, which returns all variables to None.

Another thing to note is the use of hash tables to draw the snake. Its keys are obtained by making Vector2 of the "Pygame" library hasheable, and then registering all possible directions in a tuple (only two directions per tuple are required).

## Requirements
- [`Pygame`](https://www.pygame.org/news)
- [`Python 3.10`](https://www.python.org/downloads/release/python-3100/)
