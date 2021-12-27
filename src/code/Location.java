package code;

import api.GeoLocation;

/**
 * this class implements the GeoLocation interface
 */
public class Location implements GeoLocation {
    private double x;
    private double y;
    private double z;

    public Location(double x, double y, double z){
        this.x = x;
        this.y = y;
        this.z = z;
    }


    @Override
    public double x() {
        return this.x;
    }

    @Override
    public double y() {
        return this.y;
    }

    @Override
    public double z() {
        return this.z;
    }

    @Override
    public double distance(GeoLocation g) {
        double xDist = Math.pow(this.x - g.x(),2);
        double yDist = Math.pow(this.y - g.y(),2);
        double zDist = Math.pow(this.z - g.z(),2);
        return Math.sqrt(xDist + yDist + zDist);
    }

    public String toString() {
        return this.x + "," + this.y + "," + this.z;
    }
}
