import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph1 = nx.Graph()

    def buildGraph1(self, genre, date1, date2):
        self._graph1.clear()
        self._nodes = DAO.get_nodes_1(genre, date1, date2)
        self._idMapNodes = {}
        for node in self._nodes:
            self._idMapNodes[node.TrackId] = node
        self._edges = DAO.get_edges_1(genre, date1, date2, self._idMapNodes)
        self._graph1.add_nodes_from(self._nodes)
        for item in self._edges:
            self._graph1.add_edge(item[0], item[1], weight=item[2])

    def printGraph1(self):
        return f"Il grafo ha {len(self._graph1.nodes)} nodi e {len(self._graph1.edges)} archi."
