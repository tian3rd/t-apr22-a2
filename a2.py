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


def load_game(filename: str) -> list['Level']:
    """ Reads a game file and creates a list of all the levels in order.

    Parameters:
        filename: The path to the game file

    Returns:
        A list of all Level instances to play in the game
    """
    levels = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Maze'):
                _, _, dimensions = line[5:].partition(' - ')
                dimensions = [int(item) for item in dimensions.split()]
                levels.append(Level(dimensions))
            elif len(line) > 0 and len(levels) > 0:
                levels[-1].add_row(line)
    return levels


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


class Maze:
    def __init__(self, dimensions: tuple[int, int]) -> None:
        self.dimensions = dimensions
        self.maze = []
        self.tile_pool = {LAVA: Lava, WALL: Wall, EMPTY: Empty, DOOR: Door}

    def get_dimensions(self) -> tuple[int, int]:
        return self.dimensions

    def add_row(self, row: str) -> None:
        assert len(row) == self.dimensions[1] and len(
            self.maze) < self.dimensions[0]
        real_row = []
        for tile in row:
            if tile in self.tile_pool:
                real_row.append(self.tile_pool[tile]())
            else:
                real_row.append(self.tile_pool[EMPTY]())
        self.maze.append(real_row)

    def get_tiles(self) -> list[list[Tile]]:
        return self.maze

    def unlock_door(self) -> None:
        for row in self.maze:
            for tile in row:
                if isinstance(tile, Door):
                    tile.unlock()

    def get_tile(self, position: tuple[int, int]) -> Tile:
        return self.maze[position[0]][position[1]]

    def __str__(self) -> str:
        rtn = ""
        for row in self.maze:
            for tile in row:
                rtn += str(tile)
            rtn += "\n"
        return rtn

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"({self.dimensions})"


class Level:
    def __init__(self, dimenstions: tuple[int, int]) -> None:
        self.dimensions = dimenstions
        self.maze = Maze(self.dimensions)
        self.items = {}
        self.item_pool = {'C': Coin, 'M': Potion, 'P': PLAYER,
                          'W': Water, 'A': Apple, 'H': Honey}
        self.player_start_position = None

    def get_maze(self) -> Maze:
        return self.maze

    def get_dimensions(self) -> tuple[int, int]:
        return self.dimensions

    def attempt_unlock_door(self) -> None:
        all_items = self.get_items()
        for item in all_items:
            if isinstance(all_items[item], Coin):
                return
        self.maze.unlock_door()

    def add_row(self, row: str) -> None:
        self.maze.add_row(row)
        row_no = len(self.maze.get_tiles()) - 1
        for col_no, element in enumerate(row):
            if element in self.item_pool:
                self.items[(row_no, col_no)] = self.item_pool[element](
                    (row_no, col_no))
            if element == PLAYER:
                self.add_player_start((row_no, col_no))

    def add_entity(self, position: tuple[int, int], entity_id: str) -> None:
        if entity_id in self.item_pool:
            self.items[position] = self.item_pool[entity_id](position)

    def get_items(self) -> dict[tuple[int, int], Item]:
        return self.items

    def remove_item(self, position: tuple[int, int]) -> None:
        if self.items[position].get_id() in self.item_pool:
            del self.items[position]

    def add_player_start(self, position: tuple[int, int]) -> None:
        self.player_start_position = position

    def get_player_start(self) -> Optional[tuple[int, int]]:
        return self.player_start_position

    def __str__(self) -> str:
        rtn = "Maze:\n"
        rtn += str(self.maze)
        rtn += f"Items:{self.items}\n"
        rtn += f"Player start: {self.get_player_start()}\n"
        return rtn

    def __repr__(self) -> str:
        return self.__class__.__name__ + f"({self.dimensions})"


class Model:
    def __init__(self, game_file: str) -> None:
        self.game_file = game_file
        self.levels = load_game(game_file)
        self.player = Player(self.levels[0].get_player_start())
        self.won = False
        self.lost = False
        self.current_level = 0
        self.just_level_up = False
        self.steps = 0
        self.item_pool = {'C': Coin, 'M': Potion,
                          'W': Water, 'A': Apple, 'H': Honey}

    def has_won(self) -> bool:
        return self.won

    def has_lost(self) -> bool:
        return self.lost

    def get_level(self) -> Level:
        return self.levels[self.current_level]

    def level_up(self) -> None:
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.won = True
            self.lost = False
        else:
            self.just_level_up = True

    def did_level_up(self) -> bool:
        return self.just_level_up

    def move_player(self, delta: tuple[int, int]) -> None:
        level = self.get_level()
        player_start = level.get_player_start()
        if player_start is None:
            return
        new_position = (player_start[0] + delta[0], player_start[1] + delta[1])
        if new_position[0] < 0 or new_position[0] >= level.get_dimensions()[0]:
            return
        if new_position[1] < 0 or new_position[1] >= level.get_dimensions()[1]:
            return
        if isinstance(level.get_maze().get_tile(new_position), Wall):
            return
        elif isinstance(level.get_maze().get_tile(new_position), Lava):
            self.player.change_health(LAVA_DAMAGE)
            return
        elif new_position in level.get_items():
            self.attempt_collect_item(new_position)
            self.player.change_health(-1)
            self.steps += 1
            if self.steps % 5 == 0:
                self.player.change_hunger(1)
                self.player.change_thirst(1)
        # update player's health
        if self.player.get_health() <= 0 or self.player.get_hunger() >= MAX_HUNGER or self.player.get_thirst() >= MAX_THIRST:
            self.lost = True
            return
        self.player.set_position(new_position)
        level.add_entity(new_position, PLAYER)
        level.remove_item(player_start)
        # level.attempt_unlock_door()

    def attempt_collect_item(self, position: tuple[int, int]) -> None:
        level = self.get_level()
        self.player.add_item(level.get_items()[position])
        level.remove_item(position)
        level.attempt_unlock_door()

    def get_player(self) -> Player:
        return self.player

    def get_player_stats(self) -> tuple[int, int, int]:
        return self.player.get_health(), self.player.get_hunger(), self.player.get_thirst()

    def get_player_inventory(self) -> Inventory:
        return self.player.get_inventory()

    def get_current_maze(self) -> Maze:
        return self.get_level().get_maze()

    def get_current_items(self) -> dict[tuple[int, int], Item]:
        return self.get_level().get_items()

    def __str__(self) -> str:
        return self.__class__.__name__ + f"({self.game_file})"

    def __repr__(self) -> str:
        return str(self)


def main():
    # Write your code here
    pass


if __name__ == '__main__':
    main()
