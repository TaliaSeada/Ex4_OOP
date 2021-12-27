package code;

import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

import api.DirectedWeightedGraph;
import api.DirectedWeightedGraphAlgorithms;
import api.EdgeData;
import api.NodeData;
import com.google.gson.*;
import com.google.gson.internal.LinkedTreeMap;

/**
 * this class implements the functions of the DirectedWeightedGraphAlgorithms interface
 */
public class GraphAlgorithms implements DirectedWeightedGraphAlgorithms {
    private Graph graph;

    @Override
    public void init(DirectedWeightedGraph g) {
        this.graph = (Graph) g;
    }

    @Override
    public DirectedWeightedGraph getGraph() {
        return this.graph;
    }

    @Override
    public DirectedWeightedGraph copy() {
        return new Graph(this.graph);
    }

    @Override
    public boolean isConnected() {
        /*
            bfs from a node, reverse edges, again bfs from the same node
            if we got integer smaller than infinity in both, it means the graph is strongly connected
         */
        int key = 0;
        for(Integer i : this.graph.getNodes().keySet()) {
            key = i;
            break;
        }
        int bfs = bfs(key,this.graph);
        if (bfs == Integer.MAX_VALUE){
            return false;
        }
        int bfs_reverse = bfs(key,createOppositeGraph());
        return bfs_reverse != Integer.MAX_VALUE;
    }

    @Override
    public double shortestPathDist(int src, int dest) {
        ArrayList<HashMap> result = dijkstra(src);
        HashMap<Integer, Double> dists = result.get(0);
        if(dists.get(dest) == Double.MAX_VALUE){
            System.out.println("no Path");
            return -1;
        }
        return dists.get(dest);
    }

    @Override
    public List<NodeData> shortestPath(int src, int dest) {
        List<NodeData> path = new ArrayList<>();
        HashMap<Integer, Node> lastPath = dijkstra(src).get(1);
        if(shortestPathDist(src,dest) == -1)
        {
            System.out.println("no Path!");
            return null;
        }
        int firstInPath = lastPath.get(dest).getKey();
        path.add(this.graph.getNode(dest));
        path.add(lastPath.get(dest));
        while (firstInPath != src) {
            path.add(lastPath.get(firstInPath));
            firstInPath = lastPath.get(firstInPath).getKey();
        }
        List<NodeData> pathReversed = new ArrayList<>();
        for (int i = (path.size()); i > 0; i--) {
            pathReversed.add(path.get(i - 1));
        }
        return pathReversed;
    }

    @Override
    public NodeData center() {
        /*
            iterate over the nodes of the graph and run the Dijkstra function on each one of them.
            then, from each hashMap of distances of every node we got, we need to take the longest path.
            then take the minimum longest path of all the nodes.
         */
        // if the graph is not connected we can't get a center.
        HashMap<Integer, Double> maxDistances = new HashMap<>();
        Iterator<NodeData> nodeIter = this.graph.nodeIter();
        while (nodeIter.hasNext()) {
            NodeData next = nodeIter.next();
            HashMap<Integer, Double> distances = dijkstra(next.getKey()).get(0);
            maxDistances.put(next.getKey(), getMaxValue(distances));
        }
        return this.graph.getNode(getMinValueIndex(maxDistances));
    }

    // this function returns the index of the minimum distance
    private int getMinValueIndex(HashMap<Integer, Double> dist) {
        int index = 0;
        double minValue = Double.MAX_VALUE;
        for (Integer key : dist.keySet()) {
            if (minValue > dist.get(key)) {
                index = key;
                minValue = dist.get(key);
            }
        }
        return index;
    }
    // this function returns the maximum distance value
    private Double getMaxValue(HashMap<Integer, Double> dist) {
        double max = Double.MIN_VALUE;
        for (Integer key : dist.keySet()) {
            if (dist.get(key) > max) {
                max = dist.get(key);
            }
        }
        return max;
    }

    @Override
    public List<NodeData> tsp(List<NodeData> cities) {
        /*
            Iterate over the given list and run the Dijkstra function on the first node.
            After running once on a node, take the shortest path to a node (it's inside the list).
            Then, run again, but now on the node we took from the last iteration.
            The function stops when we passed all the nodes.
         */
        ArrayList<ArrayList<NodeData>> eachPath = new ArrayList<>();
        ArrayList<Integer> cities_keys = new ArrayList<>();
        for (NodeData city : cities) {
            if(city != null)
            {
                cities_keys.add(city.getKey());
            }
        }
        ArrayList<Integer> passed = new ArrayList<>();

        ArrayList<HashMap> result = dijkstra(cities.get(0).getKey());
        HashMap<Integer, Double> dist = result.get(0);
        HashMap<Integer, Node> path = result.get(1);
        passed.add(cities.get(0).getKey());

        ArrayList<NodeData> currPath = new ArrayList<>();
        for(int i = 0; i < cities.size();i++)
        {
            if(dist.get(cities.get(i).getKey()) == Double.MAX_VALUE)
            {
                System.out.println("no possible path");
                return null;
            }
        }
        int dest = getMinPath(dist, passed, cities_keys);
        int firstInPath = path.get(dest).getKey();
        currPath.add(0, this.graph.getNode(dest));
        currPath.add(0, path.get(dest));
        while (firstInPath != cities.get(0).getKey()) {
            currPath.add(0, path.get(firstInPath));
            firstInPath = path.get(firstInPath).getKey();
        }
        eachPath.add(currPath);


        while(passed.size() != cities.size() -1){
            int prevDest = dest;
            result = dijkstra(dest);
            dist = result.get(0);
            for(int i = 0; i < cities.size();i++)
            {
                if(dist.get(cities.get(i).getKey()) == Double.MAX_VALUE)
                {
                    System.out.println("no possible path");
                    return null;
                }
            }
            path = result.get(1);
            passed.add(dest);

            currPath = new ArrayList<>();
            dest = getMinPath(dist, passed, cities_keys);
            firstInPath = path.get(dest).getKey();
            currPath.add( this.graph.getNode(dest));
            currPath.add( path.get(dest));
            while (firstInPath != prevDest) {
                currPath.add( path.get(firstInPath));
                firstInPath = path.get(firstInPath).getKey();
            }
            eachPath.add(currPath);
        }
        List<NodeData> correctPath = new ArrayList<>();
        for(int i =0; i < eachPath.size();i++) {
            if(i == 0) {
                correctPath.addAll(eachPath.get(i));
            }
            else{
                ArrayList<NodeData> pathReversed = new ArrayList<>();
                for(int j = eachPath.get(i).size()-1; j >= 0; j--){
                    pathReversed.add(eachPath.get(i).get(j));
                }
                correctPath.addAll(pathReversed);
            }
        }
        ArrayList<NodeData> finalList = new ArrayList<>();
        for(int i =0; i < correctPath.size();i++) {
            if(i < correctPath.size()-1 && correctPath.get(i).getKey() == correctPath.get(i+1).getKey()){
                continue;
            }
            finalList.add(correctPath.get(i));
        }

        return finalList;
    }
    // this function returns the minimum distance
    private int getMinPath(HashMap<Integer, Double> dist, ArrayList<Integer> visited, ArrayList<Integer> q) {
        double min = Double.MAX_VALUE;
        int res = 0;
        for (Integer key : q) {
            if(!visited.contains(key)){
                if (dist.get(key) < min) {
                    min = dist.get(key);
                    res = key;
                }
            }

        }
        return res;
    }

    @Override
    public boolean save(String file) {
        /*
            for this function we've created a new classes to convert the nodes and edges to the format of the json file
            then we used the gson to convert the java file we have into json files
         */
        try {
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            FileWriter writer =  new FileWriter(file);
            HashMap<String, ArrayList<?>> toWrite = new HashMap<>();
            ArrayList<nodeToJson> nodes = new ArrayList<>();
            ArrayList<edgeToJson> edges = new ArrayList<>();
            for (Integer key : this.graph.getNodes().keySet()) {
                NodeData CurrNode = this.graph.getNodes().get(key);
                nodes.add(new nodeToJson(CurrNode));
            }
            toWrite.put("Nodes", nodes);

            for (int i = 0; i < this.graph.getAllEdges().size(); i++) {
                edges.add(new edgeToJson(this.graph.getAllEdges().get(i)));
            }
            toWrite.put("Edges", edges);

            gson.toJson(toWrite,writer);
            writer.flush(); //flush data to file
            writer.close(); //close write
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    @Override
    public boolean load(String file) {
        try {
            Gson gson = new Gson();
            Reader reader = Files.newBufferedReader(Paths.get(file));
            List<?> edges = null; // ? - we don't know the type yet
            List<?> nodes = null;
            Map<?, ?> map = gson.fromJson(reader, Map.class);
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                if (entry.getKey().equals("Edges")) {
                    edges = (List<?>) entry.getValue();
                } else {
                    nodes = (List<?>) entry.getValue();
                }

            }

            assert edges != null;
            ArrayList<Node> nodeArrayList = new ArrayList<>();
            ArrayList<Edge> edgeArrayList = new ArrayList<>();
            for (Object edge : edges) {
                edgeArrayList.add(new Edge((LinkedTreeMap<?, ?>) edge));
            }
            assert nodes != null;
            for (Object node : nodes) {
                nodeArrayList.add(new Node((LinkedTreeMap<?, ?>) node));
            }
            Graph graph = new Graph(edgeArrayList, nodeArrayList, file.split("\\.")[0]);
            this.init(graph);

            reader.close();
            return true;
        } catch (Exception e) {
            return false;
        }
    }


    //this function gets a source nodes and calculates the shortest path from it to every other
    //node on the graph, and returns the distances, and also the last node that we got from to
    // every other node
    public ArrayList<HashMap> dijkstra(int sourceNode){
        ArrayList<HashMap> result = new ArrayList<>();
        HashMap<Integer,Double> minDists = new HashMap<>();
        HashMap<Integer,NodeData> lastPath = new HashMap<>();

        int maxKey = -1;
        for(Integer key:this.graph.getNodes().keySet())
        {
            if(key > maxKey){
                maxKey = key;
            }
        }
        maxKey++;

        pair [] heapNodes = new pair[maxKey];
        for (Integer i: this.graph.getNodes().keySet()) {
            if(i == sourceNode){
                minDists.put(sourceNode,0.0);
            }
            else {
                minDists.put(i,Double.MAX_VALUE);
            }
            lastPath.put(i,null);

        }

        for(int i =0; i < maxKey;i++)
        {
            heapNodes[i] = new pair();
            heapNodes[i].node = i;
            heapNodes[i].dist = Double.MAX_VALUE;
        }

        heapNodes[sourceNode].dist = 0;

        minHeap MinHeap = new minHeap(maxKey);
        for (int i = 0; i < maxKey ; i++) {
            MinHeap.insert(heapNodes[i]);
        }
        int counter = 0;
        while(counter != this.graph.getNodes().size()){
            pair extractedNode = MinHeap.extractMin();
            counter++;
            int curr = extractedNode.node;
            Iterator<EdgeData> edges = this.graph.edgeIter(curr);
            if(edges != null)
            {
                while(edges.hasNext()){
                    EdgeData edge = edges.next();
                    int dest = edge.getDest();
                    double newDist = heapNodes[curr].dist + edge.getWeight();
                    if(heapNodes[dest].dist > newDist){
                        decreaseKey(MinHeap, newDist, dest);
                        heapNodes[dest].dist = newDist;
                        minDists.put(dest,newDist);
                        lastPath.put(dest,this.graph.getNode(curr));
                    }
                }
            }

        }
        result.add(minDists);
        result.add(lastPath);
        return result;
    }

    private void decreaseKey(minHeap MinHeap, double newKey, int vertex){
        int index = MinHeap.indexes[vertex];
        pair node = MinHeap.mH[index];
        node.dist = newKey;
        MinHeap.bubbleUp(index);
    }


    public int bfs(int nodeKey,Graph graph) {
        /*
            for bfs algorithm, we will change the tags of the graphs
            0 for Undiscovered nodes "white"
            1 for discovered but not finished "grey"
            2 for finished nodes "black"
         */
        HashMap<Integer,Integer> distances = new HashMap<>();
        HashMap<Integer, EdgeData> lastEdge = new HashMap<>();
        //lastEdge.get(i) represents the last edge in the path from node i to the node we do bfs on
        for (Integer key:this.graph.getNodes().keySet()){
            distances.put(key,Integer.MAX_VALUE);
            lastEdge.put(key,null);
        }
        // mark the node as visit (now)
        graph.getNode(nodeKey).setTag(1);
        distances.put(nodeKey, 0);
        LinkedList<Integer> queue = new LinkedList<>();

        queue.add(nodeKey);

        while (!queue.isEmpty()) {
            Node currNode = (Node) graph.getNodes().get(queue.poll());
            for (Integer key : currNode.getEdgeTo()) {
                if (graph.getNodes().get(key).getTag() != 1 && graph.getNodes().get(key).getTag() != 2) {
                    graph.getNodes().get(key).setTag(1);
                    distances.put(key, distances.get(currNode.getKey()) + 1);
                    lastEdge.put(key, graph.getEdge(currNode.getKey(), key));
                    queue.add(key);
                }
            }
            graph.getNode(currNode.getKey()).setTag(2);
        }
        int maxDistance = Integer.MIN_VALUE;
        for (Integer key: distances.keySet()) {
            if (distances.get(key) > maxDistance) {
                maxDistance = distances.get(key) ;
            }
        }
        for(Integer key : graph.getNodes().keySet()){
            this.graph.getNode(key).setTag(0);
        }
        return maxDistance;
    }

    /*
        this function reverses the edges of the graph of this class
     */
    public Graph createOppositeGraph() {
        ArrayList<Edge> edges = new ArrayList<>();
        ArrayList<Node> nodes = new ArrayList<>();

        Iterator<EdgeData> edgeIter = this.graph.edgeIter();
        while (edgeIter.hasNext()) {
            Edge currEdge = (Edge) edgeIter.next();
            Edge newEdge = new Edge(currEdge.getDest(), currEdge.getSrc(), currEdge.getWeight());
            edges.add(newEdge);
        }
        Iterator<NodeData> nodeIter = this.graph.nodeIter();
        while (nodeIter.hasNext()) {
            NodeData node = nodeIter.next();
            Node newNode = new Node(node.getKey(), node.getLocation());
            nodes.add(newNode);
        }

        return new Graph(edges, nodes, this.graph.getName());
    }

    public List<NodeData> createListForTSP(int sizeOfList)
    {
        List<NodeData> nodes = new ArrayList<>();
        while(nodes.size() != sizeOfList)
        {
            int currNode = ThreadLocalRandom.current().nextInt(0,this.graph.getNodes().size());
            if(!nodes.contains(this.graph.getNode(currNode)))
            {
                nodes.add(this.graph.getNode(currNode));
            }
        }
        return nodes;
    }





    public Graph createRandomGraph(int numOfNodes)
    {
        Graph graph = new Graph();
        Random r = new Random();
        int rangeMin = 100;
        int rangeMax = 110;
        for(int i =0; i < numOfNodes;i++)
        {
            double x = rangeMin + ( rangeMax-rangeMin ) * r.nextDouble();
            double y = rangeMin + ( rangeMax-rangeMin ) * r.nextDouble();
            double z = 0.0;
            NodeData node = new Node(i,x,y,z);
            graph.addNode(node);
        }
        for(Integer key: graph.getNodes().keySet())
        {
            for(int i =0; i < 10;i++)
            {
                int randomNode = ThreadLocalRandom.current().nextInt(0,numOfNodes);
                double weight = rangeMin + (rangeMax-rangeMin) * r.nextDouble();
                graph.connect(key,randomNode,weight);
            }
        }
        return graph;
    }

}