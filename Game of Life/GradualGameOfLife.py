import pygame as pg
from GradualBoard import Board
import time


def gameOfLife():
    pg.init()

    window_size = (800, 600)
    window = pg.display.set_mode(window_size)
    pg.display.set_caption("The Game of Life")

    board = Board(20)

    running = True
    while running:
        timeIN = time.time()
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            board.nextGen()

        # Draw board and record clicks
        board.drawBoard(window, window_size)
        board.recordClicks(window, window_size)
        board.recordArrow(window)


        pg.display.update()
        try: print(1 / (time.time() - timeIN))
        except ZeroDivisionError:
            print("infinite")

    pg.quit()


if __name__ == '__main__':
    gameOfLife()
