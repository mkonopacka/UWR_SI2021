# ZALICZONE
''' Zadanie 1 (P1) 
1. stan: (krotka) kolor gracza na ruchu (1 = białe 0 = czarne) + współrzędne x,y białego króla, czarnego króla, wieży (Wx, Wy, Bx, By, Rx, Ry)
2. zbiór akcji: lista możliwych ruchów, czyli stanów do których mozna bezposrednio przejsc
3. model przejścia: przejscie ze stanu do stanu
4. stan końcowy: checkmate == True
5. liczenie kosztu: +1 z kazdym przejsciem
'''
from itertools import product
from collections import deque

def possible_moves(player, Wx, Wy, Bx, By, Rx, Ry, optimal = True):
    ''' Zwraca wszystkie stany do jakich mozna przejsc w tym momencie; 
        optimal = False odrzuca dodatkowo możliwe, ale bezsensowne ruchy '''
    states = []
    if player == 0:
        for nBx, nBy in product([Bx+1, Bx, Bx-1],[By+1, By, By-1]):
            # wykluczamy: stanie w miejscu
            if nBx == Bx and nBy == By: continue
            # yjscie poza krawedz szachownicy
            if not on_board(nBx, nBy): continue
            # stykajace sie krole
            if kings_collide(Wx, Wy, nBx, nBy): continue
            # miejsca gdzie krol bylby szachowany 
            # TODO TU JEST BŁĄÐ
            if check(Wx, Wy, nBx, nBy, Rx, Ry): continue
            
            # dodatkowo jesli szukamy optymalnych ruchów wykluczamy:
            if optimal:
                # zbicie krolem wiezy
                if nBx == Rx and nBy == Ry: continue 
                # nie cofanie sie wglab szachownicy jesli to mozliwe TODO

            # pozostale ruchy akceptujemy jako przejscie do nowego stanu (na ruchu beda biale)
            states.append((1,Wx,Wy,nBx,nBy,Rx,Ry))
    
    elif player == 1:
        # RUCH KRÓLEM
        for nWx, nWy in product([Wx+1, Wx, Wx-1],[Wy+1, Wy, Wy-1]):
            if nWx == Wx and nWy == Wy: continue
            if not on_board(nWx, nWy): continue
            if kings_collide(nWx, nWy, Bx, By): continue
            if nWx == Rx and nWy == Ry: continue
            if optimal:
                # nie cofamy sie krolem od czarnego krola
                if king_dist(nWx, Bx, nWy, By) > king_dist(Wx, Bx, Wy, By): continue
                
            states.append((0,nWx,nWy,Bx,By,Rx,Ry))
        
        # RUCH WIEŻĄ W POZIOMIE
        for nRx in range(8):
            # Zabraniamy przeskoczyc nad białym królem (nie moze stac pomiedzy stara a nowa pozycja wiezy) lub na niego najechac. 
            if nRx == Rx: continue
            if Ry == Wy and between(Rx, Wx, nRx): continue
            if optimal:
                pass # TODO?
            # Pozostale ruchy akceptujemy.
            states.append((0,Wx,Wy,Bx,By,nRx,Ry))
        
        # RUCH WIEŻĄ W PIONIE
        for nRy in range(8):
            if Rx == Wx and between(Ry, Wy, nRy): continue
            if nRy == Ry: continue
            if optimal:
                pass # TODO?
            states.append((0,Wx,Wy,Bx,By,Rx,nRy))
    return states

def king_dist(x1, x2, y1, y2):
    ''' Zwraca odleglosc pól liczona w ruchach krola '''
    return max(abs(x1 - x2), abs(y1 - y2))

def on_board(x,y):
    ''' True if x,y are between 0 and 7'''
    return between(0,x,7) and between(0,y,7)

def kings_collide(Wx, Wy, Bx, By):
    '''Zwraca prawde jesli krole stykaja sie (co jest niedozwolone)'''
    if  king_dist(Wx,Bx,Wy,By) <= 1: return True
    return False

def between(x,z,y):
    '''Zwraca prawde jesli z jest pomiedzy x a y (wlacznie)'''
    return (x <= z and z <= y) or (x >= z and z >= y)

def check(Wx, Wy, Bx, By, Rx, Ry):
    '''Zwraca prawde jesli czarny krol jest szachowany z uwzglednieniem przesloniecia bialym krolem'''
    if Rx == Bx and Ry == By: return False # zabezpieczenie przed błędem, że król zbił wieżę, a jest "szachowany"
    if Rx == Bx and not between(Bx, Wx, Rx): return True
    if Ry == By and not between(By, Wy, Ry): return True
    else: return False

def checkmate(player, Wx, Wy, Bx, By, Rx, Ry):
    '''Zwraca prawde jesli na szachownicy stoi mat'''
    if len(possible_moves(player, Wx, Wy, Bx, By, Rx, Ry, optimal = False)) == 0 and check(Wx, Wy, Bx, By, Rx, Ry):
        return True
    return False

def simple_board(player, Wx, Wy, Bx, By, Rx, Ry):
    '''Printuje prosta reprezentacje szachownicy, gdzie W - biały król, B - czarny król, R - biała wieża'''
    # TODO pewnie da sie troche to przyspieszyc zeby za kazdym razem nie bylo tego tworzenia
    grid = [f"| "*8 for row in range(8)]
    for row in range(8):
        grid[7-row] = f"{row+1} " + grid[7-row]
    grid.append('   A B C D E F G H')
    for y in range(3,len(grid[1]), 2):
        for x in range(8):
            # Wstawianie czarnych pól (musi byc przed wstawianiem figur)
            if ((y-1)/2 + x)%2 == 0:
                grid[x] = grid[x][:y]+ "#" + grid[x][y+1:] 
            
            # Wstawianie figur (najpierw przeliczam współrzędne gridowe na szachownice)
            xS = 7-x
            yS = (y-1)/2 - 1
            if xS == Wx and yS == Wy:
                grid[x] = grid[x][:y]+ "W" + grid[x][y+1:] # Tutaj podstawianie innego znaku w srodku stringa
            elif xS == Bx and yS == By:
                grid[x] = grid[x][:y]+ "B" + grid[x][y+1:] 
            elif xS == Rx and yS == Ry:
                grid[x] = grid[x][:y]+ "R" + grid[x][y+1:]

    print(*grid, sep = '|\n')
    print(f'Gracz: {player}')

def let_to_int(a):
    ''' Zamienia nazwę kolumny na szachownicy na odpowiadający jej int od 0 do 7'''
    return ord(a) - 97

def get_state(line):
    '''Bierze stringa line i zwraca ruch (1/0 = białe/czarne) i pozycje figur.
       UWAGA: kolumna 1 na szachownicy ma odpowiadać kolumnie 0 w programie.'''
    parts = line.split()
    player = 1 if parts[0] == 'white' else 0
    Wx = int(parts[1][1]) - 1
    Wy = let_to_int(parts[1][0])
    Bx = int(parts[3][1]) - 1
    By = let_to_int(parts[3][0])
    Rx = int(parts[2][1]) - 1
    Ry = let_to_int(parts[2][0])
    return player, Wx, Wy, Bx, By, Rx, Ry
 
def backtrace_path(last_move, visited):
    ''' Tworzy liste ruchow prowadzacych do mata na podstawie slownika visited i ostatniego ruchu '''
    path = []
    path.append(last_move)
    while True:
        prev = visited[path[-1]]
        if prev == 0: break
        else: path.append(prev)
    return list(reversed(path))

def print_path(path):
    n_moves = len(path) - 1
    for i,state in enumerate(path):
            print(f'Krok {i}/{n_moves}:')
            simple_board(*state)

def zadanie(debug = False):
    with open('zad1_input.txt', 'r') as file_in:
        line = file_in.readlines()[0]

    with open('zad1_output.txt', 'w') as file_out:
        gracz, Wx, Wy, Bx, By, Rx, Ry = get_state(line)
        queue = deque()
        # W kolejce przechowujemy pary stan, poprzednik i poprzednikiem startu jest 0
        # W ten sposob latwo przenosic je pozniej do odwiedzonych wraz z poprzednikami w celu odtworzenia znalezionej sciezki
        queue.append(((gracz, Wx, Wy, Bx, By, Rx, Ry), 0))
        visited = {}

        for iter in range(100000000):
            # 1.Zdejmij z kolejki parę (stan, poprzednik) i umieść go w odwiedzonych, jeśli go tam nie ma
            curr, prev = queue.popleft()
            if not curr in visited: visited[curr] = prev
            else: continue
            # 2.Sprawdź czy stan jest końcowy i jeśli tak, zakończ
            if checkmate(*curr): break
            
            # 3. Jeśli stan nie był końcowy, wygeneruj stany do których można z niego przejść i nie były jeszcze odwiedzone
            moves = [move for move in possible_moves(*curr) if not move in visited]
            
            # 4. Dla każdego stanu, którego jeszcze nie odwiedzaliśmy, dodaj go do kolejki z curr jako poprzednikiem
            for move in moves: queue.append((move,curr))

        # Rekonstrukcja sciezki prowadzacej do mata
        path = backtrace_path(curr, visited)
        n_moves = str(len(path)-1)
        file_out.write(n_moves)
        if debug: print_path(path)

zadanie(debug = True)


