from Boid import Boid
import pygame as pg

class BoidSystem:
    def __init__(self):
        self.boids = []

    def addBoid(self, boid: Boid) -> bool:
        for b in self.boids:
            if Boid.detectCollision(b, boid):
                return False
        self.boids.append(boid)
        return True

    def updateBoidsPos(self):
        for boid in self.boids:
            boid.updatePos()
    def updateBoidsV(self, screen: pg.Surface):
         for boid in self.boids:
            boid.updateVelo(screen)
            boid.addPredatorForce(screen)

    def drawBoids(self, screen: pg.Surface):
        for boid in self.boids:
            boid.draw(screen)

    def checkForClick(self, screen: pg.Surface, maxV=4, r=7.5, v_init=2, minV=3.5):
        if pg.mouse.get_pressed()[0]:
            x, y = pg.mouse.get_pos()
            y = screen.get_height() - y
            self.addBoid(Boid(x, y, maxV, r, v=v_init, minV=minV))
            print("Boid Created")

    def updateCommunities(self):
         for boid in self.boids:
             boid.updateCommunity(self.boids)
