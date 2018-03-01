import sys
import random
from scheduler import Ride, Problem, read

cars = []

total_score = 0

alphabet = 'abcdefghijklmnopqrstuvwxyz'

class World:
    def __init__(self, problem: Problem) -> None:
        self.step = 0
        self.problem = problem
        self.cars = [Car() for _ in range(problem.num_cars)]
        self.rides = problem.rides

    def run(self):
        while self.step < self.problem.number_of_steps:
            self.next_step()

    def next_step(self):
        self.render()
        self.step += 1

        for car in self.cars:
            car.next()

    def render(self):
        matrix = [['%'] * self.problem.size.rows
                  for _ in range(self.problem.size.columns)]
        for i, car in enumerate(self.cars):
            matrix[car.column][car.row] = i
            if car.assigned_ride:
                finish = car.assigned_ride.finish
                matrix[finish.column][finish.row] = alphabet[i]

        print('-' * 80)
        for column in matrix:
            for el in column:
                print(el, end=' ')
            print()


class Car:
    assigned_ride = None
    current_score = 0

    row = 0
    column = 0

    def next(self):
        global total_score
        global world
        if (
            self.assigned_ride and
            self.assigned_ride.started and
            self.row == self.assigned_ride.finish.row and
            self.column == self.assigned_ride.finish.column
        ):
            if world.step < self.assigned_ride.time_end:
                total_score += self.current_score
            self.assigned_ride = None
            self.current_score = 0

        if self.assigned_ride:
            self.move()
        else:
            if world.rides:
                self.assigned_ride = random.choice(world.rides)
                world.rides.remove(self.assigned_ride)
                self.move()

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
        if self.assigned_ride.started:
            self.current_score += 1
        if (
            self.row == self.assigned_ride.start.row and
            self.column == self.assigned_ride.start.column and
            world.step >= self.assigned_ride.time_start
        ):
            self.assigned_ride.started = True


if __name__ == '__main__':
    init_file = sys.argv[1]
    world = World(read(init_file))
    world.run()
    print(total_score)
