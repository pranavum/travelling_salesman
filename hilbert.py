import matplotlib.pyplot as plt
from math import inf, log, ceil
from random import randint

class Board:
    def __init__(self, n=0) -> None:
        self.n = n
        self.nodes = []
        self.path = []
    def setup(self):
        pass
    def findN(self):
        biggest = -inf
        for node in self.nodes:
            if node[0] > biggest:
                biggest = node[0]
            if node[1] > biggest:
                biggest = node[1]
        biggest += 1
        n = ceil(log(biggest)/log(2))
        return n
    def display(self):
        x, y = [node[0] for node in self.path], [node[1] for node in self.path]
        plt.plot(x,y, color='red')
    def findPath(self, frac):
        for point in frac.points:
            if point in self.nodes:
                self.path.append(point)

class Frac:
    def __init__(self, n=1) -> None:
        self.points = []
        self.n = n
        self.current = [0,0]
        self.dir = 0
    def move(self, len=1):
        cur = self.current[:]
        self.dir = self.dir % 360
        if self.dir == 90:
            cur[0] += len
        if self.dir == 270:
            cur[0] -= len
        if self.dir == 0:
            cur[1] += len
        if self.dir == 180:
            cur[1] -= len
        self.points.append(cur)
        return cur
    def recur(self, n):
        self.points.append(self.current)
        if n > 1:
            f.dir += 90
            f.reverseRecur(n-1)
            if n % 2 == 0:
                f.dir += 90
            f.current = f.move()
            f.recur(n-1)
            if n % 2 == 0:
                f.dir -= 90
            f.current = f.move()
            f.dir -= 90
            f.recur(n-1)
            if n % 2 == 1:
                f.dir += 90
            f.current = f.move()
            f.dir += 90
            f.reverseRecur(n-1)
        else:
            self.current = self.move()
            self.dir += 90
            self.current = self.move()
            self.dir += 90
            self.current = self.move()
    def reverseRecur(self, n):
        if n > 1:
            f.dir -= 90
            f.recur(n-1)
            if n % 2 == 0:
                f.dir -= 90
            f.current = f.move()
            f.reverseRecur(n-1)
            if n % 2 == 0:
                f.dir += 90
            f.current = f.move()
            f.dir += 90
            f.reverseRecur(n-1)
            if n % 2 == 1:
                f.dir -= 90
            f.current = f.move()
            f.dir -= 90
            f.recur(n-1)
        else:
            self.points.append(self.current)
            self.current = self.move()
            self.dir -= 90
            self.current = self.move()
            self.dir -= 90
            self.current = self.move()
    def display(self):
        x, y = [point[0] for point in self.points], [point[1] for point in self.points]
        plt.plot(x, y)

b = Board()
b.nodes = [[randint(0,63),randint(0,63)] for n in range(100)]

f = Frac()
f.recur(b.findN())

b.findPath(f)

b.display()
f.display()
plt.show()
