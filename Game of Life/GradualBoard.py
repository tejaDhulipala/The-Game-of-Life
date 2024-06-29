import pygame as pg
from copy import deepcopy

class Board:
    def __init__(self, size):
        self.n = size
        self.board = [[0 for i in range(size)] for i in range(size)]

    def drawBoard(self, screen: pg.Surface, screenSize: tuple):
        rowNum = 0
        for row in self.board:
            col = 0
            for cell in row:
                if cell == 1:
                    rect = pg.Rect(col / self.n * screenSize[0], rowNum / self.n * screenSize[1], screenSize[0] / self.n, screenSize[1] / self.n)
                    pg.draw.rect(screen, (0, 255, 0), rect)
                elif cell == 0.5:
                    rect = pg.Rect(col / self.n * screenSize[0], rowNum / self.n * screenSize[1],
                                   screenSize[0] / self.n, screenSize[1] / self.n)
                    pg.draw.rect(screen, (0, 128, 0), rect)
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
            self.board[row][col] = 0.5
        elif pg.mouse.get_pressed()[2]:
            x, y = pg.mouse.get_pos()
            row = int(y / screenSize[1] * self.n)
            col = int(x / screenSize[0] * self.n)
            print("Row" + str(row))
            print("Col" + str(col))
            self.board[row][col] = 0

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
                else: lUp = 0

                if col > 0: lC = self.board[row][col-1]
                else: lC = 0

                if row < self.n - 1 and col > 0: lDown = self.board[row+1][col-1]
                else:
                    lDown = 0

                if row > 0: cUp = self.board[row-1][col]
                else:
                    cUp = 0

                if row < self.n - 1: cDown = self.board[row+1][col]
                else:
                    cDown = 0

                if row > 0 and col < self.n - 1: rUp = self.board[row-1][col+1]
                else:
                    rUp = 0

                if col < self.n - 1: rC = self.board[row][col+1]
                else:
                    rC = 0

                if row < self.n - 1 and col < self.n - 1: rDown = self.board[row+1][col+1]
                else:
                    rDown = 0

                adjCells = [lUp, lC, lDown, cDown, cUp, rDown, rC, rUp]
                numLive = adjCells.count(0)
                if self.board[row][col] == 0:
                    if numLive < 1:
                        tempBoard[row][col] = 0
                    elif numLive < 2 and adjCells.count(0.5) >= 1:
                        tempBoard[row][col] = 0.5
                    elif numLive == 2:
                        tempBoard[row][col] = 1
                else:
                    if adjCells.count(0) <= 3:
                        tempBoard[row][col] -= 0.5 if adjCells.count(0) == 3 else 1
                    if numLive >= 4:
                        tempBoard[row][col] -= 0.5 if numLive == 4 else 1
                # if self.board[row][col] == 0.5:
                #     if numDead != 6 and numDead != 5:
                #         tempBoard[row][col] = 0
                # elif self.board[row][col] == 1:
                #     if numDead != 6 and numDead != 5:
                #         tempBoard[row][col] = 0.5
                # else:
                #     if numDead == 5:
                #         tempBoard[row][col] += 0.5


        self.board = tempBoard
