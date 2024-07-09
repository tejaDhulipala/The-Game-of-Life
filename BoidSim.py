import pygame as pg
import time
from Boid import Boid, BLACK
from BoidSystem import BoidSystem


def boidSim():
    pg.init()

    window_size = (1400, 700)
    window = pg.display.set_mode(window_size)
    pg.display.set_caption("Boid Sim")
    font = pg.font.Font('freesansbold.ttf', 20)
    fr = 0

    clock = pg.time.Clock()

    boidSystem1 = BoidSystem()

    running = True
    while running:
        window.fill(BLACK)
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()

        # Draw board
        # I'm changing the position system such that the bottom left is (0, 0)
        boidSystem1.checkForClick(window)
        boidSystem1.updateCommunities()
        boidSystem1.updateBoidsV(window)
        boidSystem1.updateBoidsPos()
        boidSystem1.drawBoids(window)

        # Text
        text1 = font.render("FPS: " + str(fr), True, (0, 255, 0))
        textRect = text1.get_rect()
        textRect.center = (40, 32)
        window.blit(text1, textRect)

        text1 = font.render("Wall Avoidance ", True, (0, 255, 0))
        textRect = text1.get_rect()
        textRect.center = (150, 32)
        window.blit(text1, textRect)

        pg.display.update()
        fr = 1000 // clock.tick(60)
        print(fr)

    pg.quit()


if __name__ == '__main__':
    boidSim()
