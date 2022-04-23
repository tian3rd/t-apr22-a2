from __future__ import annotations
from typing import Optional
from a2_support import UserInterface, TextInterface
from constants import *
# from abc import ABCMeta, abstractmethod

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"

# Before submission, update this tag to reflect the latest version of the
# that you implemented, as per the blackboard changelog.
__version__ = 1.0

# Uncomment this function when you have completed the Level class and are ready
# to attempt the Model class.

# def load_game(filename: str) -> list['Level']:
#     """ Reads a game file and creates a list of all the levels in order.

#     Parameters:
#         filename: The path to the game file

#     Returns:
#         A list of all Level instances to play in the game
#     """
#     levels = []
#     with open(filename, 'r') as file:
#         for line in file:
#             line = line.strip()
#             if line.startswith('Maze'):
#                 _, _, dimensions = line[5:].partition(' - ')
#                 dimensions = [int(item) for item in dimensions.split()]
#                 levels.append(Level(dimensions))
#             elif len(line) > 0 and len(levels) > 0:
#                 levels[-1].add_row(line)
#     return levels


# Write your classes here

class Tile():
    def is_blocking(self) -> bool:
        return False

    def damage(self) -> int:
        return 0

    def get_id(self) -> str:
        return ABSTRACT_TILE

    def __str__(self) -> str:
        return self.get_id()

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"


class Wall(Tile):
    def is_blocking(self) -> bool:
        return True

    def get_id(self) -> str:
        return WALL


class Empty(Tile):
    def is_blocking(self) -> bool:
        return False

    def get_id(self) -> str:
        return EMPTY


class Lava(Tile):
    def is_blocking(self) -> bool:
        return False

    def damage(self) -> int:
        return LAVA_DAMAGE

    def get_id(self) -> str:
        return LAVA


class Door(Tile):
    def __init__(self, is_blocked: bool = True, id: str = DOOR):
        self.is_blocked = is_blocked
        self.id = id

    def is_blocking(self) -> bool:
        return self.is_blocked

    def get_id(self) -> str:
        return self.id

    def unlock(self) -> None:
        self.is_blocked = False
        self.id = EMPTY


def main():
    # Write your code here
    pass


if __name__ == '__main__':
    main()
