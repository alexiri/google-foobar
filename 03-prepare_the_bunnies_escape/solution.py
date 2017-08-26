import cProfile, pstats, StringIO
from timeit import default_timer as timer

from collections import deque

def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not maze[i][j]}
    for row, col in graph.keys():
        if row < height - 1 and not maze[row + 1][col]:
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and not maze[row][col + 1]:
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph

def find_path_bfs(maze):
    # print('\nstarting')
    start, goal = (0, 0), (len(maze) - 1, len(maze[0]) - 1)
    queue = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)
    while queue:
        # print('queue: {}'.format(queue))
        path, current = queue.popleft()
        # print('current: {}, path: {}'.format(current, path))
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            # print(' add to queue {}'.format(direction))
            queue.append((path + direction, neighbour))
    return None

def shortestPath(maze):
    path = find_path_bfs(maze)
    if path:
        return len(path)+1
    return -1

def deepcopy(stuff):
    return [row[:] for row in stuff]

def getAllVariations(maze):
    maps = [maze]

    maxY = len(maze)
    maxX = len(maze[0])
    for y in range(maxY):
        for x in range(maxX):
            if maze[y][x] == 1:
                # print('new version')
                t = deepcopy(maze)
                t[y][x] = 0
                maps.append(t)

    return maps


def answer(maze):
    mazes = getAllVariations(maze)

    lengths = [shortestPath(m) for m in mazes]
    lengths = filter(lambda l: l>0, lengths)

    return min(lengths)


map1 = [[0, 0, 1, 0],
        [1, 0, 1, 0],
        [1, 0, 0, 1],
        [1, 1, 0, 0]]

map2 = [[0, 0, 1, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 1, 0, 0]]

map3 = [[0, 0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 0]]

map4 = [[0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0]]

map9 = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]]

maze1 = [ [0, 1, 1, 0],
          [0, 0, 0, 1],
          [1, 1, 0, 0],
          [1, 1, 1, 0]]

maze2 = [ [0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1],
          [0, 1, 1, 1, 1, 1],
          [0, 0, 0, 0, 0, 0]]

def bench(maze):
    pr = cProfile.Profile()
    pr.enable()
    start = timer()
    res = answer(maze)
    end = timer()
    pr.disable()

    print('Elapsed: {}'.format(end-start))
    print(' -> {}'.format(res))

    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s)
    ps.strip_dirs().sort_stats(sortby).print_stats()
    print s.getvalue()

bench(map9)
