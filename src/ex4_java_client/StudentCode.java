package ex4_java_client;

 /**
 * @author AchiyaZigi
 * A trivial example for starting the server and running all needed commands
 */
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class StudentCode {
    private void moveGraphTOJson(String graph){
        try{
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            FileWriter fw = new FileWriter("to_load.json");
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

    }
    public static void main(String[] args) {
        Client client = new Client();
        try {
            client.startConnection("127.0.0.1", 6666);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String graphStr = client.getGraph();

        System.out.println(graphStr);
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
