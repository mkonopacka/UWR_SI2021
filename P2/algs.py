from collections import deque, Hashable
from tqdm import trange

def backtrace_path1(final_state, visited, break_str = "_INITIAL_STATE_"):
    ''' Reconstruct path from initial state to final state (for BFS1)
        final_state: final state (Hashable)
        visited: dict of visited states {state : its parent}
        break_str: expression used to recognize initial state when found as state's parent 
    '''
    path = []
    path.append(final_state)
    while True:
        prev = visited[path[-1]]
        if prev == break_str: break
        else: path.append(prev)
    return list(reversed(path))

def BFS1(initial_state, state_is_final, generate_states, break_str = '_INITIAL_STATE_', 
max_iter = 1000000000, **kwargs):
    ''' Return path from initial state to final state found by Breadth First Search algorithm
        initial_state: initial state (Hashable)
        state_is_final: function that takes state as an argument and returns True if it is final and False otherwise
        generate_states: function that takes state as an argument and returns list of its children (hashable states)
        **kwargs: extra parameters used by state_is_final and generate_states
    '''
    # if not isinstance(initial_state, Hashable):
    #     raise TypeError('initial_state must be of a hashable type')
    # queue stores pairs of state and its parent
    queue = deque()
    queue.append((initial_state, "_INITIAL_STATE_"))
    # dict of visited states (state : parent)
    visited = {}
    for _ in range(max_iter):
            curr, prev = queue.popleft()
            if not curr in visited: visited[curr] = prev
            else: continue
            if state_is_final(curr, **kwargs): break
            neighbours = [state for state in generate_states(curr, **kwargs) if not state in visited]
            for state in neighbours: queue.append((state,curr))

    return backtrace_path1(curr, visited, break_str)

def BFS2(initial_state, state_is_final, change_state, moves, break_str = '_INITIAL_STATE_', 
max_iter = 1000000000, **kwargs):
    ''' BFS but returns moves instead of states
        change_state: function that given state and move returns new state (forbidden moves must not change state)
        moves: list of representations of possible moves in each state (e.g ["UP", "DOWN", "RIGHT", "LEFT"])'''
    if not isinstance(initial_state, Hashable): 
        raise TypeError('initial_state must be of a hashable type')
    # queue stores triples: state, parent, move from parent to state
    queue = deque()
    queue.append((initial_state, "_INITIAL_STATE_", None))
    # keep track of moves leading to goal dict {state: (parent, move)}
    trace = {}
    
    for _ in trange(max_iter):
        curr, prev, move = queue.popleft()
        if not curr in trace.keys(): 
            trace[curr] = (prev, move)
        else: continue
        if state_is_final(curr, **kwargs): break
        for move in moves:
            new_state = change_state(curr, move, **kwargs)
            if not new_state in trace.keys():
                queue.append((new_state,curr,move))

    # backtrace path (moves)
    moves = []
    while True:
        prev, move = trace[curr]
        if prev == break_str: break
        else: 
            curr = prev
            moves.append(move)
    return list(reversed(moves))
