import pygame as pg
from math import cos, sin, sqrt, pi
from random import random

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (172, 216, 230)


class Boid:
    def __init__(self, x, y, maxV, r, theta=random() * 2 * pi, v=2, relativeCommunity=1000, minV=0.5): # if you delete the init val for theta then every thing goes in a different direction
        self.x = x
        self.y = y
        self.pos = pg.Vector2(x, y)
        self.maxV = maxV
        self.r = r
        print(theta == 0)
        self.theta = random() * 2 * pi if theta == 0 else theta
        print("Theta is " + str(self.theta))
        self.v = v
        self.velo = pg.Vector2(v * cos(self.theta), v * sin(self.theta))
        self.boidCommunity = []
        self.relativeCommunity = relativeCommunity # How many body radiusus a boid can see
        self.minV = minV
        print(theta)

    def draw(self, screen: pg.Surface):
        # I'm changing the position system such that the bottom left is (0, 0)
        pg.draw.circle(screen, LIGHT_BLUE, (self.x, screen.get_height() - self.y), self.r)

    def updatePos(self):
        self.pos += self.velo
        self.x, self.y = self.pos

    def updateVelo(self, screen: pg.Surface):
        a = pg.Vector2(0, 0)
        # Have Walls Exert a force on the boid acording to the inverse square law
        k = 1000
        a += k * pg.Vector2(-1, 0) / ((screen.get_width() - self.x) ** 2) # Right wall
        # Left wall
        a += k * pg.Vector2(1, 0) / ((self.x) ** 2)
        # Bottom Wall
        a += k * pg.Vector2(0, 1) / ((self.y) ** 2)
        # Top Wall
        a += k * pg.Vector2(0, -1) / ((screen.get_height() - self.y) ** 2)

        # Rule 1: Seperation
        k2 = 2
        for boid in self.boidCommunity:
            if (self.pos - boid.pos).magnitude() < 2 * self.r:
                unitV = (self.pos - boid.pos).normalize()
                a += k2 * unitV / (self.pos.distance_to(boid.pos) - self.r - boid.r) * self.maxV

        # Rule 2: Coherence
        d = 0.1 * self.r # distance we want equillibrium between cohesion and seperations
        k3 = 1 #(d + 1) / (d ** 2 + 1) * k2
        if len(self.boidCommunity) != 0:
            cMass = pg.Vector2(0, 0)
            for boid in self.boidCommunity:
                cMass += boid.pos
            cMass /= len(self.boidCommunity)
            a += (cMass - self.pos) * k3

        # Rule 3: Alignment
        k4 = 1
        if len(self.boidCommunity) != 0:
            cVelo = pg.Vector2(0, 0)
            for boid in self.boidCommunity:
                cVelo += boid.velo
            cVelo /= len(self.boidCommunity)
            if cVelo != self.velo:
                a += (cVelo - self.velo).normalize() * k4 * self.maxV

        # Update velo
        print("Accel: " + str(a.magnitude()))
        a = Boid.clamp(a, 0, 0.2)
        self.velo += a
        self.velo = Boid.clamp(self.velo, self.minV, self.maxV)

        # Making Variables Consistent
        self.v = self.velo.length()
        self.theta = self.velo.angle_to(pg.Vector2(0, 0))

    def updateCommunity(self, allBoids: list):
        temp = []
        for boid in allBoids:
            if boid is not self and self.pos.distance_to(boid.pos) <= self.relativeCommunity * self.r:
                temp.append(boid)
        self.boidCommunity = temp

    @staticmethod
    def detectCollision(boid1, boid2) -> bool:
        assert type(boid1) == Boid
        assert type(boid2) == Boid
        d = sqrt((boid1.x - boid2.x) ** 2 + (boid2.y - boid1.y) ** 2)
        return boid2.r + boid1.r >= d

    @staticmethod
    def clamp(val: pg.Vector2, min, max):
        if val.magnitude() < min:
            return val.normalize() * min
        elif val.magnitude() > max:
            return val.normalize() * max
        else:
            return val