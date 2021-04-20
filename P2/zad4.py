# przechodzi 6/11
''' AI 2021 Z4/P2 (Komandos)
Dane: prostokat n x m z polami "S", "G", "B", "#", " " (mapa)
Cel: sekwencja ruchow, która na pewno doprowadzila do G
Akcje: U, D, L, R (wejście na ścianę nie zmienia stanu)
Stan elementarny: wspolrzędne (x,y) komandosa
Stan (przekonań): set wszystkich mozliwych par (x,y) np. ((1,2),(0,0))
Stan końcowy = stan przekonań w którym wszystkie stany są końcowe
'''
import numpy as np
from random import choice
from typing import *
from algs import *
from utils import *

class DeadMoveError(Exception):
    ''' Wyjatek rzucany, kiedy jakis ruch nie zmienia juz stanu '''
    pass

def final_coords(coords: tuple, map: np.ndarray) -> bool:
    ''' Zwraca prawde jesli wspolrzedne wskazuja na cel '''
    return map[coords] in ['G', 'B']

def final_set(coords_set: frozenset, map: np.ndarray) -> bool:
    ''' Zwraca prawde jesli wszystkie wspolrzedne w zbiorze sa koncowe '''
    return all([final_coords(coords, map) for coords in coords_set])

def generate_new_set(coords_set: frozenset, move: str, map: np.ndarray) -> frozenset:
    ''' Dla zbioru wspolrzednych generuj nowy zbior po zrobieniu pojedynczego ruchu '''
    moves = {
        "U": move_U,
        "D": move_D,
        "R": move_R,
        "L": move_L
        }
    move_func = moves[move]
    return frozenset([move_func(coords, map) for coords in coords_set])

def moves_sequence(coords_set: frozenset, move_seq: str, map: np.ndarray) -> frozenset:
    ''' Dla zbioru wspolrzednych generuj nowy zbior po zrobieniu sekwencji ruchów;
        jesli znajdzie ruch dla ktorego stan sie nie zmienia, wyrzuca DeadMoveError '''
    moves = {
        "U": move_U,
        "D": move_D,
        "R": move_R,
        "L": move_L
        }
    for move in move_seq:
        move_func = moves[move]
        new_set = [move_func(coords, map) for coords in coords_set]
        if new_set == list(coords_set):
            raise DeadMoveError
        else:
            coords_set = new_set
    return frozenset(coords_set)
    
def move_U(coords: tuple, map: np.ndarray) -> tuple:
    ''' Zwraca pare (x,y) nowych wspolrzednych komandosa jesli jest w x,y i robi ruch U '''
    new_coords = (coords[0] - 1, coords[1])
    if map[new_coords] == '#': 
        return coords
    else: 
        return new_coords

def move_D(coords: tuple, map: np.ndarray) -> tuple:
    ''' Zwraca pare (x,y) nowych wspolrzednych komandosa jesli jest w x,y i robi ruch D '''
    new_coords = (coords[0] + 1, coords[1])
    if map[new_coords] == '#': 
        return coords
    else: 
        return new_coords

def move_R(coords: tuple, map: np.ndarray) -> tuple:
    ''' Zwraca pare (x,y) nowych wspolrzednych komandosa jesli jest w x,y i robi ruch  R'''
    new_coords = (coords[0], coords[1] + 1)
    if map[new_coords] == '#': 
        return coords
    else: 
        return new_coords

def move_L(coords: tuple, map: np.ndarray) -> tuple:
    ''' Zwraca pare (x,y) nowych wspolrzednych komandosa jesli jest w x,y i robi ruch L '''
    new_coords = (coords[0], coords[1] - 1)
    if map[new_coords] == '#': 
        return coords
    else: 
        return new_coords
    
def get_initial_set(map: np.ndarray) -> frozenset:
    ''' Generuje poczatkowy zbiór stanów na podstawie mapy '''
    coords_set = []
    rows,cols = map.shape
    for y in range(cols):
        for x in range(rows):
            if map[x,y] in ['S', 'B']:
                coords_set.append((x,y))
    return frozenset(coords_set)

def reduce_select(coords_set: frozenset, map: np.ndarray, moves_lst: list, max_moves = 20) -> Tuple[frozenset, list]:
    # JAKIEŚ SŁABE, GORSZE NIŻ TAMTO. CZEMU?
    ''' Zmniejszanie niepewnosci przez wybor ruchu po ktorym niepewnosc jest najmniejsza
        Zwraca stan po i listę ruchów.
        coords_set: wyjściowy zbiór'''
    path = []
    min_size = len(coords_set) # ilu teraz jest komandosow?
    for _ in range(max_moves):
        best_move = None 
        for move in moves_lst:
            try:
                new_set = moves_sequence(coords_set, move, map)
            except DeadMoveError:
                continue
            else:
                coords_set = new_set
                path.append(move)
            if len(new_set) < min_size: # jeśli udało się zmniejszyć niepewność, ustaw ten ruch jako najlepszy
                best_move = move
                best_set = new_set
                min_size = len(new_set)
        if best_move is None: # jeśli nie da się juz polepszyć niepewności, zakończ
            return (coords_set, path)
        else: 
            coords_set = best_set
            path.append(best_move)
    
    return (coords_set, path)

def reduce_max(coords_set: frozenset, map: np.ndarray, moves_lst: list) -> Tuple[frozenset, list]:
    ''' Zmniejszanie niepewnosci przez pójście max. w kazdym z kierunkow na liscie po kolei
        Zwraca stan po i listę ruchów.
        coords_set: wyjściowy zbiór'''
    rang = max(map.shape)
    path = []
    for move in moves_lst:
        for _ in range(rang):
            try:
                new_set = moves_sequence(coords_set, move, map)
            except DeadMoveError:
                break
            else:
                coords_set = new_set
                path.append(move)
    return coords_set, path

def reduce_random(coords_set: frozenset, map: np.ndarray, moves_lst: list, num = 100) -> Tuple[frozenset, list]:
    ''' Zmniejszanie niepewnosci przez zrobienie `num` losowych ruchow z listy `moves_lst`
        Zwraca stan po i listę ruchów.
        coords_set: wyjściowy zbiór'''
    path = []
    for _ in range(num):
        move = choice(moves_lst)
        try:
            new_set = moves_sequence(coords_set, move, map)
        except DeadMoveError:
            continue
        else:
            coords_set = new_set
            path.append(move)
    return coords_set, path

if __name__ == '__main__':
    map = read_map('zad_input.txt')
    initial_set = get_initial_set(map)
    h, w = map.shape
    double_moves = ["UR", "LD", "UL", "RD", "DR","LU","DL","LU"]
    triple_moves = ["URD", "LDR", "ULD", "RDL", "DRU","LUR","DLU","LUR"]

    # initial_set, path1 = reduce_max(initial_set, map, ['U'])
    # print(len(initial_set))

    # initial_set, path2 = reduce_max(initial_set, map, ['R'])
    # print(len(initial_set))
    print('____________________________________________________________________________________________________________')
    path = []
    for i in range(10000):
        new_set, path_ = reduce_random(initial_set, map, ['UUUUUUU', 'URURURU', 'RRRRRRR', 'RDRDRDR', 'DDDDDDD', 'DLDLDLD', 'LLLLLLL', 'LULULUL'], 20)
        if len(new_set) < 3:
            initial_set = new_set
            path3 = path_
            break
    print(len(initial_set))
    print(initial_set)

    path_bfs = BFS2(initial_set, final_set, generate_new_set, ["U", "D", "L", "R"], map = map)
    final = moves_sequence(initial_set, path_bfs, map)
    print(final)
    path = path3 + path_bfs
    print(len(path))

    with open('zad_output.txt', 'w') as f:
        for char in  path:
            f.write(char)