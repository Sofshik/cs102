import curses
import curses.ascii
import pathlib
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, save_path: pathlib.Path) -> None:
        super().__init__(life)
        self.save_path = save_path

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for r in range(self.life.rows):
            for c in range(self.life.cols):
                if self.life.curr_generation[r][c] == 1:
                    screen.addch(r + 1, c + 1, "*")
                else:
                    screen.addch(r + 1, c + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        screen.clear()
        screen.refresh()
        window = curses.newwin(self.life.rows + 2, self.life.cols + 2)
        self.draw_borders(window)
        window.timeout(1)
        window.nodelay(True)

        running = True
        paused = False
        while running:
            el = window.getch()
            if el == ord("\n"):
                paused = False if paused else True
            elif el == ord("S"):
                self.life.save(self.save_path)
            elif el == curses.ascii.ESC:
                running = False
            if not paused:
                self.draw_grid(window)
                window.refresh()
                self.life.step()

                time.sleep(1)

        curses.endwin()
