# Pokemon Game
In this repository we present the fifth assignment of our OOP course as part of our B.sc in computer science </br>
Collaberators: </br>
&emsp;  Lior Breitman: 212733257 </br>
&emsp;  Talia Seada: 211551601 </br>

---------------------------------------------------
## Intro
In this assignment we get a graph, a number of agents, and pokemons. The goal of the game is to collect as much pokemons as we can in the time given to each level (0-15) </br>
We took the graph implementation from our [prevoius assignment](https://github.com/TaliaSeada/Ex3_OOP) </br>
For more information: [lecturer's git](https://github.com/benmoshe/OOP_2021/tree/main/Assignments/Ex4) </br>
In this assignment we combined all the assignments we had before this one.

----------------------------
## The Algorithm </br>
First of all we seperate our algorithm into two cases, when we have one agent and when we have more than one agent.  </br>
We took insparation from our [first elevator assignment](https://github.com/TaliaSeada/Ex0_OOP) and [second elevator assignment](https://github.com/TaliaSeada/Ex1_OOP) </br>
In the first case, when we have only one agent, the algorithm is as follows: </br>
&emsp;1. Create an empty list that will hold the nodes that the agent has to go through </br>
&emsp;2. Iterate over all the pokemons and find the shortest path and distance from each one to the agent </br>
&emsp;3. Sort all the pokemons according to their distance from the agent divided by the value </br>
&emsp;4. Insert the paths in a sorted way to the agent's list </br>
&emsp;  4.b If needed, insert the path between the destination of one pokemon to the source of the next one so we dont get stuck </br>


In the second case, when we have more than one agent, the algorithm is as follows: </br>
&emsp;1. Create an empty list of lists, each one will hold the nodes that the corresponding agent need to go through </br>
&emsp;2. Set a limit which will be the number of pokemons diveded by the number of agents rouneded down </br>
&emsp;3. Iterate over all the agents and for each one: </br>
&emsp;  3.b  Iterate over all the pokemons and find the shortest path and distance from each one to the agent </br>
&emsp;  3.c  Sort all the pokemons according to their distance from the agent divided by the value </br>
&emsp;  3.d  While we are under the limit we set in step two we will pop from the start of the list of the pokemons </br>
&emsp;  3.e  Insert the paths of the pokemons we popped in a sorted way to the agent's list </br>
&emsp;  3.f  Mark the pokemons so that the next agents won't be assigned to them as well </br>


--------------------------------------
## How to download and run </br>
First you need to clone the project </br>
Next you need to run the jar file like this: java -jar Ex4_Server_v0.0.jar _ and insted of the underscore put a number between 0 and 15 </br>
Last you need to open the project in pycharm and run the GUI file with a 3.8 python interpeter

-----------------
## Results
Here are the results for the 16 cases we got to test our algorithm
![Result](https://github.com/LiorBreitman8234/Ex4_oop/blob/master/Client/picturs/results.png)
