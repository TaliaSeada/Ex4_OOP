package code;

import api.GeoLocation;
import api.NodeData;
import com.google.gson.internal.LinkedTreeMap;

import java.util.ArrayList;

/**
 * this class implements the NodeData interface
 */
public class Node implements NodeData {
    private int key;
    private GeoLocation loc;
    private String info;
    private ArrayList<Integer> EdgesToNode;
    private ArrayList<Integer> EdgesFromNode;
    private int tag; // 0 - white, 1 - gray, 2 - black
//    private double weight;
    public Node(int key, GeoLocation location) {
        this.EdgesFromNode = new ArrayList<>();
        this.EdgesToNode = new ArrayList<>();
        this.loc = location;
        this.key = key;
        this.info = "Location of node: x = " + this.loc.x() + " y = " + this.loc.y() + " z = "+ this.loc.z();
    }
    public Node(int key,double x, double y, double z){
        this.EdgesFromNode = new ArrayList<>();
        this.EdgesToNode = new ArrayList<>();
        this.loc = new Location(x,y,z);
        this.key = key;
        this.info = "Location of node: x = " + x + " y = " + y + " z = "+ z;
    }

    public Node(LinkedTreeMap<?,?> node) {
        this.EdgesFromNode = new ArrayList<>();
        this.EdgesToNode = new ArrayList<>();
        String pos = node.get("pos").toString();
        String id = node.get("id").toString();;
        String[] posValues = pos.split(",");
        this.key = (int) Double.parseDouble(id);
        Location loc = new Location(Double.parseDouble(posValues[0]),Double.parseDouble(posValues[1]),Double.parseDouble(posValues[2]));
        this.loc = loc;
        this.info = "Location of node #"+ this.key +" : x = " + loc.x() + " y = " + loc.y() + " z = "+ loc.z();
        this.tag = 0;
    }

    public Node(Node other){
        this.key = other.getKey();
        this.loc = new Location(other.getLocation().x(),other.getLocation().y(),other.getLocation().z());
        this.info = other.getInfo();
        this.EdgesFromNode = new ArrayList<Integer>(other.getFromNode());
        this.EdgesToNode = new ArrayList<Integer>(other.getToNode());
        this.tag = other.getTag();
    }

    public Node(int key, GeoLocation pos, String happy) {
        this.key = key;
        this.loc = pos;
        System.out.println(happy);
    }

    public ArrayList<Integer> getToNode(){
        return this.EdgesToNode;
    }

    public ArrayList<Integer> getFromNode(){
        return this.EdgesFromNode;
    }

    // this function adds an edge to the correct list (if the edge go out or come in)
    public void addEdge(Edge edge) {
        if(edge.getSrc() == this.key) {
            EdgesFromNode.add(edge.getDest());
        }
        else if(edge.getDest() == this.key) {
            EdgesToNode.add(edge.getSrc());
        }
    }
    // this function removes an edge from the correct list (if the edge go out or come in)
    public void removeEdge(int node,String type) {
        if(type.equals("dest")) {
            this.EdgesFromNode.remove((Integer)node);
        }
        else {
            this.EdgesToNode.remove((Integer)node);
        }
    }

    @Override
    public int getKey() {
        return this.key;
    }

    @Override
    public GeoLocation getLocation() {
        return this.loc;
    }

    @Override
    public void setLocation(GeoLocation p) {
        this.loc = (Location) p;
    }

    @Override
    public double getWeight() {
        return 0;
    }

    @Override
    public void setWeight(double w) {}

    public ArrayList<Integer> getEdgeTo()
    {
        return this.EdgesToNode;
    }

    public ArrayList<Integer> getEdgeFrom()
    {
        return this.EdgesFromNode;
    }

    @Override
    public String getInfo() {
        return this.info;
    }

    @Override
    public void setInfo(String s) {
        this.info = s;
    }

    @Override
    public int getTag() {
        return this.tag;
    }

    @Override
    public void setTag(int t) {
        this.tag = t;
    }
}
