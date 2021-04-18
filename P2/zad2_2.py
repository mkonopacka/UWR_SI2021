from utils import find_first, get_goals, read_map
from collections import deque
from tqdm import trange

class Board:

    moves_dict = {
        "U": (-1,0),
        "D": (1,0),
        "L": (0,-1),
        "R": (0,1)
    }

    class CannotMoveBoxError(Exception):
        pass

    def __init__(self, map, **kwargs):
        if map is not None:
            self.map = map
            self.height, self.width = map.shape
            self.goals = frozenset(get_goals(map, ['G', '*']))
            self.walls = frozenset(get_goals(map, ['#']))
            self.boxes = set(get_goals(map, ['B', '*']))
            self.K_row, self.K_col = find_first(map, ['K', '+'])
        else:
            self.height = kwargs['h']
            self.width = kwargs['w']
            self.goals = kwargs['goals']
            self.walls = kwargs['walls']
            self.boxes = kwargs['boxes']
            self.K_row = kwargs['K_row']
            self.K_col = kwargs['K_col']

    def copy(self):
        return Board(None, h = self.height, w = self.width, goals = self.goals,
            walls = self.walls,boxes = self.boxes,K_row = self.K_row,K_col = self.K_col)

    def solved(self):
        return self.goals == self.boxes

    # dodać tablice
    # dodać martwe stany (rogi, ściany bez goals)
    def __hash__(self):
        # zmienić na tostr hash map
        return hash((self.K_row, self.K_col, tuple(self.boxes))) 

    def square_is_empty(self, pos):
        return not (pos in self.boxes or pos in self.walls)

    def try_move_box(self, pos1,  pos2):
        if self.square_is_empty(pos2):
            self.boxes.remove(pos1)
            self.boxes.add(pos2)
        else:
            raise Board.CannotMoveBoxError

    def try_move_keeper(self, d_row, d_col):
        new_pos = (self.K_row + d_row, self.K_col + d_col)
        if self.square_is_empty(new_pos):
            self.Kx, self.Ky = new_pos
        elif new_pos in self.boxes:
            new_pos_box = (new_pos[0] + d_row, new_pos[1] + d_col)
            try:
                self.try_move_box(new_pos, new_pos_box)
            except Board.CannotMoveBoxError:
                pass
            else:
                self.Kx, self.Ky = new_pos

    def make_move(self, move):
        d_row, d_col = Board.moves_dict[move]
        self.try_move_keeper(d_row, d_col)

board = Board(read_map('zad_input.txt'))

# BFS
queue = deque()
queue.append((board.copy(), "_INITIAL_STATE_", None))
trace = {}

for _ in trange(100000000):
    curr, prev, move = queue.popleft()
    if not curr in trace.keys(): 
        trace[curr] = (prev, move)
    else: continue
    if curr.solved(): break
    for move in ["U", "L", "D", "R"]:
        new = curr.copy()
        new.make_move(move)
        if not new in trace.keys():
            queue.append((new,curr,move))

moves = []
while True:
    prev, move = trace[curr]
    if prev == '__INITIAL_STATE_': break
    else: 
        curr = prev
        moves.append(move)

with open('zad_output.txt', 'w') as f:
    for char in reversed(moves):
        f.write(char)