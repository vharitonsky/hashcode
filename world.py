import sys
import random
from scheduler import Ride, Problem, read

cars = []

total_score = 0


class World:
    def __init__(self, problem: Problem) -> None:
        self.step = 0
        self.problem = problem
        self.cars = [Car() for _ in range(problem.num_cars)]
        self.rides = problem.rides

    def run(self):
        self.rides = [ride for ride in self.rides if ride.time_end > self.step]
        while self.step < self.problem.number_of_steps:
            self.next_step()

    def next_step(self):
        self.step += 1

        for car in self.cars:
            car.next()


class Car:

    def __init__(self):
        self.assigned_ride = None
        self.current_score = 0
        self.row = 0
        self.column = 0
        self.ride_history = []

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
            self.ride_history.append(self.assigned_ride.index)
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
            if self.assigned_ride.time_start == world.step:
                self.current_score = world.problem.in_time_start_bonus


if __name__ == '__main__':
    init_file = sys.argv[1]
    out_file = sys.argv[2]
    world = World(read(init_file))
    world.run()
    print(total_score)
    with open(out_file, 'w') as out:
        for car in world.cars:
            out.write(str(len(car.ride_history)))
            out.write(' ')
            out.write(' '.join(map(str, car.ride_history)))
            out.write('\n')
