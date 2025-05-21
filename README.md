# The-Goblet-of-fire-task-

 ## Approach
1. Environment
The environment is loaded from a maze text file (V1.txt) using the Maze class.
Walls (X) are impassable; free spaces ( ) are valid cells.
Each episode starts with random valid positions for:
Harry (Agent)
Death Eater (Chaser)
Cup (Goal)

2. Q-learning Setup
State Representation: (Harry_pos, (dx, dy), (cx, cy)), where:
Harry_pos = current position of Harry
(dx, dy) = relative position of the Death Eater
(cx, cy) = fixed position of the cup
Actions: Up, Down, Left, Right
Rewards:
+200 on reaching the cup
-300 if caught by the Death Eater
Distance-based progress reward and danger penalty for intermediate steps
Epsilon-greedy policy with decay for exploration

3. Death Eater AI
Uses Breadth-First Search (BFS) to move one step closer to Harry on each turn.

## Assumptions
The maze file (V1.txt) is properly formatted and present at the specified path.
All characters start in valid positions (not on a wall).
The cup position remains fixed for all episodes (for consistent goal-learning).
Game visuals (draw()) are disabled during training for faster simulation

## Failed Approach
I also came up with a new strategy but was not able to code it,
In this when harry, death eater and cup spawn randomly first harry would analyze the positions of death eater and cup, now he will move towards the nearest wall and wait there and use it as a shield to protect himself from death eater, so when death eater reaches beside that wall then harry would start circling the wall until the death eater reaches a position while following harry around that wall from which the shortest distance of harry to cup would be less than that of death eater to cup and at that moment harry would start moving towards the cup and would reach there safely.
