package code;

import api.GeoLocation;

public class StraightLineFormula {
    public double slope;
    public double b_of_formula;

    public StraightLineFormula(GeoLocation first, GeoLocation second) {
        double firstX = first.x();
        double firstY = first.y();
        double secondX = second.x();
        double secondY = second.y();

        slope = (secondY - firstY)/(secondX - firstX);
        b_of_formula = firstY-(firstX*slope);
    }

    public boolean checkOnEdge(GeoLocation pos) {
        double y = pos.y();
        double toCheck = pos.x()*this.slope + this.b_of_formula;
        return (y == toCheck);
    }

    @Override
    public String toString() {
       return "y = " + slope + "*x " +b_of_formula;
    }
}
