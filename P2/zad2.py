# DO ZROBIENIA
''' AI 2021 P2 Sokoban 
    . oznacza puste pole, 
    W ścianę, 
    K magazyniera, 
    B skrzynkę, 
    G pole docelowe, 
    * skrzynkę na polu docelowym, 
    + magazyniera na polu docelowym 
    Stan: mapa
    Stan końcowy: na wszyskich polach docelowych stoją skrzynki (*)'''
import numpy as np
from utils import read_map, get_goals

moves_dict = {
    "U": (-1,0),
    "D": (1,0),
    "L": (0,-1),
    "R": (0,1)
}

map = read_map('zad_input.txt')
goals = get_goals(map, ['*', 'G'])
K_pos = get_goals(map, ['K', '+'])[0]
K_char = map[K_pos]

def level_solved(map):
    return all([map(coords) in ['*', 'G'] for coords in goals])

def make_move(map, move):
    global K_pos
    global K_char
    update = moves_dict[move]
    new_K = (K_pos(0) + update(0), K_pos(1) + update(1))
    
    if map[new_K] == 'W': 
        pass
    
    elif map[new_K] in ['B', '*']:
        new_B = (new_K(0) + update(0), new_K(1) + update(1))
        # mozna wejsc na skrzynke tylko jesli po przesunieciu trafia na wolne pole
        # wtedy zmieniaja sie wartosci trzech pol: starego magazyniera K_pos, nowego magazyniera new_K i nowej skrzynki new_B
        if map[new_B] in ['.', 'G']:
            # postaw na nowym polu skrzynki skrzynke
            map[new_B] = 'B' if map[new_B] == '.' else '*'
            # postaw na nowym polu magazyniera magazyniera
            K_char = 'K' if map[new_K] == 'B' else '+'
            map[new_K] = K_char
            # usun ze starego pola magazyniera i zaktualizuj jego wspolrzedne
            map[K_pos] = 'G' if map[K_pos] == '+' else '.'
            K_pos = new_K
        else: 
            # jesli nie da sie przesunac skrzynki, nic sie nie dzieje
            pass

    elif map[new_K] == ['G', '.']:
        # jesli trafia na puste pole, zmieniaja sie wartosci dwoch pol
        # przesun na nowe pole
        K_char = '+' if map[new_K] == 'G' else 'K'
        map[new_K] = K_char
        # usun ze starego pola
        map[K_pos] = 'G' if map[K_pos] == '+' else '.'
        K_pos = new_K

# BFS
# remember moves with their depths (#ancestors)
moves = []