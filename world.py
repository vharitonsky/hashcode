import random
from scheduler import Ride


cars = []
rides = []


class World:

    step = 0

    def next_step(self):

        self.step += 1

        for car in cars:
            car.next()


class Car:
    assigned_ride = None

    row = 0
    column = 0

    def next(self):
        if self.assigned_ride:
            if not self.assigned_ride.started:
                self.move()
            else:
                self.move()
        else:
            self.assigned_ride = random.choice(rides)
            rides.remove(self.assigned_ride)

    def move(self):
        if self.assigned_ride.started:
            to = self.assigned_ride.finish
        else:
            to = self.assigned_ride.start
        if self.row > to.row:
            self.row -= 1
        elif self.row < to.row:
            self.row += 1
        elif self.column > to.column:
            self.column -= 1
        elif self.column < to.column:
            self.column += 1