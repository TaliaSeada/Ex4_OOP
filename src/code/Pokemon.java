package code;

import api.EdgeData;
import api.GeoLocation;

public class Pokemon {
    public double value;
    public int type;
    public GeoLocation pos;
    public EdgeData on;

    public Pokemon(double value, int type, GeoLocation pos)
    {
        this.value = value;
        this.type = type;
        this.pos = pos;
    }
}
