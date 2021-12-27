import api.DirectedWeightedGraph;
import api.EdgeData;
import api.NodeData;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

/**
 * this class represent the graph by implementing the DirectedWeightedGraph algorithm
 */
public class Graph implements DirectedWeightedGraph {
    private HashMap<Integer,NodeData> nodes;
    private HashMap<Integer,HashMap<String,EdgeData>> nodeEdges;
    private ArrayList<EdgeData> allEdges;
    private final String name;
    private int MC =0;

    public Graph(){
        this.name = "testStuff";
        this.nodeEdges = new HashMap<>();
        this.nodes = new HashMap<>();
        this.allEdges = new ArrayList<>();

        //for each node we have in this graph, we add the edges that this node is their src
        for(Integer key: this.nodes.keySet()) {
            HashMap<String,EdgeData> edgesFrom = new HashMap<>();
            this.nodeEdges.put(key,edgesFrom);
            MC++;
        }
    }

    public Graph(ArrayList<Edge> edges, ArrayList<Node> nodes,String name){
        this.nodeEdges = new HashMap<>();
        this.nodes = new HashMap<>();
        for(NodeData node:nodes) {
            this.nodes.put(node.getKey(),node);
            MC++;
        }
        for(Integer key: this.nodes.keySet()) {
            HashMap<String,EdgeData> edgesFrom = new HashMap<>();
            for(EdgeData edge: edges) {
                if(edge.getSrc() == key) {
                    edgesFrom.put(key +"-"+edge.getDest(),edge);
                }
            }
            this.nodeEdges.put(key,edgesFrom);
            MC++;
        }
        for(Integer key:this.nodeEdges.keySet()) {
            for(String edgeKey:this.nodeEdges.get(key).keySet()) {
                Node srcNode = (Node)this.nodes.get(key);
                Node destNode = (Node)this.nodes.get(Integer.parseInt(edgeKey.split("-")[1]));
                srcNode.getFromNode().add(destNode.getKey());
                destNode.getToNode().add(key);
            }
        }
        this.allEdges = new ArrayList<>(edges);
        this.name = name;
        MC++;
    }

    public Graph(Graph other){
        this.nodes = new HashMap<>();
        this.nodeEdges = new HashMap<>();
        for(Integer key:other.getNodeEdges().keySet()) {
            HashMap<String,EdgeData> edgesTo = new HashMap<>();
            for(String edgeKey:other.getNodeEdges().get(key).keySet()) {
                edgesTo.put(edgeKey,other.getNodeEdges().get(key).get(edgeKey));
            }
            this.nodeEdges.put(key,edgesTo);
            MC++;
        }
        for(Integer key:other.getNodes().keySet()) {
            this.nodes.put(key,other.getNodes().get(key));
            MC++;
        }
        this.name = other.getName();
        this.allEdges = new ArrayList<>(other.allEdges);
        MC++;
    }

    public ArrayList<EdgeData> getAllEdges(){
        return this.allEdges;
    }

    public HashMap<Integer, HashMap<String, EdgeData>> getNodeEdges() {
        return nodeEdges;
    }

    public HashMap<Integer, NodeData> getNodes(){
        return this.nodes;
    }
    public String getName(){
        return this.name;
    }

    @Override
    public NodeData getNode(int key) {
        return this.nodes.get(key);
    }

    @Override
    public EdgeData getEdge(int src, int dest) {
        String key = src +"-"+dest;
        return this.nodeEdges.get(src).get(key);
    }

    @Override
    public void addNode(NodeData n) {
        if(this.nodeEdges.get(n) == null) {
            HashMap<String, EdgeData> edges = new HashMap<>();
            this.nodeEdges.put(n.getKey(),edges);
        }
        this.nodes.put(n.getKey(),n);
        MC++;
    }

    @Override
    public void connect(int src, int dest, double w) {
        if(this.nodeEdges.get(src).get(src + "-" + dest) == null && src != dest) {
            Edge edgeData = new Edge(src,dest,w);
            String key = src + "-" + dest;
            this.nodeEdges.get(src).put(key,edgeData);
            Node source = (Node)this.nodes.get(src);
            Node destination = (Node)this.nodes.get(dest);
            source.addEdge(edgeData);
            destination.addEdge(edgeData);
            this.allEdges.add(edgeData);
            MC++;
        }
    }

    @Override
    public Iterator<NodeData> nodeIter() throws RuntimeException{
        return this.nodes.values().iterator();
    }

    @Override
    public Iterator<EdgeData> edgeIter() throws RuntimeException {
        return allEdges.iterator();
    }

    @Override
    public Iterator<EdgeData> edgeIter(int node_id) throws RuntimeException{
        if(!this.nodeEdges.containsKey(node_id)) {
            return null;
        }
        HashMap<String, EdgeData> edges = this.nodeEdges.get(node_id);
        return edges.values().iterator();
    }

    @Override
    public NodeData removeNode(int key) {
        Node node = (Node)this.nodes.get(key);
        if(node != null) {
            ArrayList<Integer> nodesConnectedTo = new ArrayList<>();
            nodesConnectedTo.addAll(node.getToNode());
            for(int i = 0; i < nodesConnectedTo.size();i++) {
                removeEdge(nodesConnectedTo.get(i),key);
            }
            nodesConnectedTo.clear();
            nodesConnectedTo.addAll(node.getFromNode());
            for(int i = 0; i < nodesConnectedTo.size();i++) {
                removeEdge(key,nodesConnectedTo.get(i));
            }
            this.nodes.remove(key);
            this.nodeEdges.remove(key);
            MC++;
            return node;
        }
        return null;
    }

    @Override
    public EdgeData removeEdge(int src, int dest) {
        EdgeData edge = this.nodeEdges.get(src).get(src+"-"+dest);
        if(edge != null) {
            Node nodeSrc = (Node)this.nodes.get(src);
            Node nodeDest = (Node)this.nodes.get(dest);
            nodeSrc.removeEdge(dest, "dest");
            nodeDest.removeEdge(src, "src");
            this.nodeEdges.get(src).remove(src+"-"+dest);
            this.allEdges.remove(edge);
            MC++;
        }
        return edge;
    }

    @Override
    public int nodeSize() {
        return this.nodes.size();
    }

    @Override
    public int edgeSize() {
        return this.nodeEdges.size();
    }

    @Override
    public int getMC() {
        return MC;
    }
}
