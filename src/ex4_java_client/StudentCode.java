package ex4_java_client;
 /**
 * @author AchiyaZigi
 * A trivial example for starting the server and running all needed commands
 */
import api.DirectedWeightedGraph;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;
import api.DirectedWeightedGraphAlgorithms;
import code.GraphAlgorithms;

public class StudentCode {
    public static void main(String[] args) {
        Client client = new Client();
        try {
            client.startConnection("127.0.0.1", 6666);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String graphStr = client.getGraph();
        String info = client.getInfo();
        String[] split = info.split(",");
        System.out.println(split[7]);
        String[] splitGraph = split[7].split(":");
        System.out.println(splitGraph[1]);
        String[] splitPath = splitGraph[1].split("\"");
        String path = "src/" + splitPath[1];
        System.out.println(path);
        GraphAlgorithms algo = new GraphAlgorithms();
        algo.load(path);
        System.out.println((algo.center().getKey()));
//        client.addAgent("{\"id\":0}");
//        String agentsStr = client.getAgents();
//        System.out.println(agentsStr);
//        String pokemonsStr = client.getPokemons();
//        System.out.println(pokemonsStr);
//        String isRunningStr = client.isRunning();
//        System.out.println(isRunningStr);
//
//        client.start();
//        int counter = 0;
//
//        while (client.isRunning().equals("true")) {
//            client.move();
//            System.out.println(client.getAgents());
//            System.out.println(client.timeToEnd());
//
//            Scanner keyboard = new Scanner(System.in);
//            System.out.println("enter the next dest: ");
//            int next = keyboard.nextInt();
//            client.chooseNextEdge("{\"agent_id\":0, \"next_node_id\": " + next + "}");
//            if(counter == 3)
//            {
//                client.stop();
//            }
//            counter++;
//        }
    }

}
