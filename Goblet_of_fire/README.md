# The-Goblet-of-fire-task-

## Game Description

Characters:

- **Harry** (Blue): The agent trained with Q-learning.
- **Death Eater** (Red): Follows Harry using BFS (shortest path).
- **Cup** (Purple): The goal Harry must reach.

The maze is read from `V1.txt`, where:

- `'X'` represents a wall
- `' '` (space) represents a path

Each episode resets the positions of Harry, the Cup, and the Death Eater.

---

## Q-Learning Details

- **State**: (Harry’s position, relative position of Death Eater to Harry, position of the Cup)
- **Actions**: Up, Down, Left, Right
- **Reward Function**:
  - +200 for reaching the Cup
  - -300 for being caught by the Death Eater
  - Otherwise: progress reward (based on distance change to cup) + danger penalty (based on inverse distance from Death Eater)

---

## Parameters

- `epsilon = 1.0`: Initial exploration rate
- `epsilon_decay = 0.9996`: How fast exploration decreases
- `min_epsilon = 0.05`: Minimum exploration rate
- `alpha = 0.5`: Learning rate
- `gamma = 0.9`: Discount factor for future rewards
- `totalepisodes = 12500`: Number of training episodes

---

## Evaluation Metrics

- **Reward Graph**: Rolling average reward per episode
- **Success Rate Graph**: Whether Harry reached the Cup (1) or not (0)

These help evaluate how well Harry is learning over time.

---

## Classes

- **Maze**: Reads maze and provides BFS for Death Eater
- **Character**: Represents Harry, Death Eater, or Cup
- **Game**: Handles training, game updates, rendering, Q-table, and logic


## Results
when running for 18000 episodes i got peak around 12000th episode which was around 70% success rate


## Failed Approach
I also came up with a new strategy but was not able to code it,
In this when harry, death eater and cup spawn randomly first harry would analyze the positions of death eater and cup, now he will move towards the nearest wall and wait there and use it as a shield to protect himself from death eater, so when death eater reaches beside that wall then harry would start circling the wall until the death eater reaches a position while following harry around that wall from which the shortest distance of harry to cup would be less than that of death eater to cup and at that moment harry would start moving towards the cup and would reach there safely.
