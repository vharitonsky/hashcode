from domain import Point, Problem, Ride, Size, World


def read(filename: str) -> Problem:
    with open(filename, 'r') as f:
        (
            total_rows, total_columns,
            num_cars, num_rides,
            in_time_start_bonus, steps
        ) = map(int, f.readline().split())

        rides = []

        for i in range(num_rides):
            (
                start_row, start_column,
                end_row, end_column,
                earliest_start, latest_finish,
            ) = map(int, f.readline().split())
            rides.append(Ride(
                start=Point(start_row, start_column),
                finish=Point(end_row, end_column),
                time_start=earliest_start, time_end=latest_finish,
                index=i
            ))

    return Problem(
        num_rides=num_rides,
        num_cars=num_cars,
        size=Size(rows=total_rows, columns=total_columns),
        rides=rides,
        in_time_start_bonus=in_time_start_bonus,
        num_steps=steps,
    )


def write(filename: str, world: World) -> None:
    with open(filename, 'w') as out:
        for car in world.cars:
            out.write(str(len(car.ride_history)))
            out.write(' ')
            out.write(' '.join(map(str, car.ride_history)))
            out.write('\n')
