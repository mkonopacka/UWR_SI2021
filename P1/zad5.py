# ZALICZONE
''' Obrazki logiczne c.d. 
    Input: #kolumn #wierszy \n kol1 \n kol2 ... \n wiersz1 ...
    Oznaczenia: # - pełne . -puste (pole) '''
from zad4 import opt_dist
import numpy as np


def solve(nrows, ncols, rows, cols, max_iter = 1000, board = None, p = 0.5):
    ''' Zwraca ulozony obrazek w postaci np.array zer i jedynek '''
    if board is not None: 
        board = board
    else: 
        board = np.random.randint(0, 2, (nrows, ncols))
    
    h,w = board.shape

    # listy opt_dist dla wierszy i kolumn, żeby nie musiały się mnóstwo razy liczyć
    row_distances = [opt_dist(row,rows[i]) for i,row in enumerate(board)]
    col_distances = [opt_dist(col,cols[i]) for i,col in enumerate(board.T)]

    # indeksy nieułożonych wierszy i kolumn
    bad_rows_ind = set([j for j in range(nrows) if row_distances[j] > 0])
    bad_cols_ind = set([i for i in range(ncols) if col_distances[i] > 0])

    iter = 0
    rand_init = 0

    while True:
        # print(iter)
        if iter > max_iter: 
            board = np.random.randint(0, 2, (nrows, ncols))
            row_distances = [opt_dist(row,rows[i]) for i,row in enumerate(board)]
            col_distances = [opt_dist(col,cols[i]) for i,col in enumerate(board.T)]
            bad_rows_ind = set([j for j in range(nrows) if row_distances[j] > 0])
            bad_cols_ind = set([i for i in range(ncols) if col_distances[i] > 0])
            iter = 0
            rand_init += 1
        
        # listy opt_dist dla wierszy i kolumn, żeby nie musiały się mnóstwo razy liczyć
        row_distances = [opt_dist(row,rows[i]) for i,row in enumerate(board)]
        col_distances = [opt_dist(col,cols[i]) for i,col in enumerate(board.T)]

        # indeksy nieułożonych wierszy i kolumn
        bad_rows_ind = set([j for j in range(nrows) if row_distances[j] > 0])
        bad_cols_ind = set([i for i in range(ncols) if col_distances[i] > 0])

        # print(bad_cols_ind, bad_rows_ind)
        if len(bad_cols_ind) == 0 and len(bad_rows_ind) == 0: 
            print(f'Obrazek ulozony po {rand_init} losowaniach w {iter} iteracji')
            return board
        else:
            # wybor złej kolumny
            if np.random.randint(0,2) == 0 and len(bad_cols_ind) != 0:
                # print(f'bad_cols: {bad_cols_ind}')
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
                _,i,j = triple
                board[i, j] ^=1
                row_distances[i] = opt_dist(board[i,:],rows[i])
                col_distances[j] = opt_dist(board[:,j], cols[j])
                # if row_distances[i] == 0: bad_rows_ind.discard(i)
                # if col_distances[j] == 0: bad_cols_ind.discard(j)
                # if row_distances[i] > 0: bad_rows_ind.add(i)
                # if row_distances[j] > 0: bad_rows_ind.add(j)

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
                _,i,j = triple
                board[i, j] ^=1
                row_distances[i] = opt_dist(board[i,:],rows[i])
                col_distances[j] = opt_dist(board[:,j], cols[j])
                # if row_distances[i] == 0: bad_rows_ind.discard(i)
                # if col_distances[j] == 0: bad_cols_ind.discard(j)
                # if row_distances[i] > 0: bad_rows_ind.add(i)
                # if row_distances[j] > 0: bad_rows_ind.add(j)
            
            iter += 1

def draw(board, file = None):
    ''' Rysuje obrazek, jesli podano to do pliku '''
    for i in range(len(board)):
        for j in range(len(board[i])):
            print('#' if board[j][i] == 1 else '.', end ='', file = file)
        print(file = file)
    print(file = file)

def try_change_bit(i,j, rows, cols, board, row_distances, col_distances):
    ''' Zwraca sume roznicy pomiedzy dopasowaniem wierszy i kolumn przed i po zamianie bitu i,j
        (Ujemna oznacza, ze polepszylismy dopasowanie, czyli opt_dist zmalalo)
        row_dists, col_dists - słowniki obliczonych wcześniej opt_dist dla wierszy i kolumn '''
    row_dist1 = row_distances[i] 
    col_dist1 = col_distances[j]
    board[i,j] ^= 1
    row_dist2 = opt_dist(board[i,:], rows[i])
    col_dist2 = opt_dist(board[:,j], cols[j])
    board[i,j] ^=1  
    d = col_dist2 - col_dist1 + row_dist2 - row_dist1
    return d

if __name__ == '__main__':
    with open('zad5_input.txt', "r") as f1:
        input = []
        for line in f1.read().splitlines():
            input = input + [p for p in line]
        ncols = int(input[0])
        nrows = int(input[2])
        cols = list(map(int, input[3: 3+ncols]))
        rows = list(map(int, input[3+ncols: ]))
        solved = solve(nrows, ncols, rows, cols)
        print('________________________________________________________________________________')
        print(solved)
        with open('zad5_output.txt', 'w') as f2:
            draw(solved, file = f2)
        