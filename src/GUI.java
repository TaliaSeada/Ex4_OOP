import javax.swing.*;
import api.DirectedWeightedGraph;
import api.EdgeData;
import api.GeoLocation;
import api.NodeData;
import code.GraphAlgorithms;
import code.Location;
import code.Node;

import java.awt.*;
import java.util.List;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;


public class GUI {
    private JPanel grid;

    public static void createMainWindow(String path) {
        JFrame frame = new JFrame("Graph gui");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(500, 500);
        myBoxLayout layout = new myBoxLayout();
        layout.createMainWindow(frame.getContentPane(), path);
        frame.setLocationRelativeTo(null);

        //frame.pack();
        frame.setVisible(true);
    }
    public static void activateGUI(String path){
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createMainWindow(path);
            }
        });
    }
    /*the main method runs createAndShowGui*/
    public static void main(String[] args) {
        activateGUI("src/data/A3");
    }


}

/**
 * this class builds part of the GUI for this project
 */
class showGraph extends JPanel {
    private static GraphAlgorithms GA = new GraphAlgorithms();
    private List<GeoLocation> scores;
    private int padding = 20;
    private int labelPadding = 12;
    private static int pointWidth = 7;
    private Color pointColor = new Color(255,0,0);
    private Color lineColor = new Color(0,0,0);
    private Color indexColor = new Color(0,0,255);
    public ArrayList<EdgeData> paintEdges = new ArrayList<>();
    private NodeData center;
    public HashMap<Integer,GeoLocation> locations = new HashMap<>();
    public HashMap<Integer,Point> points = new HashMap<>();

    // constructor
    public showGraph(List<GeoLocation> scores,ArrayList<EdgeData> edgesToPaint, NodeData center) {
        this.paintEdges = edgesToPaint;
        this.scores = scores;
        this.center = center;
        Iterator<NodeData> iter = GA.getGraph().nodeIter();
        while(iter.hasNext())
        {
            NodeData n = iter.next();
            locations.put(n.getKey(),n.getLocation());
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        double min_x = Double.MAX_VALUE, min_y = Double.MAX_VALUE;
        double max_x = Double.MIN_VALUE, max_y = Double.MIN_VALUE;
        int t = 0;
        while(t < scores.size()){
            if(scores.get(t).x() < min_x){
                min_x = scores.get(t).x();
            }
            if(scores.get(t).x() > max_x){
                max_x = scores.get(t).x();
            }
            if(scores.get(t).y() < min_y){
                min_y = scores.get(t).y();
            }
            if(scores.get(t).y() > max_y){
                max_y = scores.get(t).y();
            }
            t++;
        }

        double xScale = ((double) getWidth() - (3 * padding) - labelPadding) / (min_x - max_x);
        double yScale = ((double) getHeight() - 2 * padding - labelPadding) / (min_y - max_y);

        List<Point> graphPoints = new ArrayList<>();
        for (Integer key:locations.keySet()) {
            int x1 = (int) ((min_x - locations.get(key).x()) * xScale + padding);
            int y1 = (int) ((min_y - locations.get(key).y()) * yScale + padding);
            points.put(key,new Point(x1,y1));
        }

        Stroke oldStroke = g2.getStroke();
        g2.setColor(lineColor);

        for (Integer i: points.keySet()) {
            Iterator<EdgeData> edges = GA.getGraph().edgeIter(i);
            while(edges.hasNext()) {
                EdgeData edge = edges.next();
                int x1 = points.get(i).x;
                int y1 = points.get(i).y;
                int x2 = points.get(edge.getDest()).x;
                int y2 = points.get(edge.getDest()).y;

                drawArrowLine(g2,x1,y1,x2,y2,7,4);
            }
        }

        g2.setColor(Color.CYAN);

        if(paintEdges != null)
        {
            for(EdgeData edge: this.paintEdges) {
                int x1 = points.get(edge.getSrc()).x;
                int y1 = points.get(edge.getSrc()).y;
                int x2 = points.get(edge.getDest()).x;
                int y2 = points.get(edge.getDest()).y;

                drawArrowLine(g2,x1,y1,x2,y2,7,4);
            }
        }


        g2.setStroke(oldStroke);
        g2.setColor(pointColor);

        for (Integer i:this.points.keySet()) {
            g2.setColor(pointColor);
            int x = points.get(i).x - pointWidth / 2;
            int y = points.get(i).y - pointWidth / 2;
            int ovalW = pointWidth;
            int ovalH = pointWidth;
            g2.fillOval(x, y, ovalW, ovalH);

            g2.setColor(indexColor);
            g2.setFont(new Font("Serif", Font.PLAIN, 14));
            g2.drawString(i+"", x-15, y+15);
            if(this.center != null && this.center.getKey() == i) {
                g2.setColor(Color.BLACK);
                g2.drawString("center", x + 10, y - 10);
            }
        }
    }

    public static void createAndShowGui(DirectedWeightedGraph g, ArrayList<EdgeData> toPaint, NodeData center) {
        GA.init(g);
        List<GeoLocation> scores = new ArrayList<>();
        Iterator<NodeData> iter = g.nodeIter();
        while(iter.hasNext()){
            NodeData n = iter.next();
            scores.add(n.getLocation());
        }

        /* Main panel */
        showGraph mainPanel = new showGraph(scores,toPaint,center);
        mainPanel.setPreferredSize(new Dimension(800, 600));

        /* creating the frame */
        JFrame frame = new JFrame("Graph");
        frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        frame.getContentPane().add(mainPanel);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    /**
     * Draw an arrow line between two points.
     * @param g the graphics component.
     * @param x1 x-position of first point.
     * @param y1 y-position of first point.
     * @param x2 x-position of second point.
     * @param y2 y-position of second point.
     * @param d  the width of the arrow.
     * @param h  the height of the arrow.
     */
    private void drawArrowLine(Graphics g, int x1, int y1, int x2, int y2, int d, int h) {
        int dx = x2 - x1, dy = y2 - y1;
        double D = Math.sqrt(dx*dx + dy*dy);
        double xm = D - d, xn = xm, ym = h, yn = -h, x;
        double sin = dy / D, cos = dx / D;

        x = xm*cos - ym*sin + x1;
        ym = xm*sin + ym*cos + y1;
        xm = x;

        x = xn*cos - yn*sin + x1;
        yn = xn*sin + yn*cos + y1;
        xn = x;

        int[] xpoints = {x2, (int) xm, (int) xn};
        int[] ypoints = {y2, (int) ym, (int) yn};

        g.drawLine(x1, y1, x2, y2);
        g.fillPolygon(xpoints, ypoints, 3);
    }


}


/**
 * this class builds part of the GUI for this project
 */
class myBoxLayout extends JFrame implements ActionListener {
    private GraphAlgorithms GA = new GraphAlgorithms();
    List<NodeData> cities = new ArrayList<>();

    // Buttons
    JButton fileActions = new JButton("file");
    JButton graphActions = new JButton("Graph");
    JButton algoActions = new JButton("algorithms");

    JButton load = new JButton("load a file");
    JButton save = new JButton("save to file");
    JButton show = new JButton("show graph");
    JButton AddNode = new JButton("Add node");
    JButton RemoveNode = new JButton("remove Node");
    JButton Connect2Nodes = new JButton("Connect between 2 nodes");
    JButton removeEdges = new JButton("Disconnect 2 nodes");

    JButton isConnected = new JButton("Check if the graph is connected");
    JButton shortestPathDist = new JButton("Get the shortest path distance between two nodes");
    JButton shortestPath = new JButton("Show the shortest path on the graph");
    JButton center = new JButton("Show the center node on the graph");
    JButton tsp_path = new JButton("insert nodes for TSP");
    JButton drawTSP = new JButton("Draw TSP path");

    // texts
    JTextField filePath = new JTextField("enter path to file");

    // frames
    JFrame fileFrame = new JFrame("file actions window");
    JFrame graphFrame = new JFrame("graph window");
    JFrame algoFrame = new JFrame("Algorithm");
    Container cont;

    //layouts
    GroupLayout fileLayout = new GroupLayout(fileFrame.getContentPane());
    BoxLayout graphLayout = new BoxLayout(graphFrame.getContentPane(), BoxLayout.Y_AXIS);
    BoxLayout algoLayout = new BoxLayout(algoFrame.getContentPane(), BoxLayout.Y_AXIS);


    public void createMainWindow(Container pane, String path) {
        cont = pane;
        GA.load(path);
        pane.setLayout(new BoxLayout(pane, BoxLayout.Y_AXIS));


        fileActions.setAlignmentX(Component.CENTER_ALIGNMENT);
        fileActions.addActionListener(this);
        pane.add(fileActions);
        pane.add(Box.createRigidArea(new Dimension(5, 20)));


        graphActions.setAlignmentX(Component.CENTER_ALIGNMENT);
        graphActions.addActionListener(this);
        pane.add(graphActions);
        pane.add(Box.createRigidArea(new Dimension(5, 20)));


        algoActions.setAlignmentX(Component.CENTER_ALIGNMENT);
        algoActions.addActionListener(this);
        pane.add(algoActions);
        pane.add((Box.createRigidArea(new Dimension(5, 20))));
        CreateAlgoWindow();
        CreateFileWindow();
        CreateGraphWindow();
        fileFrame.setVisible(false);
        algoFrame.setVisible(false);
        graphFrame.setVisible(false);
    }

    public void CreateAlgoWindow() {
        algoFrame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        algoFrame.setSize(500, 500);
        algoFrame.setLocationRelativeTo(null);

        algoFrame.getContentPane().setLayout(algoLayout);

        isConnected.setAlignmentX(Component.CENTER_ALIGNMENT);
        isConnected.addActionListener(this);
        algoFrame.getContentPane().add(isConnected);

        shortestPathDist.setAlignmentX(Component.CENTER_ALIGNMENT);
        shortestPathDist.addActionListener(this);
        algoFrame.getContentPane().add(shortestPathDist);

        shortestPath.setAlignmentX(Component.CENTER_ALIGNMENT);
        shortestPath.addActionListener(this);
        algoFrame.getContentPane().add(shortestPath);


        center.setAlignmentX(Component.CENTER_ALIGNMENT);
        center.addActionListener(this);
        algoFrame.getContentPane().add(center);


        tsp_path.setAlignmentX(Component.CENTER_ALIGNMENT);
        tsp_path.addActionListener(this);
        algoFrame.getContentPane().add(tsp_path);

        drawTSP.setAlignmentX(Component.CENTER_ALIGNMENT);
        drawTSP.addActionListener(this);
        algoFrame.getContentPane().add(drawTSP);

        algoFrame.setVisible(false);
    }

    public void CreateFileWindow() {
        fileFrame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        fileFrame.setSize(500, 500);
        fileFrame.setLocationRelativeTo(null);

        fileFrame.getContentPane().setLayout(fileLayout);
        fileLayout.setAutoCreateGaps(true);
        fileLayout.setAutoCreateContainerGaps(true);

        save.addActionListener(this);
        JTextField path = new JTextField("Enter path of file");

        load.addActionListener(this);

        fileLayout.setHorizontalGroup(
                fileLayout.createSequentialGroup()
                        .addGroup(fileLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                .addComponent(filePath)
                                .addComponent(load))
                        .addComponent(save)


        );
        fileLayout.setVerticalGroup(
                fileLayout.createSequentialGroup()
                        .addGroup(fileLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                .addComponent(save)
                                .addComponent(load))
                        .addComponent(filePath)
        );

        fileFrame.setVisible(true);


    }

    public void CreateGraphWindow() {
        graphFrame.setDefaultCloseOperation(HIDE_ON_CLOSE);
        graphFrame.setSize(500, 500);
        graphFrame.setLocationRelativeTo(null);

        graphFrame.getContentPane().setLayout(graphLayout);

        show.setAlignmentX(Component.CENTER_ALIGNMENT);
        show.addActionListener(this);
        graphFrame.getContentPane().add(show);

        AddNode.setAlignmentX(Component.CENTER_ALIGNMENT);
        AddNode.addActionListener(this);
        graphFrame.getContentPane().add(AddNode);

        RemoveNode.setAlignmentX(Component.CENTER_ALIGNMENT);
        RemoveNode.addActionListener(this);
        graphFrame.getContentPane().add(RemoveNode);


        Connect2Nodes.setAlignmentX(Component.CENTER_ALIGNMENT);
        Connect2Nodes.addActionListener(this);
        graphFrame.getContentPane().add(Connect2Nodes);


        removeEdges.setAlignmentX(Component.CENTER_ALIGNMENT);
        removeEdges.addActionListener(this);
        graphFrame.getContentPane().add(removeEdges);

    }


    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == this.fileActions) {
            fileFrame.setVisible(true);
        }
        if (e.getSource() == this.load) {
            String Path = filePath.getText();
            if(!GA.load(Path)) {
                filePath.setText("invalid path");
            }
            else {
                fileFrame.dispose();
            }
        }
        if (e.getSource() == this.save) {
            String Path = filePath.getText();
            String[] split = Path.split("\\.");
            if (split.length == 0 || !split[split.length - 1].equals("json")) {
                filePath.setText("invalid path");
            } else {
                GA.save(Path);
                JOptionPane.showMessageDialog(null, "Saved!");
                filePath.setText("enter path file");
                fileFrame.setVisible(false);
            }
        }
        if (e.getSource() == this.graphActions) {
            graphFrame.setVisible(true);
        }
        if (e.getSource() == this.show) {
            showGraph.createAndShowGui(this.GA.getGraph(), new ArrayList<>(), null);
        }
        if (e.getSource() == this.removeEdges) {
            String src = openSrc();
            String dest = openDest();
            if(GA.getGraph().getEdge(Integer.parseInt(src), Integer.parseInt(dest)) != null) {
                this.GA.getGraph().removeEdge(Integer.parseInt(src), Integer.parseInt(dest));
            }
            else{
                JOptionPane.showMessageDialog(null, "Edge Doe's Not Exist" );
            }
        }
        if (e.getSource() == this.RemoveNode) {
            String node = openNode();
            if(GA.getGraph().getNode(Integer.parseInt(node)) != null) {
                this.GA.getGraph().removeNode(Integer.parseInt(node));
            }
            else{
                JOptionPane.showMessageDialog(null, "Node Doe's Not Exist" );
            }
        }
        if (e.getSource() == this.Connect2Nodes) {
            String node1 = openNode1();
            String node2 = openNode2();
            String w = openW();
            this.GA.getGraph().connect(Integer.parseInt(node1), Integer.parseInt(node2), Double.parseDouble(w));
        }
        if (e.getSource() == this.AddNode) {
            String node = openNode();
            String x = openLocX();
            String y = openLocY();
            GeoLocation loc = new Location(Double.parseDouble(x), Double.parseDouble(y), 0.0);
            NodeData n = new Node(Integer.parseInt(node), loc);
            this.GA.getGraph().addNode(n);
        }
        if (e.getSource() == this.algoActions) {
            algoFrame.setVisible(true);
        }
        if (e.getSource() == this.isConnected) {
            Boolean ans = this.GA.isConnected();
            String answer = ans ? "YES" : "NO";
            JOptionPane.showMessageDialog(null, answer);
        }
        if (e.getSource() == this.shortestPathDist) {
            String src = openSrc();
            String dest = openDest();
            double ans = this.GA.shortestPathDist(Integer.parseInt(src), Integer.parseInt(dest));
            if(ans == -1)
            {
                JOptionPane.showMessageDialog(null, "No Path!");
            }
            else
            {
                JOptionPane.showMessageDialog(null, ans);
            }
        }
        if (e.getSource() == this.shortestPath) {
            String src = openSrc();
            String dest = openDest();
            List<NodeData> path = this.GA.shortestPath(Integer.parseInt(src), Integer.parseInt(dest));
            if(path == null)
            {
                JOptionPane.showMessageDialog(null, "No Possible Path!");
            }
            else
            {
                showGraph.createAndShowGui(this.GA.getGraph(), getEdgesOfPath(path), null);
            }
        }
        if (e.getSource() == this.center) {
            if(this.GA.center() != null){
                showGraph.createAndShowGui(this.GA.getGraph(), null, this.GA.center());
            }
            else{
                JOptionPane.showMessageDialog(null, "There is no center");
            }

        }

        if (e.getSource() == this.tsp_path) {
            Iterator<NodeData> iter = GA.getGraph().nodeIter();
            ArrayList<Integer> option = new ArrayList<>();
            HashMap<Integer, Integer> realNode = new HashMap<>();
            while (iter.hasNext()) {
                NodeData node = iter.next();
                option.add(node.getKey());
                realNode.put(option.size()-1,node.getKey());
            }
            Object[] options = option.toArray();
            int n = JOptionPane.showOptionDialog(graphFrame,
                    "choose Nodes",
                    "A Silly Question",
                    JOptionPane.CANCEL_OPTION,
                    JOptionPane.QUESTION_MESSAGE,
                    null,
                    options,
                    null);
            NodeData no = GA.getGraph().getNode(realNode.get(n));
            if (!cities.contains(no)){
                cities.add(no);
            }
        }
        if (e.getSource() == this.drawTSP) {
            if(cities.size() == 1){
                JOptionPane.showMessageDialog(null, "Insert More Than One Node");
            }
            else if(cities.size() != 0) {
                List<NodeData> path = this.GA.tsp(cities);
                if(path != null){
                    showGraph.createAndShowGui(this.GA.getGraph(), getEdgesOfPath(path), null);
                }
                else{
                    JOptionPane.showMessageDialog(null, "No Possible path");
                }
                cities = new ArrayList<>();
            }
            else{
                JOptionPane.showMessageDialog(null, "Insert Nodes!");
            }
        }

    }

    public String openSrc() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert source node:\n",
                "Source",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0");
        return s;
    }
    public String openDest() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert destination node:\n",
                "Destination",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0");
        return s;
    }
    public String openNode() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert node:\n",
                "Node",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0");
        return s;
    }
    public String openNode1() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert first node:\n",
                "Source",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0");
        return s;
    }
    public String openNode2() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert second node:\n",
                "Destination",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0");
        return s;
    }
    public String openW() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert weight of edge:\n",
                "Weight",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0.0");
        return s;
    }
    public String openLocX() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert x-axis location of node:\n",
                "X",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0.0");
        return s;
    }
    public String openLocY() {
        String s = (String) JOptionPane.showInputDialog(
                graphFrame,
                "insert y-axis location of node:\n",
                "Y",
                JOptionPane.PLAIN_MESSAGE,
                null,
                null,
                "0.0");
        return s;
    }

    public ArrayList<EdgeData> getEdgesOfPath(List<NodeData> path) {
        ArrayList<EdgeData> pathEdges = new ArrayList<>();
        for (int i = 0; i < path.size() - 1; i++) {
            EdgeData edge = this.GA.getGraph().getEdge(path.get(i).getKey(), path.get(i + 1).getKey());
            pathEdges.add(edge);
        }

        return pathEdges;
    }
}