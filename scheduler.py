from collections import namedtuple


Point = namedtuple('Point', ('row', 'column'))


class Problem(object):
    pass


class Ride(object):
    def __init__(self, 
        start: Point, finish: Point,
        time_start: int, time_end: int
    ):
        self.start = start
        self.end = end
        self.time_start = time_start
        self.time_end = time_end

        self.duration = self.time_end - self.time_start
        self.length = abs(start.row - end.row) + abs(start.column - end.column)


def read(filename):
    with open(filename, 'r') as f:
        (
            total_rows, total_columns,
            num_veichles, num_rides,
            per_ride_bonus, steps
        ) = map(int, f.readline().split())

        rides = []

