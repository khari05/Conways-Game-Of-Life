from time import sleep
import numpy as np
import curses
import os

win = curses.initscr()
curses.noecho()
curses.cbreak()
win.keypad(True)

def genPoints():
    width, height = os.get_terminal_size()
    return np.zeros((height - 3, width))

def draw(point):
    if point == 0: return ' '
    if point == 1: return 'x'
    if point == 2: return '█'
    if point == 3: return '▒'
    return ' '

def getRow(row, col=0):
    if col == len(row) -1:
        return draw(row[col])
    else:
        return draw(row[col]) + getRow(row, col + 1)

def drawScreen(win, points, row=0):
    win.addstr(row + 2, 0, getRow(points[row]))
    if (row == len(points)-1):
        win.refresh()
    else:
        drawScreen(win, points, row + 1)

def runCycle(points):
    height = len(points)
    width = len(points[0])

    result = genPoints()
    for i in range(height):
        for j in range(width):
            n = 0
            alive = points[i][j] == 1
            left  = j != 0
            right = j != width - 1
            up    = i != 0
            down  = i != height - 1

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
            if alive and (n == 2 or n == 3):
                result[i][j] = 1

            # Rule 4: Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
            elif not alive and n == 3:
                result[i][j] = 1
    return result

def removeCursor(points, xy):
    x, y = xy
    point = points[y][x]
    point -= 2
    if point < 0: raise IndexError()

    points[y][x] = point

def addCursor(points, xy):
    x, y = xy
    point = points[y][x]
    point += 2
    if point > 3: raise IndexError()

    points[y][x] = point

def h(points, x, y):
    x, y = xy
    if x == 0: x = len(points[0]) - 1
    else: x -= 1
    return x, y

def j(points, x, y):
    x, y = xy
    if y == len(points) - 1: y = 0
    else: y += 1
    return x, y

def k(points, x, y):
    if y == 0: y = len(points) - 1
    else: y -= 1
    return x, y

def l(points, x, y):
    if x == len(points[0]) - 1: x = 0
    else: x += 1
    return x, y

def togglePoint(points, xy):
    x, y = xy
    point = points[y][x]
    if   point == 3: point = 2
    elif point == 2: point = 3
    else: raise IndexError()

    points[y][x] = point

movements = {
    ord('h'): h,
    ord('j'): j,
    ord('k'): k,
    ord('l'): l,
    curses.KEY_LEFT:  h,
    curses.KEY_RIGHT: l,
    curses.KEY_DOWN:  j,
    curses.KEY_UP:    k,
}

points = genPoints()

try:
    while True:
        win.addstr(0, 0, "Build mode: h, j, k, and l for movement, [Space] and x to toggle cells, q to simulate", curses.A_REVERSE)
        points[0][0] = 2
        xy = (0, 0)
        drawScreen(win, points)

        ch = win.getch()
        while ch != ord('\n'):
            if   ch == ord('q'): break
            elif ch == 32 or ch == ord('x'): togglePoint(points, xy)
            elif ch == curses.KEY_RESIZE: break
            else:
                removeCursor(points, xy)
                xy = movements[ch](points, xy[0], xy[1])
                addCursor(points, xy)
            drawScreen(win, points)
            ch = win.getch()

        removeCursor(points, xy)
        win.clear()
        win.addstr(0, 0, "Running Life: Press 'q' to return to build mode", curses.A_REVERSE)
        win.addstr(1, 0, 'Generation: 1')
        live = runCycle(points)

        win.nodelay(True)
        gen = 1
        while True:
            ch = win.getch()
            if ch is not None and ch == ord('q'): break
            if ch is not None and ch == curses.KEY_RESIZE: gen += 1; runCycle(live)
            win.addstr(1, 12, str(gen))
            drawScreen(win, live)
            sleep(0.1)
            gen += 1
            live = runCycle(live)
        win.nodelay(False)
        win.addstr(1, 12, '0' + ' '*5)

except KeyboardInterrupt:
    curses.nocbreak()
    win.keypad(False)
    curses.echo()
    curses.endwin()
    print()
    exit(0)
