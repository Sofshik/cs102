import copy
import random
from typing import List, Tuple

import pygame
from pygame.locals import *

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Создание списка клеток
        self.grid = copy.deepcopy(self.create_grid(randomize=True))

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x_pos in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x_pos, 0), (x_pos, self.height))
        for y_pos in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y_pos), (self.width, y_pos))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []
        for row in range(self.cell_height):
            curr_el = []
            for col in range(self.cell_width):
                if randomize:
                    curr_el.append(random.randint(0, 1))
                else:
                    curr_el.append(0)
            grid.append(curr_el)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in self.grid:
            index_row = self.grid.index(row)
            for col in row:
                index_col = row.index(col)
                rect = pygame.Rect(
                    0 + self.cell_size * index_col,
                    0 + self.cell_size * index_row,
                    self.cell_size,
                    self.cell_size,
                )
                if self.grid[index_row][index_col]:
                    pygame.draw.rect(self.screen, pygame.Color("white"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        self.neighbours = []
        for y_pos in range(max(0, row - 1), min(self.cell_height, row + 2)):
            for x_pos in range(max(0, col - 1), min(self.cell_width, col + 2)):
                if not (row == y_pos and col == x_pos):
                    self.neighbours += [self.grid[y_pos][x_pos]]
        return self.neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        self.new_grid = copy.deepcopy(self.grid)
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                cell = (row, col)
                summary = sum(self.get_neighbours(cell))
                if self.grid[row][col] == 1:
                    if summary == 2 or summary == 3:
                        self.new_grid[row][col] = 1
                    else:
                        self.new_grid[row][col] = 0
                else:
                    if summary == 3:
                        self.new_grid[row][col] = 1
                    else:
                        self.new_grid[row][col] = 0
        return self.new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
