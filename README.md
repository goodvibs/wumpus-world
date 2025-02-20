# Wumpus World

**This project is a solution to [the Wumpus world kata at CodeWars](https://www.codewars.com/kata/625c70f8a071210030c8e22a/train/python).**

*Below is the description of the problem, much of which is copy-pasted from CodeWars.*

## Problem

The Wumpus World is a simple world example to illustrate the worth of a knowledge-based agent and to represent knowledge representation.

### Wumpus World rules

The Wumpus world is a cave consisting of 16 rooms (in a 4x4 layout) with passageways between each pair of neighboring rooms. This cave contains:

- 1 agent - always starts from room `(0, 0)`
- 1 wumpus, a monster who eats anybody entering his room - inside random empty room 
- 1 treasure - inside random empty room 
- 1-3 bottomless pits - each inside a random empty room
(The original rules for valid cave layouts are slightly different, but they were changed for the sake of this kata.)

Initially the agent doesn't know the contents of each room. He navigates the cave blindly having only 2 sources of information:

a smell sensor which signals about the presence of Wumpus in any of the neighboring rooms
a wind sensor which signals about the presence of a bottomless pit in any of the neighboring rooms
The agent's goal is to find the hidden treasure while avoiding the bottomless pits and avoiding or killing the Wumpus - if the Wumpus's exact location can be determined, the agent can throw a spear in his direction, across a horizontal/vertical row of rooms, and kill the monster (original rules don't require knowing Wumpus's exact location: instead you can take a guess when throwing the spear and an additional sound sensor will tell you whether it hit the monster, but this was also changed for the sake of this kata).

### Task

Implement a function which receives a matrix representing a configuration of the Wumpus world and returns a boolean value signifying whether it's possible to find the treasure safely.

### Input matrix format

The input will always be a 4x4 matrix filled with following characters:

- `'W'` - Wumpus
- `'G'` - treasure (gold)
- `'P'` - bottomless pit
- `'_'` - empty space


### Visual example

Legend:

- `Agent` - agent's initial location
- `Gold` - treasure's location
- `Wumpus` - Wumpus's location
- `Pit` - bottomless pit location
- `s` - smell from Wumpus
- `w` - wind from bottomless pits

```
|------------|------------|------------|------------|
|            |            |            |            |
|            |            |            |            |
|    Agent                                          |
|            |            |            |  wwwwwwww  |
|            |            |            |  wwwwwwww  |
|-----  -----|-----  -----|-----  -----|-----  -----|
|            |            |            |            |
|            |            |         ww |            |
|                                   ww       Pit    |
|  ssssssss  |            |  wwwwwwwww |            |
|  ssssssss  |            |  wwwwwwww  |            |
|-----  -----|-----  -----|-----  -----|-----  -----|
|            |            |            |  wwwwwwww  |
|            | ss      ww |            | wwwwwwwww  |
|   Wumpus     ss Gold ww       Pit      ww         |
|            | ss      ww |            | ww         |
|            |            |            |            |
|-----  -----|-----  -----|-----  -----|-----  -----|
|  ssssssss  |            |  wwwwwwww  |            |
|  ssssssss  |            |  wwwwwwww  |            |
|                                                   |
|            |            |            |            |
|            |            |            |            |
|------------|------------|------------|------------|
```