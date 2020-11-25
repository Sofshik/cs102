import pathlib

import pygame
import pygame.constants

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(
        self,
        life: GameOfLife,
        save_path: pathlib.Path,
        cell_size: int = 20,
        speed: int = 10,
    ) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen = pygame.display.set_mode(
            (self.life.cols * self.cell_size, self.life.rows * self.cell_size)
        )
        self.save_path = save_path

    def draw_lines(self) -> None:
        for x_pos in range(0, self.life.cols * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (x_pos, 0),
                (x_pos, self.life.rows * self.cell_size),
            )
        for y_pos in range(0, self.life.rows * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, y_pos),
                (self.life.cols * self.cell_size, y_pos),
            )

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                rect = pygame.Rect(
                    self.cell_size * col,
                    self.cell_size * row,
                    self.cell_size,
                    self.cell_size,
                )
                if self.life.curr_generation[row][col]:
                    pygame.draw.rect(self.screen, pygame.Color("yellowgreen"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("cornsilk2"), rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    running = False
                if (
                    event.type == pygame.constants.KEYDOWN
                    and event.key == pygame.constants.K_SPACE
                ):
                    paused = not paused
                if event.type == pygame.constants.MOUSEBUTTONUP and event.button == 1:
                    position = pygame.mouse.get_pos()
                    x_pos = position[0] // self.cell_size
                    y_pos = position[1] // self.cell_size
                    if self.life.curr_generation[y_pos][x_pos] == 1:
                        self.life.curr_generation[y_pos][x_pos] = 0
                    else:
                        self.life.curr_generation[y_pos][x_pos] = 1
                if (
                    event.type == pygame.constants.KEYDOWN
                    and event.key == pygame.constants.K_s
                ):
                    self.life.save(self.save_path)
            self.draw_lines()
            if not paused:
                self.life.step()
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((18, 25), randomize=True)
    gui = GUI(life, save_path=pathlib.Path("filegui.txt"))
    gui.run()
