/**
 * this class represents a node and its distance from the source node in the Dijkstra algorithm
 */
class pair implements Comparable<pair>{
    public int node;
    public double dist;

    public pair(int n, double dist){
        this.node = n;
        this.dist = dist;
    }

    public pair(){
        this.node = -1;
        this.dist = 0;
    }

    public int getNode() {
        return node;
    }

    public double getDist() {
        return dist;
    }

    public void setNode(int node) {
        this.node = node;
    }

    public void setDist(double dist) {
        this.dist = dist;
    }

    @Override
    public int compareTo(pair other) {
        if(other.getDist() > this.dist) return -1;
        else if(other.getDist() == this.dist) return 0;
        else{return 1;}
    }

    @Override
    public boolean equals(Object o){
        if(o == this) {
            return true;
        }
        if(!(o instanceof pair)){
            return false;
        }

        if(this.node == ((pair) o).getNode()){
            return true;
        }
        return false;
    }
}


