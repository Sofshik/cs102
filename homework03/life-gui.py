import pathlib

import pygame
from pygame.constants import K_SPACE, KEYDOWN, MOUSEBUTTONUP, QUIT, K_s

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(
        self,
        life: GameOfLife,
        save_path: pathlib.Path,
        cell_size: int = 10,
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
        for x in range(0, self.life.cols * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (x, 0),
                (x, self.life.rows * self.cell_size),
            )
        for y in range(0, self.life.rows * self.cell_size, self.cell_size):
            pygame.draw.line(
                self.screen,
                pygame.Color("black"),
                (0, y),
                (self.life.cols * self.cell_size, y),
            )

    def draw_grid(self) -> None:
        for r in range(self.life.rows):
            for c in range(self.life.cols):
                if self.life.curr_generation[r][c] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        pygame.Rect(
                            c * self.cell_size,
                            r * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        pygame.Rect(
                            c * self.cell_size,
                            r * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    paused = not paused
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    position = pygame.mouse.get_pos()
                    x = position[0] // self.cell_size
                    y = position[1] // self.cell_size
                    if self.life.curr_generation[y][x] == 1:
                        self.life.curr_generation[y][x] = 0
                    else:
                        self.life.curr_generation[y][x] = 1
                if event.type == KEYDOWN and event.key == K_s:
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
    gui = GUI(life, save_path=pathlib.Path("filegui"), cell_size=40)
    gui.run()
