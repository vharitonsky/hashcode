from typing import List
from collections import namedtuple


Point = namedtuple('Point', ('row', 'column'))
Size = namedtuple('Size', ('rows', 'columns'))


class Ride(object):
    def __init__(self, 
        start: Point, finish: Point,
        time_start: int, time_end: int
    ) -> None:
        self.start = start
        self.finish = finish
        self.time_start = time_start
        self.time_end = time_end

        self.duration = self.time_end - self.time_start
        self.length = (
            abs(start.row - finish.row)
            + abs(start.column - finish.column)
        )


class Problem(object):
    def __init__(self,
        num_rides: int, num_cars: int,
        size: Size, rides: List[Ride],
        in_time_start_bonus: int,
    ) -> None:
        self.num_rides = num_rides
        self.num_cars = num_cars
        self.size = size
        self.rides = rides
        self.in_time_start_bonus = in_time_start_bonus


def read(filename: str) -> Problem:
    with open(filename, 'r') as f:
        (
            total_rows, total_columns,
            num_cars, num_rides,
            in_time_start_bonus, steps
        ) = map(int, f.readline().split())

        rides = []

        for _ in range(num_rides):
            (
                start_row, start_column,
                end_row, end_column,
                earliest_start, latest_finish,
            ) = map(int, f.readline().split())
            rides.append(Ride(
                start=Point(start_row, start_column),
                finish=Point(end_row, end_column),
                time_start=earliest_start, time_end=latest_finish,
            ))

    return Problem(
        num_rides=num_rides,
        num_cars=num_cars,
        size=Size(rows=total_rows, columns=total_columns),
        rides=rides,
        in_time_start_bonus=in_time_start_bonus,
    )
