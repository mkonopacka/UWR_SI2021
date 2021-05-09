# Moduł do obrazków logicznych
from os import error
from typing import *
from functools import lru_cache
import numpy as np

def draw(board, file = None):
    ''' Rysuje obrazek, jesli podano to do pliku '''
    repr = {0: ".", 1: "#", 2: "?"}
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(repr[board[i][j]], end ='', file = file) # podmienione miejsca wzgl. listy 1 (tam jest złe wczytywanie)
        print(file = file)
    print(file = file)

@lru_cache(maxsize = None)
def possible_ones(n: int, parts: tuple) -> List[list]:
    ''' Zwraca listę możliwych do ustawienia ciągów długości `n` z długościami bloków podanymi w `parts`'''
    p = len(parts)
    if (sum(parts) + p - 1 > n):
        raise ValueError('Sumaryczna długość bloków z przerwami przekracza długość ciągu')
    
    # długość pierwszej części się przyda
    l = parts[0]

    # jeśli został już tylko jeden blok
    if p == 1:
        # end = start + l - 1 < n => start < n + 1 - l
        return [[0]*start + [1]*l + [0]*(n-l-start) for start in range(n + 1 - l)]
    
    else:
        # dla każdego możliwego początku dołączyć wszystkie możliwe końce
        # obl. max. indeks końca pierwszego ciągu; musi zostać r_min miejsc na resztę ciągu (przed każdym z bloków wolne miejsce)
        r_min = sum(parts[1:]) + len(parts[1:])
        max = n - r_min
        heads = [[0]* x + [1]*l for x in range(0,max - l + 1)]
        merged = []
        for head in heads:
            tails = possible_ones(n - len(head) - 1, parts[1:])
            # print(f'Tails for head {head}: {tails}')
            for tail in tails:
                merged.append(head + [0] + tail)
        return merged

def read_spec(file_in: str) -> Tuple[int, int, Tuple[Tuple[int]], Tuple[Tuple[int]]]:
    ''' Wczytuje z pliku txt dane w formacie: nrows \n ncols \n [row1] \n [row2] ... [col1] ... i zwraca krotkę
    nrows, ncols, rows, cols (dwa ostatnie to krotki krotek - na potrzeby hashowania przez @lru_cache. '''
    with open(file_in) as file_in:
        lines = file_in.read().splitlines()
        nrows, ncols = map(int, (lines[0]).split())
        rows = tuple(map(tuple, [list(map(int, seq.split())) for seq in lines[1: 1+nrows]]))
        cols = tuple(map(tuple, [list(map(int, seq.split())) for seq in lines[1+nrows: ]]))
    return (nrows, ncols, rows, cols)

def choose_one(nrow, ncol):
    ''' Wybiera kolumnę lub wiersz do sprawdzenia (TERAZ: losowo) i zwraca parę (row/col, nr) '''
    if np.random.randint(0,2) == 1:
        return("rows", np.random.randint(0,nrow))
    else:
        return ("cols", np.random.randint(0,ncol))

def nonogram_inference(nrow, ncol, rows: List[int], cols: List[int], max_iter = 500):
    ''' Przeprowadza wnioskowanie o obrazku logicznym w następujący sposób:
    - do każdego z wierszy i kolumn przypisana jest lista wszystkich możliwych ustawień oraz flaga "do sprawdzenia". Wstępnie wszystkie są do sprawdzenia
    - w wybranym B.S.O. wierszu sprawdzamy czy któreś z pól z 2 we wszystkich ustawieniach ma 1 lub 0
    - jeśli tak, zmieniamy znak na planszy z 2 na 0 lub 1, a następnie usuwamy z listy przypisanej odpowiedniej kolumnie ustawienia sprzeczne z tym znakiem
    - zmieniamy flagę zmodyfikowanej kolumny na "do sprawdzenia"
    - powtarzamy, aż nie pozostanie nic do sprawdzenia
    ---------------------------------------------------------------------------
    '''
    lengths = {"rows": ncol, "cols": nrow}
    examine = {"rows": [True] * nrow, "cols": [True] * ncol}
    
    # TODO zamienić listy wewnątrz na tuple i zrobić z nich seta, żeby szybciej wyjmować elementy
    arrangements = {"rows": [possible_ones(ncol, row) for row in rows], "cols": [possible_ones(nrow, col) for col in cols]}
    board = np.full(shape = (nrow,ncol), fill_value = 2, dtype = np.uint8)

    for iter in range(max_iter):
        print(f'Iteracja {iter} ---------------------------------')
        print(f'examine[\'rows\']: {examine["rows"]}')
        print(f'examine[\'cols\']: {examine["cols"]}')
        if sum(examine["rows"]) == 0 and sum(examine["cols"]) == 0: 
            print('Nie zostalo nic do sprawdzenia')
            return board
        
        # Losowanie
        while True:
            what, ind = choose_one(nrow, ncol) # np. ("rows", 5)
            if examine[what][ind]: break # jeśli jest do sprawdzenia, nie trzeba dalej losować
            if len(arrangements[what][ind]) == 0:
                raise ValueError('Coś nie tak: puste arranements dla {what} {ind}') # debug
        
        all_ones = [True] * lengths[what]
        all_zeros = [True] * lengths[what]
        # Iteracja po wszystkich ustawieniach: jeśli któreś z nich nie ma jedynki, zmieniamy all_ones na False
        # (analogicznie dla zera); np. arrangements['rows'][0] lista wszystkich możliwych ustawień pierwszego wiersza
        for i in range(len(all_ones)):
            ones_broken = zeros_broken = False
            for arr in arrangements[what][ind]:
                if arr[i] == 0: 
                    all_ones[i] = False 
                    ones_broken = True
                else: 
                    all_zeros[i] = False
                    zeros_broken = True
                if zeros_broken and ones_broken: 
                    break # jeśli znaleźliśmy już że na jakimś miejscu nie ma wszędzie ani zer ani jedynek, nie ma sensu dalej sprawdzać
        
        # Wiemy już, gdzie są same zera i same jedynki, więc możemy ustawić te pola
        for x in range(len(all_ones)):
            if all_ones[x] and all_zeros[x]:
                raise ValueError(f"Coś nie tak: all_zeros: {all_zeros}, all_ones: {all_ones}") # debug

            # indeks w arrayu zal. czy to wiersz czy kolumna TODO zoptymalizować później
            i,j = (ind, x) if what == 'rows' else (x, ind)

            if all_ones[x]:
                board[i,j] = 1
                # po zmianie pola na planszy, trzeba jeszcze usunąć wszystkie ustawienia, które mają w tym miejscu 0
                # z zarówno wierszy jak i kolumn. Po usunięciu jakiegoś ustawienia trzeba oznaczyć ten wiersz/kolumnę jako do sprawdzenia
                for arr in arrangements["rows"][i]:
                    # spr. miejsce j w wierszu i
                    if arr[j] != 1:
                        arrangements["rows"][i].remove(arr)
                        examine["rows"][i] = True # TODO zoptymalizować, bo teraz to się robi wielokrotnie
                
                for arr in arrangements["cols"][j]:
                    # spr. miejsce i w kolumnie j
                    if arr[i] != 1:
                        arrangements["cols"][j].remove(arr)
                        examine["cols"][j] = True

            if all_zeros[x]:
                board[i,j] = 0
                for arr in arrangements["rows"][i]:
                    # spr. miejsce j w wierszu i
                    if arr[j] != 0:
                        arrangements["rows"][i].remove(arr)
                        examine["rows"][i] = True # TODO zoptymalizować, bo teraz to się robi wielokrotnie
                
                for arr in arrangements["cols"][j]:
                    # spr. miejsce i w kolumnie j
                    if arr[i] != 0:
                        arrangements["cols"][j].remove(arr)
                        examine["cols"][j] = True
            
            # można ustawić teraz ten wiersz / kolumnę jako sprawdzony
            # TODO przy losowaniu dodać sprawdzanie czy nie jest to sprawdzone
            examine[what][ind] = False
    
    return board

if __name__ == '__main__':
    spec = read_spec('zad_input.txt')
    result = nonogram_inference(*spec)
    draw(result)