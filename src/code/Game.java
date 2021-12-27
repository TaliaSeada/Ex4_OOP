package code;

import api.EdgeData;

import java.util.ArrayList;
import java.util.Iterator;

public class Game {
    public GraphAlgorithms algo;
    public ArrayList<Pokemon> pokemons;


    public Game(GraphAlgorithms algo) {
        this.algo = new GraphAlgorithms();
        this.algo.init(algo.getGraph());
        pokemons = new ArrayList<>();
    }

    public void setPokemonEdges() {
        for (Pokemon p : pokemons) {
            Iterator<EdgeData> iter = this.algo.getGraph().edgeIter();
            while(iter.hasNext())
            {
                Edge curr = (Edge) iter.next();
                if (curr.getDest() > curr.getSrc() && p.type > 0) {
                    if (curr.formula.checkOnEdge(p.pos)) {
                        p.on = curr;
                        break;
                    }
                } else if (curr.getDest() < curr.getSrc()  && p.type < 0) {
                    if (curr.formula.checkOnEdge(p.pos)) {
                        p.on = curr;
                        break;
                    }
                }
            }

        }
    }
}
