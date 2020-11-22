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

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = copy.deepcopy(self.create_grid(randomize=False))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
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
        for r in range(self.cell_height):
            el = []
            for d in range(self.cell_width):
                if randomize:
                    el.append(random.randint(0, 1))
                else:
                    el.append(0)
            grid.append(el)
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
                    0 + self.cell_width * index_col,
                    0 + self.cell_height * index_row,
                    self.cell_width,
                    self.cell_height,
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
        for y in range(row - 1, row + 2):
            for x in range(col - 1, col + 2):
                val = True
                if y == row and x == col:
                    val = False
                if y < 0 or y >= self.height:
                    val = False
                if x < 0 or x >= self.width:
                    val = False
                if val:
                    self.neighbours.append(self.grid[y][x])
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
        for r in range(self.height):
            for c in range(self.width):
                cell = (r, c)
                summary = sum(self.get_neighbours(cell))
                if summary < 2 or summary > 3:
                    self.new_grid[r][c] = 0
                elif summary == 3:
                    self.new_grid[r][c] = 1
        return self.new_grid
