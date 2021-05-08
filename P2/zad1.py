# wynik: 
# TODO zoptymalizować + wybrać lepsze p, iter jeśli się da
# np. zmienić listy na stringi, zmienić pętle na list comprehension(?), uzależnić losowanie na nowo od tego jak daleko się jest
''' Obrazki logiczne pełna wersja (por. zad 5/P1)
    Input: nrows ncols \n [row1] \n [row2] ... [col1] \n [col2] ... '''
import numpy as np
from opt_dist import *

def try_change_bit(i,j, rows, cols, board, row_distances, col_distances):
    ''' Zwraca sume roznicy pomiedzy dopasowaniem wierszy i kolumn przed i po zamianie bitu i,j
        (Ujemna oznacza, ze polepszylismy dopasowanie, czyli opt_dist_multi zmalalo)
        row_dists, col_dists - słowniki obliczonych wcześniej opt_dist_multi dla wierszy i kolumn '''
    row_dist1 = row_distances[i] 
    col_dist1 = col_distances[j]
    board[i,j] ^= 1
    row_dist2 = opt_dist_multi(board[i,:], rows[i])
    col_dist2 = opt_dist_multi(board[:,j], cols[j])
    board[i,j] ^=1  
    d = col_dist2 - col_dist1 + row_dist2 - row_dist1
    return d

def solve(nrows, ncols, rows, cols, max_iter = None, board = None, p = 0.1):
    ''' Zwraca ulozony obrazek w postaci np.array zer i jedynek '''
    max_iter = max_iter if max_iter else ncols * nrows * 10
    if board is not None: 
        board = board
    else: 
        board = np.random.randint(0, 2, (nrows, ncols))
    
    h,w = board.shape

    # listy opt_dist_multi dla wierszy i kolumn
    row_distances = [opt_dist_multi(row,rows[i]) for i,row in enumerate(board)]
    col_distances = [opt_dist_multi(col,cols[i]) for i,col in enumerate(board.T)]

    # indeksy nieułożonych wierszy i kolumn
    bad_rows_ind = set([j for j in range(nrows) if row_distances[j] > 0])
    bad_cols_ind = set([i for i in range(ncols) if col_distances[i] > 0])

    iter = 0
    rand_init = 0

    while 1:
        if iter > max_iter: 
            board = np.random.randint(0, 2, (nrows, ncols))
            row_distances = [opt_dist_multi(row,rows[i]) for i,row in enumerate(board)]
            col_distances = [opt_dist_multi(col,cols[i]) for i,col in enumerate(board.T)]
            bad_rows_ind = set([j for j in range(nrows) if row_distances[j] > 0])
            bad_cols_ind = set([i for i in range(ncols) if col_distances[i] > 0])
            iter = 0
            rand_init += 1
            
        if len(bad_cols_ind) == 0 and len(bad_rows_ind) == 0: 
            print(f'Obrazek {nrows} x {ncols} ulozony po {rand_init} losowaniach w {iter} iteracji')
            return board
        else:
            # patrz: coś ok. linii 86
            triple = None
            
            # wybor złej kolumny
            if np.random.randint(0,2) == 0 and len(bad_cols_ind) != 0:
                j = np.random.choice(tuple(bad_cols_ind))
                d_lst = []
                for i in range(h):
                    d = try_change_bit(i,j,rows,cols,board, row_distances, col_distances)
                    d_lst.append((d,i,j))

                d_lst = sorted(d_lst)
                if np.random.rand() > p:
                    triple = d_lst[0]
                else:
                    randind = np.random.randint(1,len(d_lst))
                    triple = d_lst[randind]

            # wybor złego wiersza
            if np.random.randint(0,2) == 1 and len(bad_rows_ind) != 0:
                i = np.random.choice(tuple(bad_rows_ind))
                d_lst = []
                for j in range(w):
                    d = try_change_bit(i,j,rows, cols,board, row_distances, col_distances)
                    d_lst.append((d,i,j))
                
                d_lst = sorted(d_lst)
 
                if np.random.rand() > p:
                    triple = d_lst[0]
                else:
                    randind = np.random.randint(1,len(d_lst))
                    triple = d_lst[randind]
                
            # jeśli udało się znaleźć jakiś piksel, podmiana
            if triple is not None:
                _,i,j = triple
                board[i, j] ^=1
                row_distances[i] = opt_dist_multi(board[i,:],rows[i])
                col_distances[j] = opt_dist_multi(board[:,j], cols[j])
                if row_distances[i] == 0: bad_rows_ind.discard(i)
                if col_distances[j] == 0: bad_cols_ind.discard(j)
                if row_distances[i] > 0: bad_rows_ind.add(i)
                if col_distances[j] > 0: bad_cols_ind.add(j)
            
            iter += 1

def draw(board, file = None):
    ''' Rysuje obrazek, jesli podano to do pliku '''
    for i in range(len(board)):
        for j in range(len(board[i])):
            print('#' if board[i][j] == 1 else '.', end ='', file = file) # podmienione miejsca wzgl. listy 1 (tam jest złe wczytywanie)
        print(file = file)
    print(file = file)

if __name__ == '__main__':
    with open('zad_input.txt', "r") as f_in:
        print('________________________________________________________________________________')
        lines = f_in.read().splitlines()
        nrows,ncols = map(int, (lines[0]).split())
        rows = [list(map(int, seq.split())) for seq in lines[1: 1+nrows]]
        cols = [list(map(int, seq.split())) for seq in lines[1+nrows: ]]
        solved = solve(nrows, ncols, rows, cols, max_iter= 1000)
        draw(solved)
        with open('zad_output.txt', 'w') as f2:
            draw(solved, file = f2)