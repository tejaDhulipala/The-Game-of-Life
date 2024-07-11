import pygame as pg
from math import cos, sin, sqrt, pi, fabs
from random import random

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (172, 216, 230)


class Boid:
    def __init__(self, x, y, maxV, r, theta=0, v=2, relativeCommunity=20, minV=0.5): # if you delete the init val for theta then every thing goes in a different direction
        self.x = x
        self.y = y
        self.pos = pg.Vector2(x, y)
        self.maxV = maxV
        self.r = r
        self.theta = pi / 4 #random() * 2 * pi if theta == 0 else theta
        self.v = v
        self.velo = pg.Vector2(v * cos(self.theta), v * sin(self.theta))
        self.boidCommunity = []
        self.relativeCommunity = relativeCommunity # How many body radiusus a boid can see
        self.minV = minV

    def draw(self, screen: pg.Surface):
        # I'm changing the position system such that the bottom left is (0, 0)
        pg.draw.circle(screen, LIGHT_BLUE, (self.x, screen.get_height() - self.y), self.r)

    def updatePos(self):
        self.pos += self.velo
        self.x, self.y = self.pos

    def updateVelo(self, screen: pg.Surface):
        a = pg.Vector2(0, 0)
        wallForce = pg.Vector2(0, 0)
        # Have Walls Exert a force on the boid acording to the inverse square law
        k = 1
        # Right wall
        # wallForce += k * pg.Vector2(-1, 0) / ((screen.get_width() - self.x) ** 2 + 1)
        # wallForce += k * pg.Vector2(-1, 0) if (screen.get_width() - self.x) < 50 else pg.Vector2(0, 0)
        # Left wall
        # wallForce += k * pg.Vector2(1, 0) / ((self.x) ** 2 + 1)
        # wallForce += k * pg.Vector2(1, 0) if self.x < 50 else pg.Vector2(0, 0)
        # Bottom Wall
        # wallForce += k * pg.Vector2(0, 1) / ((self.y) ** 2 + 1)
        # wallForce += k * pg.Vector2(0, 1) if self.y < 50 else pg.Vector2(0, 0)
        # Top Wall
        # wallForce += k * pg.Vector2(0, -1) / ((screen.get_height() - self.y) ** 2 + 1)
        # wallForce += k * pg.Vector2(0, -1) if (screen.get_height() - self.y) < 50 else pg.Vector2(0, 0)
        # a += wallForce

        # Rule 1: Seperation
        k2 = 10
        for boid in self.boidCommunity:
                if 4 * self.r > (self.pos - boid.pos).magnitude() > 0:
                    unitV = (self.pos - boid.pos).normalize()
                    steering = k2 * unitV / ((self.pos.distance_to(boid.pos) - self.r - boid.r) ** 2)
                    # steering = steering.normalize()
                    # steering *= 0.07
                    steering = Boid.clamp(steering, 0, 1)
                    a += steering

        # Rule 2: Coherence
        d = 0.1 * self.r # distance we want equillibrium between cohesion and seperations
        k3 = 1 #(d + 1) / (d ** 2 + 1) * k2
        if len(self.boidCommunity) != 0:
            cMass = pg.Vector2(0, 0)
            for boid in self.boidCommunity:
                cMass += boid.pos
            cMass /= len(self.boidCommunity)
            steering = (cMass - self.pos).normalize() * k3
            steering = Boid.clamp(steering, 0, 1)
            a += steering

        # Rule 3: Alignment
        k4 = 1
        if len(self.boidCommunity) != 0:
            desired = pg.Vector2(0, 0)
            for boid in self.boidCommunity:
                desired += boid.velo
            desired /= len(self.boidCommunity)
            if desired != self.velo:
                steering = (desired - self.velo).normalize() * k4
                steering = Boid.clamp(steering, 0, 1)
                a += steering

        # Applying the Wall force

        # Top wall
        d = 120
        t = 360 / d
        if (screen.get_height() - self.pos.y < d):
            if self.velo.x < 0:
                self.velo = self.velo.rotate(t)
            else:
                self.velo = self.velo.rotate(-t)
        # Bottom Wall
        elif self.pos.y < d:
             if self.velo.x > 0:
                 self.velo = self.velo.rotate(t)
             else:
                 self.velo = self.velo.rotate(-t)
        # Left Wall
        elif self.pos.x < d:
            if self.velo.y < 0:
                self.velo = self.velo.rotate(t)
            else:
                self.velo = self.velo.rotate(-t)
        # Right wall
        elif screen.get_width() - self.pos.x < d:
            if self.velo.y > 0:
                self.velo = self.velo.rotate(t)
            else:
                self.velo = self.velo.rotate(-t)

        # Update velo
        # print("Accel: " + str(a.magnitude()))
        a = Boid.clamp(a, 0, 0.1)
        self.velo += a
        # self.velo *= 1.0075

        self.velo = Boid.clamp(self.velo, self.minV, self.maxV)
        print(self.velo.length())

        # Making Variables Consistent
        self.v = self.velo.length()
        self.theta = self.velo.angle_to(pg.Vector2(0, 0))

    def updateCommunity(self, allBoids: list):
        temp = []
        for boid in allBoids:
            if boid is not self and self.pos.distance_to(boid.pos) <= self.relativeCommunity * self.r:
                temp.append(boid)
        self.boidCommunity = temp

    def addPredatorForce(self, screen: pg.Surface):
        if (pg.mouse.get_pressed()[2]):
            force = pg.Vector2(self.pos[0] - pg.mouse.get_pos()[0], self.pos[1] - (screen.get_height() - pg.mouse.get_pos()[1]))
            force = 50 * force.normalize() / (force.magnitude() + 5)
            self.velo += force
            pg.draw.circle(screen, (255, 0, 0), pg.mouse.get_pos(), 5)


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
        elif val.magnitude() >= max:
            return val.normalize() * max
        else:
            return val