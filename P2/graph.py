from vertex import Vertex
from collections import deque

class Graph:
    def __init__(self):
        self.vert_list = {} # pairs "key : Vertex"

    def bfs_search(self, start_key, goal_key, max_iter = 100000000):
        ''' Return the shortest path between start and goal '''
        queue = deque()
        queue.append((start_key, "__INITIAL_STATE__"))
        visited = {}
        for i in range(max_iter):
            if i == max_iter-1: 
                print('Path not found.')
                return None
            curr, prev = queue.popleft()
            if not curr in visited: visited[curr] = prev
            else: continue
            if curr == goal_key: break
            vertex = self.get_vertex(curr)
            neighbours = [nbr for nbr in vertex.get_connections() if not nbr in visited]
            for nbr in neighbours: queue.append((nbr.key,curr))

        path = []
        path.append(goal_key)
        while True:
            prev = visited[path[-1]]
            if prev == '__INITIAL_STATE__': break
            else: path.append(prev)
        return list(reversed(path))

    def remove_vertex(self, key):
        try:    
            v = self.vert_list.pop(key)
            for w in self:
                if v in w.get_connections():
                    del w.connected_to[v]
        
        except KeyError:
            pass
    
    def add_vertex(self, key):
        new_vertex = Vertex(key)
        self.vert_list[key] = new_vertex

    def get_vertex(self, key):
        if key in self.vert_list:
            return self.vert_list[key]
        else:
            return None

    def add_edge(self, f, t, weight = 1):
        ''' Add new egde connecting vertex f to vertex t; f and t are keys '''
        if f not in self.vert_list:
            self.add_vertex(f)
        if t not in self.vert_list:
            self.add_vertex(t)
        self.vert_list[f].add_neighbour(self.vert_list[t], weight)

    def get_vertices(self):
        return self.vert_list.keys()

    def __contains__(self, key):
        return key in self.vert_list

    def __iter__(self):
        return iter(self.vert_list.values())


def graph_test():
    g = Graph()
    for i in range(6):
        g.add_vertex(i)

    g.add_edge(0, 1)
    g.add_edge(0, 5)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 0)
    g.add_edge(5, 4)
    g.add_edge(5, 2)

    for v in g:
        print(v)

    g.remove_vertex(4)
    for v in g:
        print(v)

    g.remove_vertex(4)
    g.remove_vertex(5)
    for v in g:
        print(v)

if __name__ == "__main__":
    graph_test()
