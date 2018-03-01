import sys

from domain import World
from fileutils import read, write


if __name__ == '__main__':
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    world = World(read(in_file))
    world.run()
    write(out_file, world)

    print(f'Total score: {world.total_score}')
