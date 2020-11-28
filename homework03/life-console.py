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
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    screen.addch(row + 1, col + 1, "*")
                else:
                    screen.addch(row + 1, col + 1, " ")

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
            curr_el = window.getch()
            if curr_el == ord("\n"):
                paused = False if paused else True
            elif curr_el == ord("S"):
                self.life.save(self.save_path)
            elif curr_el == curses.ascii.ESC:
                running = False
            if not paused:
                self.draw_grid(window)
                window.refresh()
                self.life.step()

                time.sleep(1)

        curses.endwin()


if __name__ == "__main__":
    life = GameOfLife((15, 30), randomize=True)
    ui = Console(life, save_path=pathlib.Path("fileui.txt"))
    ui.run()
