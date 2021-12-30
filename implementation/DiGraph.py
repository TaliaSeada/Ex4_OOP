import random

from implementation.Node import Edge
from implementation.GraphInterface import GraphInterface
from implementation.Node import Node
from implementation.StraightLineFormula import  StraightLineFormula


class DiGraph(GraphInterface):

    def __init__(self):
        self._nodes = {}
        self._edges = []
        self.mc = 0

    def __repr__(self):
        return "Graph: |V|={},|E|={}".format(len(self._nodes), len(self._edges))

    # returns the graph
    def get_graph(self):
        return self

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        # if pos is given - use it
        if pos is not None:
            newNode = Node(node_id)
            newNode.setLocation(pos)
            # if the node does not exist - add it
            if node_id not in self._nodes.keys():
                self._nodes[node_id] = newNode
                self.mc += 1
                return True
            else:
                return False
        # if pos is not given, put random values to the node's pos
        else:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            z = 0.0
            pos = (x, y, z)
            newNode = Node(node_id)
            newNode.setLocation(pos)
            # if the node does not exist - add it
            if node_id not in self._nodes.keys():
                self._nodes[node_id] = newNode
                self.mc += 1
                return True
            else:
                return False

    # returns the dictionary of all in edges
    def all_in_edges_of_node(self, id1: int) -> dict:
        return self._nodes.get(id1).getEdgesToNode()

    # returns the dictionary of all out edges
    def all_out_edges_of_node(self, id1: int) -> dict:
        return self._nodes.get(id1).getEdgesFromNode()

    def remove_node(self, node_id: int) -> bool:
        try:
            # if the node does not exist - we cant remove it
            if node_id not in self._nodes:
                return False
            in_edges = self.all_in_edges_of_node(node_id)
            out_edges = self.all_out_edges_of_node(node_id)
            # remove all the edges that connected to the removed node
            for key in in_edges:
                self.remove_edge(key, node_id)
            for key in out_edges:
                self.remove_edge(key, node_id)
            # then remove the node
            del self._nodes[node_id]
            self.mc += 1
            return True
        except KeyError:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        # if the nodes exist
        if node_id1 in self._nodes.keys() and node_id2 in self._nodes.keys():
            i = 0
            # run over the edges
            while i < len(self._edges):
                edge = self._edges[i]
                # find the correct edge for the given nodes
                if edge.getSrcNode() == node_id1 and edge.getDestNode() == node_id2:
                    # remove the edge
                    self._edges.remove(edge)
                    # then remove it from the nodes edges lists
                    node1 = self._nodes[edge.getSrcNode()]
                    node1.removeEdge(edge)
                    node2 = self._nodes[edge.getDestNode()]
                    node2.removeEdge(edge)
                    self.mc += 1
                    return True
                i = i + 1
        else:
            return False

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        try:
            # # if the nodes exist
            if id1 in self._nodes.keys() and id2 in self._nodes.keys():
                # create the edge we would like to add
                formula = StraightLineFormula()
                formula.StraightLineFormula(self._nodes.get(id1).getLocation(), self._nodes.get(id2).getLocation())
                newEdge = Edge(id1, weight, id2, formula)
                # if the edge already exist - dont add it
                for edge in self._edges:
                    if edge.getSrcNode() == id1 and edge.getDestNode() == id2:
                        return False
                # else add the edge
                self._edges.append(newEdge)
                # then add it to the relevant nodes
                node1 = self._nodes[id1]
                node1.addEdge(newEdge)
                node2 = self._nodes[id2]
                node2.addEdge(newEdge)
                self.mc += 1
                return True
            else:
                return False
        except KeyError:
            return False

    # returns the dictionary of all the nodes
    def get_all_v(self) -> dict:
        return self._nodes

    # returns the Mode Counter
    def get_mc(self) -> int:
        return self.mc

    # returns the number of edges in the graph
    def e_size(self) -> int:
        return len(self._edges)

    # returns the number of nodes in the graph
    def v_size(self) -> int:
        return len(self._nodes)

    # this function reverses the graph by reverse its edges
    def reverse_graph(self, g: GraphInterface):
        rever = DiGraph()
        rever_v = g.get_all_v()
        for key in rever_v.keys():
            node = rever_v.get(key)
            rever_e_out = g.all_out_edges_of_node(node.getKey())
            rever_e_in = g.all_in_edges_of_node(node.getKey())
            # add all nodes
            rever.add_node(node.getKey(), node.getLocation())
            # add reversed edges
            for edge in rever_e_out:
                rever.add_edge(edge, key, rever_e_out.get(edge))
            for edge in rever_e_in:
                rever.add_edge(key, edge, rever_e_in.get(edge))
        return rever

    def get_edges(self):
        return self._edges
