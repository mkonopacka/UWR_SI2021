# AI 2021 P2 : To samo co w zadaniu 4, ale A* 
# ZALICZONE
from utils import *
from queue import PriorityQueue
from itertools import combinations
from graph import Graph
from tqdm import trange
from zad4 import get_initial_set, final_coords, final_set, generate_new_set

def map_distances(map: np.ndarray) -> dict:
    ''' Zamienia mape na graf i zwraca slownik dlugosci sciezek znalezionych przez BFS dla kazdej pary wspolrzednych na mapie '''
    map_graph = Graph()

    for row in range(h):
        for col in range(w):
            if map[row,col] != '#':
                map_graph.add_vertex((row, col))

    for pos in map_graph.get_vertices():
        for nbr in around(pos):
            if allowed_index(h,w,nbr) and map[nbr] != '#':
                map_graph.add_edge(pos, nbr)

    bfs_dist_dict = {}

    for pair in combinations(map_graph.get_vertices(), 2):
            path = map_graph.bfs_search(pair[0], pair[1])
            bfs_dist_dict[pair] = len(path)
    for coords in map_graph.get_vertices():
        bfs_dist_dict[(coords, coords)] = 0
    
    return bfs_dist_dict

def h(coords_set, goals):
    ''' Zwraca wartosc heurystyki dla zbioru wspolrzednych: dla każdego komandosa znajdujemy 
        odległość manhatańską do najbliższego celu i z tych odl. bierzemy maksimum'''
    minima = []
    for coords in coords_set:
        distances = [dist(coords, goal) for goal in goals]
        minima.append(min(distances))
    return max(minima)

def h2(coords_set, goals, dist_dict):
    ''' Tak jak wyzej, ale zamiast odleglosci manhatanskiej bierzemy prawdziwe odleglosci do celow ze slownika distances '''
    minima = []
    for coords in coords_set:
        distances = []
        for goal in goals:
            try:
                dist = dist_dict[(coords, goal)]
            except KeyError:
                dist = dist_dict[(goal,coords)] # któryś z nich powinien tam być
            finally:
                distances.append(dist)
        
        minima.append(min(distances))

    return max(minima)

if __name__ == '__main__':
    map = read_map('zad_input.txt')
    initial_set = get_initial_set(map)
    goals = []
    h, w = map.shape
    for row in range(1,h-1):
        for col in range(1,w-1):
            if final_coords((row,col), map):
                goals.append((row,col))
    
    distances = map_distances(map)
    
    queue = PriorityQueue()
    queue.put((h2(initial_set, goals, distances) + 0, 0, initial_set, "_INITIAL_STATE_", None))

    trace = {}

    for _ in trange(10000000):
        key, parent_cost, curr, prev, move = queue.get()
        if not curr in trace.keys(): 
            trace[curr] = (prev, move)
        else: continue
        if final_set(curr, map): break
        for move in ["U", "D", "L", "R"]:
            new_set = generate_new_set(curr, move, map)
            if not new_set in trace.keys():
                # increment cost by 1 and calculate new h value
                cost = parent_cost + 1
                queue.put((cost + h2(new_set, goals, distances), cost, new_set, curr, move))

    # backtrace path
    moves = []
    while True:
        prev, move = trace[curr]
        if prev == '_INITIAL_STATE_': break
        else: 
            curr = prev
            moves.append(move)

    with open('zad_output.txt', 'w') as f:
        for char in reversed(moves):
            f.write(char)
    
