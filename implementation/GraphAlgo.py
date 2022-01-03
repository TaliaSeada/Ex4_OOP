import math
from heapq import *
from typing import List
import json
import random

from implementation.DiGraph import DiGraph
from implementation.GraphAlgoInterface import GraphAlgoInterface
from implementation.GraphInterface import GraphInterface


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, copy=None):
        # default
        if not copy:
            self._graph = DiGraph()
            self._revGraph = DiGraph()
            # for GUI
            self.nodes = []
            self.balls = []
            self.lines_in = []
            self.lines_out = []
        # copy
        else:
            self._graph = copy
            self._revGraph = copy.reverse_graph(copy)
            # for GUI
            self.nodes = []
            self.balls = []
            self.lines_in = []
            self.lines_out = []

    # returns the graph
    def get_graph(self) -> GraphInterface:
        return self._graph

    # returns the reversed graph
    def get_revGraph(self) -> GraphInterface:
        return self._revGraph

    # this function returns the index of the minimum distance in a given list of distances
    def min_index(self, srcNode, dist_v, node_lst, passed):
        min = float('inf')
        index = 0
        for key in node_lst:
            if dist_v.get(key) < min and key != srcNode and key not in passed:
                index = key
                min = dist_v.get(key)
        return index

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        # Iterate over the given list and run the Dijkstra function on the first node.
        # After running once on a node, take the shortest path to a node (it's inside the list).
        # Then, run again, but now on the node we took from the last iteration.
        # The function stops when we passed all the nodes.
        new_lst = []
        for i in node_lst:
            if i not in new_lst:
                new_lst.append(i)

        dist = 0
        path = []

        passed = []
        v = new_lst[0]
        while len(passed) != len(new_lst) - 1:
            if v in new_lst:
                passed.append(v)
            # get all shortest path's to the node v
            dist_v, path_v = self.dijkstra(v)
            # then get the index of the shortest of them all
            min_ind = self.min_index(v, dist_v, new_lst, passed)
            # and take the path between the two nodes to the main path
            f, currPath = self.shortest_path(v, min_ind)
            for p in currPath:
                if len(path) == 0:
                    path.append(p)
                    continue
                elif path[-1] != p:
                    path.append(p)
            # finally increase the dist by the distance between the two nodes
            dist += dist_v.get(min_ind)
            v = min_ind

        return path, dist

    def bfs(self, nodeKey: int, g: DiGraph):
        D = {v: float('inf') for v in self._graph.get_all_v().keys()}
        D[nodeKey] = 0
        queue = []
        nodeDict = g.get_all_v()
        node = nodeDict.get(nodeKey)

        # Mark the source node as visited and enqueue it
        node.setTag(2)
        queue.append(nodeKey)
        v_group = g.get_all_v()
        while queue:
            # Dequeue a vertex from queue
            nodeKey = queue.pop(0)
            # print(nodeKey, end=" ")
            for i in g.all_out_edges_of_node(nodeKey).keys():
                if v_group.get(i).getTag() == 0:
                    queue.append(i)
                    v_group.get(i).setTag(2)
                    D[i] = D[nodeKey] + 1
        # reset tags
        for n in v_group:
            v_group.get(n).setTag(0)
        return max(D.values())

    def isConnected(self):
        # bfs from a node, reverse edges, again bfs from the same node
        # if we got integer smaller than infinity in both, it means the graph is strongly connected
        key = 0
        # get the node we want to check from
        for i in self._graph.get_all_v().keys():
            key = i
            break
        # run bfs on it
        bfs = self.bfs(key, self._graph)
        # if the result is infinity then the graph is not connected
        if bfs == float('inf'):
            return False
        # else reverse the graph and check from the same node
        bfs_rev = self.bfs(key, self._revGraph)
        # if the result is infinity then the graph is not connected
        if bfs_rev == float('inf'):
            return False
        # is the distance is not infinity then the graph is connected
        return True

    def centerPoint(self) -> (int, float):
        # if the graph is connected
        # if self.isConnected():
        minDist = float('inf')
        minIndex = -1
        # run the dijkstra algorithm then take the max value of the
        # minimum values (distances that returned from the dijkstra algorithm)
        for v in self._graph.get_all_v().keys():
            dist, path = self.dijkstra(v)
            if max(dist.values()) < minDist:
                minDist = max(dist.values())
                minIndex = int(v)
        # return the node and the distance
        return minIndex, minDist
        # if the graph is not connected we cant have a center
        #  else:
        #     return(None, float('inf'))

    def load_from_json(self, file_name: str) -> bool:
        # load files using the build in library json
        try:
            file = open(file_name)
            data = json.load(file)
            counter = 0
            # define nodes
            for i in data["Nodes"]:
                id = int(i['id'])
                # if pos is given
                if i.get('pos') is not None:
                    pos = i['pos']
                    xyz = pos.split(',')
                    for i in range(len(xyz)):
                        xyz[i] = float(xyz[i])
                    self._graph.add_node(id, xyz)
                    self._revGraph.add_node(id, xyz)
                # if pos is not given define random pos
                else:
                    x = random.randint(0, 9)
                    y = random.randint(0, 9)
                    z = 0.0
                    self._graph.add_node(id, (x, y, z))
                    self._revGraph.add_node(id, (x, y, z))
            # define edges
            for i in data["Edges"]:
                counter += 1
                src = int(i["src"])
                dest = int(i["dest"])
                weight = float(i["w"])
                self._graph.add_edge(src, dest, weight)
                self._revGraph.add_edge(dest, src, weight)
            file.close()
            return True
        # if file does not exist
        except Exception as e:
            print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        # save files using the build in library json
        try:
            nodes = []
            edges = []
            # create the dictionary for the saved file
            nodeDict = self._graph.get_all_v()
            # add the nodes
            for node in nodeDict:
                thisNode = nodeDict[node]
                location = thisNode.getLocation()
                x = location[0]
                y = location[1]
                z = location[2]
                id = node
                currNode = {"pos": (str(x) + "," + str(y) + "," + str(z)), "id": id}
                nodes.append(currNode)
                allOutEdges = self._graph.all_out_edges_of_node(id)
                # add the edges
                for edge in allOutEdges.keys():
                    src = id
                    dest = edge
                    weight = allOutEdges[edge]
                    edgeCurr = {"src": id, "w": weight, "dest": dest}
                    edges.append(edgeCurr)
            # combine
            all = {"Edges": edges, "Nodes": nodes}
            # write to the file
            with open(file_name, "w") as file:
                file.write(json.dumps(all, indent=4))
            file.close()
            return True
        # if save did not succeeded throw an exception
        except Exception as e:
            print(e)
            return False

    def dijkstra(self, src: int):
        # this function gets a source nodes and calculates the shortest path from it to every other
        # node on the graph, and returns the distances, and also the last node that we got from to
        # every other node

        Distances = {}
        lastPath = {}
        # define all distances to be infinity and all nodes in path to be None
        for v in self._graph.get_all_v():
            Distances[v] = float('inf')
            lastPath[v] = None
        # the distance between node to itself is 0, so add the first node's distance
        Distances[src] = 0
        h = []
        all_v = self._graph.get_all_v()
        # then add the node to the heap
        heappush(h, (Distances[src], src))
        # run over the nodes and get the shortest path by comparing the weights of the edges
        # update if there is shorter path, and note every node we visit as visited
        while h:
            currNode = heappop(h)[1]
            all_v.get(currNode).setTag(2)
            outEdges = self._graph.all_out_edges_of_node(int(currNode))
            for edge in outEdges.keys():
                if all_v.get(edge).getTag() != 2:
                    currDist = Distances.get(edge)
                    newDist = Distances.get(currNode) + outEdges.get(edge)
                    if newDist < currDist:
                        heappush(h, (newDist, edge))
                        Distances[edge] = newDist
                        lastPath[edge] = currNode
        # reset the tags of the nodes
        for v in all_v:
            all_v.get(v).setTag(0)
        # return the shortest distance and the path of it
        return Distances, lastPath

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        # if the nodes exist in the graph
        if self._graph.get_all_v().__contains__(id1) and self._graph.get_all_v().__contains__(id2):
            p = []
            # use dijkstra
            dist, path = self.dijkstra(id1)
            # if node1 is not connected to node2 the shortest path would be infinity
            if dist[id2] == float('inf'):
                return float('inf'), p
            # else find the path between the two nodes
            id = id2
            p.append(id)
            # run over the path from one node to the other and add the nodes its go through
            while int(id) != id1:
                p.append(int(path[id]))
                id = path[id]
            # reverse the result and return it
            p.reverse()
            return dist[id2], p
        # if nodes does not exist return infinity and empty path
        return float('inf'), []

    # # use the plotGraph we build to plot the graph
    # def plot_graph(self) -> None:
    #     plot(self)
