class Vertex:
    def __init__(self, key):
        self.key = key
        self.connected_to = {} # dict containing all neighbours as pairs "Vertex : weight"
        
    def get_key(self):
        return self.key

    def add_neighbour(self, nbr, weight=1):
        self.connected_to[nbr] = weight

    def get_connections(self):
        return self.connected_to.keys() 

    def get_weight(self, nbr):
        return self.connected_to[nbr] 

    def __str__(self):
        return "{} connected to: {}".format(self.key, [x.key for x in self.connected_to])
