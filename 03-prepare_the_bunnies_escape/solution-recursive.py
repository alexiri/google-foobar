from timeit import default_timer as timer
from pprint import pprint

from copy import deepcopy
from math import sqrt

class Path(object):
    def __init__(self, start=(0,0)):
        self.steps = [start]

    def __repr__(self):
        try:
            ret = str(self.steps[0])
            for s in self.steps[1:]:
                ret += ' -> {}'.format(s)
        except IndexError:
            ret = ''
        return 'Path({}) - {}'.format(ret, len(self))

    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return len(self.steps)

    def getLastPosition(self):
        if len(self.steps) > 0:
            return self.steps[-1]
        return (0, 0)

    def nextStep(self, move):
        # if move in self.steps:
        #     raise Exception("Going backwards is for cowards")
        self.steps.append(move)

    def isBacktrack(self, move):
        return move in self.steps

class Map(object):
    def __init__(self, map):
        self.map = map
        self.maxX = len(self.map[0])-1
        self.maxY = len(self.map)-1
        self.all_paths = None
        self.shortest = None
        self.blockDeadEnds()

    def __repr__(self):
        return 'Map({}x{})'.format(self.maxX+1, self.maxY+1)

    def distance(self, pos):
        a = self.maxX - pos[0]
        b = self.maxY - pos[1]
        return sqrt(a*a + b*b)

    def at(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return -1
        try:
            #print('looking in r{}, c{} -> {}'.format(pos.y, pos.x, self.map[pos.y][pos.x]))
            return self.map[pos[1]][pos[0]]
        except IndexError:
            return -1

    def possible_movements(self, pos):
        movements = []

        # down
        if self.at( (pos[0], pos[1]+1) ) == 0:
        #    print('could go down')
           movements.append( (pos[0], pos[1]+1) )
        # else:
        #    print("can't go down")

        # right
        if self.at( (pos[0]+1, pos[1]) ) == 0:
            # print('could go right')
            movements.append( (pos[0]+1, pos[1]) )
        # else:
        #     print("can't go right")

        # left
        if self.at( (pos[0]-1, pos[1]) ) == 0:
            # print('could go left')
            movements.append( (pos[0]-1, pos[1]) )
        # else:
        #     print("can't go left")

        # up
        if self.at( (pos[0], pos[1]-1) ) == 0:
            # print('could go up')
            movements.append( (pos[0], pos[1]-1) )
        # else:
        #    print("can't go up")

        return movements

    def blockDeadEnds(self):
        print('starting:')
        pprint(self.map)
        self.original_map = deepcopy(self.map)

        while True:
            changed = False
            for y in range(self.maxY+1):
                for x in range(self.maxX+1):
                    if (x == 0 and y == 0) or (x == self.maxX and y == self.maxY):
                        # skip the entrance and exit
                        continue

                    if self.at( (x, y) ) == 0:
                        moves = self.possible_movements( (x, y) )
                        if len(moves) < 2:
                            self.map[y][x] = 2
                            changed = True
                            # print(' - changed {},{}'.format(x,y))
            if not changed:
                break
            # print('one loop done')
            # print(self.map)

        print('all done!')
        pprint(self.map)

        # distances = []
        # for y in range(self.maxY+1):
        #     distances.append([])
        #     for x in range(self.maxX+1):
        #         distances[y].append( self.distance((x,y)) )
        # pprint(distances)
        return self.map


    def getAllPaths(self):
        p = Path()

        def traverse(self, all_paths, path):
            origin = path.getLastPosition()

            # print('path {}, {}, max {}'.format(len(path), self, (self.maxX+1)*(self.maxY+1)))
            # print(path)
            # print('current winner: {}'.format(self.shortest))
            if self.shortest != None and len(path) >= self.shortest:
                # print(' - enough!')
                return all_paths

            movements = [m for m in self.possible_movements(origin) if not path.isBacktrack(m)]
            # print('possible: {}'.format(movements))

            if len(movements) > 0:
                # print 'multiple paths'
                # sort the moves by how close they would get us to the end
                movements.sort(key=lambda m: self.distance(m))
                for move in movements:
                    # print(move)
                    try:
                        p2 = Path()
                        p2.steps = path.steps[:]
                        #p2.fromFork(path.fork())

                        p2.nextStep(move)
                        #print('-> {}'.format(p2))
                        traverse(self, all_paths, p2)

                    except Exception, e:
                        print(e)
            # elif len(movements) == 1:
            #     path.nextStep(movements[0])
            #     # print path
            #     traverse(self, all_paths, path)
            else:
                end = path.getLastPosition()
                # print(' = end of the line! {}'.format(path))
                if end[0] == self.maxX and end[1] == self.maxY:
                    # print(' == finished!')
                    all_paths.append(path)
                    if self.shortest == None or self.shortest > len(path):
                        # print(' === new record: {}'.format(len(path)))
                        self.shortest = len(path)

            return all_paths

        if self.all_paths == None:
            self.all_paths = traverse(self, [], p)
            self.all_paths.sort(key=lambda p: len(p))

        # print('final: {}'.format(self.all_paths))
        return self.all_paths

    def getShortestPath(self):
        try:
            return self.getAllPaths()[0]
        except IndexError:
            return None

    def getShortestPathLength(self):
        try:
            return len(self.getShortestPath())
        except TypeError:
            return None

    # def getAllVariations(self):
    #     maps = [self]
    #
    #     for r in range(self.maxX+1):
    #         for c in range(self.maxY+1):
    #             if self.at((r, c)) == 1:
    #                 # print('new version')
    #                 t = deepcopy(self.map)
    #                 t[c][r] = 0
    #                 maps.append(Map(t))
    #
    #     return maps

    def getShortestVariation(self):
        shortest = self.getShortestPathLength()

        for r in range(self.maxX+1):
            for c in range(self.maxY+1):
                if self.at((r, c)) == 1:
                    # print('new version')
                    t = deepcopy(self.original_map)
                    t[c][r] = 0
                    newmap = Map(t)
                    newmap.shortest = shortest
                    new = newmap.getShortestPathLength()
                    if new and new < shortest:
                        shortest = new

        return shortest


def answer(map):
    map = Map(map)

    # all_maps = map.getAllVariations()
    # lengths = [m.getShortestPathLength() for m in all_maps]
    #
    # return min(filter(lambda l: l>0, lengths))
    return map.getShortestVariation()
    #return map.getShortestPath()

def bench(map):
    start = timer()
    res = answer(map)
    end = timer()

    print('Elapsed: {}'.format(end-start))
    print(' -> {}'.format(res))

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


# start = timer()
# for i in range(1000):
#     mapt = deepcopy(map3)
# end = timer()
# print('deepcopy Elapsed: {}'.format(end-start))
#
#
# paths = Map(map1).getAllPaths()
# p = paths[0]
# p2 = Path()
# print(p, p2)
#
# p2.fromFork(p.fork())
# print(p, p2)

import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
# assert answer(maze1) == 7
# assert answer(maze2) == 11
# bench(maze1)
# bench(maze2)
bench(maze2)
#answer(map2)
pr.disable()

s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s)
ps.strip_dirs().sort_stats(sortby).print_stats()
print s.getvalue()
