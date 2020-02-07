import heapq
from math import inf
from src.graphs.graph_representations.edges import DirectedEdge
from src.graphs.graph_representations.graph_weighted import DigraphWeighted

class GraphShortestPath:
  """preprocesses a weighted digraph to find shortest paths from a source vertex to any other vertex in constant time"""
  def __init__(self, graph: DigraphWeighted, source):
    self.graph = graph
    self.source = source
    self.parent = [None for v in range(graph.v())]
    self.dist_to = [inf for v in range(graph.v())]
    self.dist_to[source] = 0
    self.heap = []
    self._dijkstras_shortest_path()

  def source_shortest_path_to(self, v):
    """returns iterable of path from source to v"""
    path = [v]
    parent = self.parent[v]
    while parent is not None:
      path.append(parent)
      parent = self.parent[parent]
    return list(reversed(path))

  def source_distance_to(self, v):
    """returns distance (total weight) from source to v"""
    return self.dist_to[v]

  def _relax(self, e: DirectedEdge):
    """relaxes edge from v to w if possible"""
    v, w = e.from_(), e.to()
    # TODO could skip alrady dealt-with verticwes here?
    if self.dist_to[w] > self.dist_to[v] + e.weight:
      self.parent[w] = v
      self.dist_to[w] = self.dist_to[v] + e.weight
      # TODO add decrease-key?
      heapq.heappush(self.heap, (self.dist_to[w], w))

  def _dijkstras_shortest_path(self):
    """implements https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm"""
    heapq.heappush(self.heap, (0, self.source))
    while self.heap:
      # TODO can I clean this up with lt/gt methods?
      _, v = heapq.heappop(self.heap)
      for edge in self.graph.adj(v):
        self._relax(edge)
        