package code;
import api.EdgeData;
import com.google.gson.internal.LinkedTreeMap;

/**
 * this class implements the EdgeData interface
 */
public class Edge implements EdgeData, Comparable<Edge>{
    private int src;
    private int dest;
    private double w;
    public StraightLineFormula formula;
    private String info;

    public Edge(int src, int dest, double weight){
        this.dest = dest;
        this.src = src;
        this.w = weight;
        this.info = "source of edge: " + src +" destination of edge: " + dest + " weight of edge "+ weight;
    }

    public Edge(LinkedTreeMap<?,?> edge){
        String dest = edge.get("dest").toString();
        String src =  edge.get("src").toString();
        String w = edge.get("w").toString();
        this.dest = (int)Double.parseDouble(dest);
        this.src = (int)Double.parseDouble(src);
        this.w = Double.parseDouble(w);
        this.info = "source of edge: " + src +" destination of edge: " + dest + " weight of edge "+ this.w;
    }

    public Edge(Edge other){
        this.dest = other.getDest();
        this.src = other.getSrc();
        this.w = other.getWeight();
        this.info = other.getInfo();
    }


    @Override
    public int getSrc() {
        return this.src;
    }

    @Override
    public int getDest() {
        return this.dest;
    }

    @Override
    public double getWeight() {
        return this.w;
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
        return 0;
    }

    @Override
    public void setTag(int t) {

    }

    @Override
    public int compareTo(Edge o) {
        if(this.w > o.getWeight())
        {
            return 1;
        }
        else if(this.w < o.getWeight())
        {
            return -1;
        }
        return 0;
    }
}
