package code;
import api.DirectedWeightedGraph;
import api.DirectedWeightedGraphAlgorithms;

/**
 * This class is the main class for Ex2 - your implementation will be tested using this class.
 */
public class Ex2 {
    /**
     * This static function will be used to test your implementation
     * @param json_file - a json file (e.g., G1.json - G3.gson)
     * @return
     */
    public static DirectedWeightedGraph getGrapg(String json_file) {
        GraphAlgorithms GA = new GraphAlgorithms();
        GA.load(json_file);
        DirectedWeightedGraph ans = (Graph) GA.getGraph();
        return ans;
    }
    /**
     * This static function will be used to test your implementation
     * @param json_file - a json file (e.g., G1.json - G3.gson)
     * @return
     */
    public static DirectedWeightedGraphAlgorithms getGrapgAlgo(String json_file) {
        DirectedWeightedGraphAlgorithms ans = new GraphAlgorithms();
        ans.load(json_file);
        return ans;
    }
    /**
     * This static function will run your GUI using the json fime.
     * @param json_file - a json file (e.g., G1.json - G3.gson)
     *
     */
//    public static void runGUI(String json_file) {
//        DirectedWeightedGraphAlgorithms alg = getGrapgAlgo(json_file);
//        GUI.activateGUI(json_file);
//
//    }
}