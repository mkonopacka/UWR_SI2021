import numpy as np

def UDLR_to_coords(move: str) -> tuple:
    ''' Zamienia stringa reprezentujacego ruch na wspolrzedne '''
    pairs = {"U" : (-1,0), "D" : (1,0), "R" : (0,1), "L" : (0,-1)}
    return pairs[move]
    
def between(x,z,y):
    '''Zwraca prawde jesli z jest pomiedzy x a y (wlacznie)'''
    return (x <= z and z <= y) or (x >= z and z >= y)

def read_map(path: str) -> np.ndarray:
    ''' Wczytuje z pliku mape jako np.array i x j (i - wiersze, j - kolumny)'''
    map = []
    with open(path, "r") as f:
        for line in f.read().splitlines():
            map.append([p for p in line])
    return np.array(map)

def find_first(map, symbols):
    ''' Find first occurance of any symbol '''
    h,w = map.shape
    for row in range(h):
        for col in range(w):
            if map[row,col] in symbols:
                return (row, col)
    return None

def get_goals(map: np.ndarray, symbols: list) -> list:
    ''' Return list of coordinates of map entries containing one of symbols '''
    goals = []
    h,w = map.shape
    for row in range(h):
        for col in range(w):
            if map[row,col] in symbols:
                goals.append((row,col))
    return goals

def allowed_index(height, width, pos):
    row,col = pos
    return between(0,row,height-1) and between(0,col,width-1)

def around(pos: tuple, moves = [(0,1), (0,-1), (1,0), (-1,0)]):
    row,col = pos
    return [(row+drow, col+dcol) for drow,dcol in moves]

def dist(p1: tuple, p2: tuple) -> int:
    ''' Zwraca odleglosc manhatanska pomiedzy punktami p1 i p2'''
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
