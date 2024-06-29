import pygame as pg
from copy import deepcopy
from random import choice

class Board:
    def __init__(self, size):
        self.n = size
        self.board = [[choice([True, False]) for i in range(size)] for i in range(size)]

    def drawBoard(self, screen: pg.Surface, screenSize: tuple):
        rowNum = 0
        for row in self.board:
            col = 0
            for cell in row:
                if cell:
                    rect = pg.Rect(col / self.n * screenSize[0], rowNum / self.n * screenSize[1], screenSize[0] / self.n, screenSize[1] / self.n)
                    pg.draw.rect(screen, (255, 255, 255), rect)
                else:
                    rect = pg.Rect(col / self.n * screenSize[0], rowNum / self.n * screenSize[1],
                                   screenSize[0] / self.n, screenSize[1] / self.n)
                    pg.draw.rect(screen, (0, 0, 0), rect)
                col += 1
            rowNum += 1

        for x in range(0, screenSize[0], int(screenSize[0] / self.n)):
            pg.draw.line(screen, (150, 150, 150), (x, 0), (x, screenSize[1]))
        for y in range(0, screenSize[1], int(screenSize[1] / self.n)):
            pg.draw.line(screen, (150, 150, 150), (0, y), (screenSize[0], y))

    def recordClicks(self, screen: pg.Surface, screenSize: tuple):
        if pg.mouse.get_pressed()[0]:
            x, y = pg.mouse.get_pos()
            row = int(y / screenSize[1] * self.n)
            col = int(x / screenSize[0] * self.n)
            print("Row" + str(row))
            print("Col" + str(col))
            self.board[row][col] = True
        elif pg.mouse.get_pressed()[2]:
            x, y = pg.mouse.get_pos()
            row = int(y / screenSize[1] * self.n)
            col = int(x / screenSize[0] * self.n)
            print("Row" + str(row))
            print("Col" + str(col))
            self.board[row][col] = False

    def recordArrow(self, screen: pg.Surface):
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    self.nextGen()

    def nextGen(self):
        tempBoard = deepcopy(self.board)
        for row in range(self.n):
            for col in range(self.n):
                # shitty code
                if row > 0 and col > 0: lUp = self.board[row-1][col-1]
                else: lUp = False

                if col > 0: lC = self.board[row][col-1]
                else: lC = False

                if row < self.n - 1 and col > 0: lDown = self.board[row+1][col-1]
                else:
                    lDown = False

                if row > 0: cUp = self.board[row-1][col]
                else:
                    cUp = False

                if row < self.n - 1: cDown = self.board[row+1][col]
                else:
                    cDown = False

                if row > 0 and col < self.n - 1: rUp = self.board[row-1][col+1]
                else:
                    rUp = False

                if col < self.n - 1: rC = self.board[row][col+1]
                else:
                    rC = False

                if row < self.n - 1 and col < self.n - 1: rDown = self.board[row+1][col+1]
                else:
                    rDown = False

                adjCells = [lUp, lC, lDown, cDown, cUp, rDown, rC, rUp]
                numLive = adjCells.count(True)
                if self.board[row][col]:
                    if numLive < 2 or numLive > 3:
                        tempBoard[row][col] = False
                else:
                    if numLive == 3:
                        tempBoard[row][col] = True

        self.board = tempBoard
