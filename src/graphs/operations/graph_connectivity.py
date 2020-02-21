from src.graphs.operations.graph_search import GraphSearch


class GraphConnectivity:
    """Preprocesses a graph into all its maximally-connected components
    in order to find unions in constant time
    """
    def __init__(self, graph):
        self.graph = graph
        self.vertex_count = self.graph.v()
        self.component_of = [None for v in range(self.vertex_count)]
        self.visited = [False for v in range(self.vertex_count)]
        self.component_count = 0
        self._preprocess()

    def connected(self, v: int, w: int) -> bool:
        """Returns True if v and w are connected, else False"""
        assert (self.component_of[v] is not None
                and self.component_of[w] is not None)
        return self.component_of[v] == self.component_of[w]

    def count(self) -> int:
        """Returns the number of distinct components"""
        return self.component_count

    def id(self, v) -> int:
        """Returns the connected component id for a given vertex"""
        return self.component_of[v]

    def _preprocess(self):
        # This would run faster with a class-specific dfs/bfs method
        # This would mean duplicate dfs/bfs code but one less for loop here
        for v in range(self.vertex_count):
            if self.visited[v] is False:
                self.component_count += 1
                GS = GraphSearch(self.graph, v)
                for vertex, visited in enumerate(GS.visited):
                    if visited:
                        self.visited[vertex] = True
                        self.component_of[vertex] = self.component_count


class GraphStrongConnectivity:
    """Implementing https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
    by preprocessing graph in linear time.
    Enables looking up strongly connected components in constant time.
    """
    def __init__(self, graph):
        self.graph = graph
        self.vertex_count = graph.v()
        self.component_count = 0
        self.visited_vertices = [False for v in range(graph.v())]
        self.component_id = [None for v in range(graph.v())]
        self.postorder = []
        self._preprocess()

    def __str__(self):
        strong_components = [[] for c in range(self.component_count)]
        for index, id in enumerate(self.component_id):
            strong_components[id].append(index)
        return f'Strong components: {strong_components}'

    def count(self) -> int:
        """Returns the number of distinct components"""
        return self.component_count

    def id(self, v) -> int:
        """Returns the connected component id for a given vertex"""
        return self.component_id[v]

    def strongly_connected(self, v, w) -> bool:
        """Returns True if v and w are strongly connected, else False"""
        return self.component_id[v] == self.component_id[w]

    def _dfs_with_component_marking(self, v: int):
        # Perform dfs and map vertices to components
        self.visited_vertices[v] = True
        self.component_id[v] = self.component_count
        for w in self.graph.adj(v):
            if not self.visited_vertices[w]:
                self._dfs_with_component_marking(w)
        return

    def _dfs_reverse_graph_with_postorder_tracking(self, v: int):
        # Perform dfs on reverse graph and track postorder of visited vertices
        self.visited_vertices[v] = True
        for w in self.graph.adj_reversed(v):
            if not self.visited_vertices[w]:
                self._dfs_reverse_graph_with_postorder_tracking(w)
        self.postorder.append(v)
        return

    def _reset_visited_vertices(self):
        self.visited_vertices = [False for v in range(self.vertex_count)]

    def _preprocess(self):
        for vertex in range(self.vertex_count):
            if not self.visited_vertices[vertex]:
                self._dfs_reverse_graph_with_postorder_tracking(vertex)
        self._reset_visited_vertices()

        # dfs on normal graph but iterate through vertices
        # in the order given by step 1
        for vertex in reversed(self.postorder):
            if not self.visited_vertices[vertex]:
                self._dfs_with_component_marking(vertex)
                self.component_count += 1
