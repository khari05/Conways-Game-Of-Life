from ast import Lambda
from time import sleep
import numpy as np
import curses
import os

# width, height = os.get_terminal_size()

height = 30
width = 60
points = np.zeros((height, width))

points[3][4] = 1
points[3][5] = 1
points[2][6] = 1
points[4][3] = 1
points[4][7] = 1
points[4][6] = 1
points[1][3] = 1
points[4][4] = 1
points[4][5] = 1
points[5][6] = 1
# points[6][7] = 1

# points[5][6] = 1
# points[6][6] = 1
# points[7][6] = 1
# points[7][5] = 1
# points[6][4] = 1

def draw(point):
    if point == 0: return ' '
    if point == 1: return 'x'

def getRow(row, col):
    if col == len(row) -1:
        return draw(row[col])
    else:
        return draw(row[col]) + getRow(row, col + 1)

def getMatrix(points, row=0):
    if (row == len(points)-1):
        return getRow(points[row], 0)
    else:
        return getRow(points[row], 0) + '\n' + getMatrix(points, row + 1)

def runCycle(points):
    result = np.zeros((len(points), len(points[0])))
    for i in range(len(points)):
        for j in range(len(points[0])):
            n = 0
            alive = points[i][j] == 1
            left  = j != 0
            right = j != len(points[0]) - 1
            up    = i != 0
            down  = i != len(points) - 1

            # count neighbours
            if left and up:    n += points[i-1][j-1] 
            if up:             n += points[i-1][j]
            if up and right:   n += points[i-1][j+1]
            if left:           n += points[i][j-1]
            if right:          n += points[i][j+1]
            if down and left:  n += points[i+1][j-1]
            if down:           n += points[i+1][j]
            if down and right: n += points[i+1][j+1]

            # Rule 1: Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            # Rule 2: Any live cell with two or three live neighbours lives on to the next generation.
            # Rule 3: Any live cell with more than three live neighbours dies, as if by overpopulation.
            if alive and (n < 2 or n > 3):
                result[i][j] = 0
            elif alive:
                result[i][j] = 1

            # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            elif not alive and n == 3:
                result[i][j] = 1
            else: result[i][j] = 0
    return result

for i in range(2000):
    print(getMatrix(points))
    points = runCycle(points)
    sleep(0.1)
# print(getMatrix(points))
