# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=unused-wildcard-import

import copy
import json
import pathlib
import random
import typing as tp
from itertools import product

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size

        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()

        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)

        # Максимальное число поколений
        self.max_generations = max_generations

        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        self.grid = []
        for row in range(self.rows):
            curr_el = []
            for col in range(self.cols):
                if randomize:
                    curr_el.append(random.randint(0, 1))
                else:
                    curr_el.append(0)
            self.grid.append(curr_el)
        return self.grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        self.neighbours = []
        for y_pos in range(row - 1, row + 2):
            for x_pos in range(col - 1, col + 2):
                val = True
                if y_pos == row and x_pos == col:
                    val = False
                if y_pos < 0 or y_pos >= self.rows:
                    val = False
                if x_pos < 0 or x_pos >= self.cols:
                    val = False
                if val:
                    self.neighbours.append(self.curr_generation[y_pos][x_pos])
        return self.neighbours

    def get_next_generation(self) -> Grid:
        self.new_grid = copy.deepcopy(self.curr_generation)
        for row in range(self.rows):
            for col in range(self.cols):
                cell = (row, col)
                summary = sum(self.get_neighbours(cell))
                if summary < 2 or summary > 3:
                    self.new_grid[row][col] = 0
                elif summary == 3:
                    self.new_grid[row][col] = 1
        return self.new_grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations  # type: ignore

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation  # type: ignore

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        curr_file = open(filename)
        curr_list = curr_file.read().splitlines()
        new_list = []
        for r in curr_list:
            new_line = []
            for c in r:
                new_line.append(int(c))
            new_list.append(new_line)
        curr_file.close()
        game = GameOfLife((len(new_list), len(new_list[0])))
        game.curr_generation = new_list
        return game

    def save(self, filename: pathlib.Path) -> None:
        new_file = open(filename, "w")
        for r in self.curr_generation:
            for c in r:
                new_file.write(str(c))
            new_file.write("\n")
        new_file.close()


def main():
    filename = "generation_{}.txt"

    def gen_path(new):
        return pathlib.Path(filename.format(new)).resolve()

    game = GameOfLife(size=(18, 25))
    game.step()
    game.save(gen_path(0))

    game = GameOfLife.from_file(gen_path(0))
    game.step()
    game.save(gen_path(1))


if __name__ == "__main__":
    main()
