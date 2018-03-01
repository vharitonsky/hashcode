from typing import List, Optional
from collections import namedtuple

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


Point = namedtuple('Point', ('row', 'column'))
Size = namedtuple('Size', ('rows', 'columns'))


def distance(start: Point, end: Point) -> int:
    return abs(start.row - end.row) + abs(start.column - end.column)


class Ride(object):
    def __init__(
        self,
        start: Point, finish: Point,
        time_start: int, time_end: int, index: int
    ) -> None:
        self.started = False
        self.start = start
        self.finish = finish
        self.time_start = time_start
        self.time_end = time_end
        self.index = index

        self.duration = self.time_end - self.time_start
        self.distance = distance(start, finish)

    @property
    def length(self) -> int:
        """Backward compatibility"""
        return self.distance


class Problem(object):
    def __init__(
        self,
        num_rides: int, num_cars: int,
        size: Size, rides: List[Ride],
        in_time_start_bonus: int,
        num_steps: int,
    ) -> None:
        self.num_rides = num_rides
        self.num_cars = num_cars
        self.size = size
        self.rides = rides
        self.in_time_start_bonus = in_time_start_bonus
        self.num_steps = num_steps

    @property
    def number_of_steps(self) -> int:
        """Backward compatibility"""
        return self.num_steps


class World(object):
    def __init__(self, problem: Problem) -> None:
        self.step = 0
        self.problem = problem
        self.cars = [Car() for _ in range(problem.num_cars)]
        self.rides = problem.rides

        self.total_score = 0

    def run(self) -> None:
        self.rides = [ride for ride in self.rides if ride.time_end > self.step]
        while self.step < self.problem.number_of_steps:
            self.next_step()

    def next_step(self) -> None:
        # self.render()
        self.step += 1
        print(f'{self.step} / {self.problem.num_steps}', end='\r')
        self.rides = list(filter(
            lambda r: self.step + r.distance <= r.time_end,
            self.rides
        ))

        for car in self.cars:
            car.next(self)

    def render(self):
        matrix = [['%'] * self.problem.size.rows
                  for _ in range(self.problem.size.columns)]
        for i, car in enumerate(self.cars):
            matrix[car.column][car.row] = i
            if car.assigned_ride:
                finish = car.assigned_ride.finish
                matrix[finish.column][finish.row] = ALPHABET[i]

        print('-' * 80)
        for column in matrix:
            for el in column:
                print(el, end=' ')
            print()


class Car(object):
    def __init__(self):
        self.assigned_ride: Optional[Ride] = None
        self.current_score: int = 0
        self.row: int = 0
        self.column: int = 0
        self.ride_history: List[Ride] = []

    @property
    def coordinates(self) -> Point:
        return Point(self.row, self.column)

    def next(self, world):
        if (
            self.assigned_ride and
            self.assigned_ride.started and
            self.coordinates == self.assigned_ride.finish
        ):
            if world.step < self.assigned_ride.time_end:
                world.total_score += self.current_score
            self.ride_history.append(self.assigned_ride.index)
            self.assigned_ride = None
            self.current_score = 0

        if self.assigned_ride:
            self.move(world)
        else:
            if world.rides:
                self.assigned_ride = self.choose(world)
                if self.assigned_ride:
                    world.rides.remove(self.assigned_ride)
                    self.move(world)

    def choose(self, world: World) -> Optional[Ride]:
        rides = world.rides
        coords = self.coordinates

        def metric(ride: Ride) -> float:
            distance_to_ride = distance(coords, ride.start)
            total_time = distance_to_ride + ride.distance
            if world.step + distance_to_ride < ride.time_start:
                total_time += ride.time_start - (world.step + distance_to_ride)

            win = ride.distance
            if total_time + world.step > ride.time_end:
                win -= ride.distance
            if world.step + distance_to_ride <= ride.time_start:
                win += world.problem.in_time_start_bonus
            return win / total_time

        best_ride, best_metric = None, float('-Inf')

        for ride in rides:
            ride_metric = metric(ride)
            if ride_metric > best_metric:
                best_ride, best_metric = ride, ride_metric

        return best_ride

    def move(self, world: World) -> None:
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
            self.coordinates == self.assigned_ride.start
            and world.step >= self.assigned_ride.time_start
        ):
            self.assigned_ride.started = True
            if self.assigned_ride.time_start == world.step:
                self.current_score = world.problem.in_time_start_bonus
