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


class Entity:
    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position

    def get_position(self) -> tuple[int, int]:
        return self.position

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_id(self) -> str:
        return 'E'

    def __str__(self) -> str:
        return self.get_id()

    def __repr__(self) -> str:
        return self.get_name() + "(" + str(self.position) + ")"


class DynamicEntity(Entity):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)

    def set_position(self, new_position: tuple[int, int]) -> None:
        self.position = new_position

    def get_id(self) -> str:
        return DYNAMIC_ENTITY


class Player(DynamicEntity):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.health = MAX_HEALTH
        self.hunger = 0
        self.thirst = 0
        self.inventory = Inventory()

    def get_id(self) -> str:
        return PLAYER

    def get_hunger(self) -> int:
        return self.hunger

    def get_thirst(self) -> int:
        return self.thirst

    def get_health(self) -> int:
        return self.health

    def change_hunger(self, amount: int) -> None:
        self.hunger += amount
        if self.hunger < 0:
            self.hunger = 0
        elif self.hunger > MAX_HUNGER:
            self.hunger = MAX_HUNGER

    def change_thirst(self, amount: int) -> None:
        self.thirst += amount
        if self.thirst < 0:
            self.thirst = 0
        elif self.thirst > MAX_THIRST:
            self.thirst = MAX_THIRST

    def change_health(self, amount: int) -> None:
        self.health += amount
        if self.health < 0:
            self.health = 0
        elif self.health > MAX_HEALTH:
            self.health = MAX_HEALTH

    def get_inventory(self) -> Inventory:
        return self.inventory

    def add_item(self, item: Item) -> None:
        self.inventory.add_item(item)


class Item(Entity):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)

    def get_id(self) -> str:
        return ITEM

    def apply(self, player: Player) -> None:
        player.add_item(self)


class Potion(Item):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.health_change = POTION_AMOUNT

    def get_id(self) -> str:
        return POTION

    def apply(self, player: Player) -> None:
        player.change_health(self.health_change)


class Coin(Item):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)

    def get_id(self) -> str:
        return COIN

    def apply(self, player: Player) -> None:
        # player.add_item(self)
        # no effect?
        pass


class Water(Item):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.thirst_change = WATER_AMOUNT

    def get_id(self) -> str:
        return WATER

    def apply(self, player: Player) -> None:
        player.change_thirst(self.thirst_change)


class Food(Item):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)

    def get_id(self) -> str:
        return FOOD


class Apple(Food):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.hunger_change = APPLE_AMOUNT

    def get_id(self) -> str:
        return APPLE

    def apply(self, player: Player) -> None:
        player.change_hunger(self.hunger_change)


class Honey(Food):
    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__(position)
        self.hunger_change = HONEY_AMOUNT

    def get_id(self) -> str:
        return HONEY

    def apply(self, player: Player) -> None:
        player.change_hunger(self.hunger_change)


class Inventory:
    def __init__(self, initial_items: Optional[list[Item]] = None) -> None:
        self.initial_items = initial_items
        self.items = {}
        if self.initial_items is not None:
            for item in self.initial_items:
                self.add_item(item)

    def add_item(self, item: Item) -> None:
        if item.get_name() not in self.items:
            self.items[item.get_name()] = [item]
        else:
            self.items[item.get_name()].append(item)

    def get_items(self) -> dict[str, list[Item]]:
        return self.items

    def remove_item(self, item_name: str) -> Optional[Item]:
        if item_name in self.items:
            item = self.items[item_name].pop(0)
            if len(self.items[item_name]) == 0:
                del self.items[item_name]
            return item
        return None

    def __str__(self) -> str:
        rtn = ""
        for item in self.items:
            rtn += f"{item}: {len(self.items[item])}\n"
        return rtn

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(initial_items=" + str(self.initial_items) + ")"


def main():
    # Write your code here
    pass


if __name__ == '__main__':
    main()
