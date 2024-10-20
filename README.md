#  Codingame-Fall-Challenge-2024 : Selenia City Transportation Network

## Objective
Welcome to **Selenia City**, the first city on the moon, set to be inaugurated in **2050**! As the architect of the first lunar transportation network, your task is to develop a dynamic solution adaptable to evolving city layouts. After your victory in the planetary programming games, you have been entrusted with designing the artificial intelligence for this ambitious project.

## Rules
The game is played over **20 lunar months**, each consisting of **20 days**. 

### Monthly Cycle
- At the beginning of each month, you will receive resources and a list of new buildings constructed in Selenia City.
- Utilize your resources to connect new buildings to the transportation network or reinforce existing infrastructure.


## Scoring
our goal is to maximize the score before the end of the simulation. Points are awarded based on astronauts reaching their targets:
- **Up to 100 points** for each astronaut:
  - **Speed:** 50 points, minus the number of days taken to reach the destination.
  - **Population Balance:** 50 points, minus the number of astronauts who have already reached the same module in the current lunar month (negative scores reset to 0).

## Implementation Summary

### Overview
My solution is a simulation for managing a space station's construction, where different types of buildings are connected to facilitate movement and resource management. The core components include the management of landing pads, modules, routes, and the connection of new buildings based on their types and existing structures.

### Key Components

#### Data Classes
- **Building**: Represents a building in the space station with attributes such as `id`, `type`, `coordinates (x, y)`, and lists of astronauts assigned to it. 
- **GameState**: Manages the overall state of the game, including buildings, routes, teleports, and resource management.

#### Functions and Methods

- **add_building**: Adds a new building to the game state and categorizes it as a landing pad or module.
- **add_route**: Establishes a connection (route) between two buildings.
- **add_teleport**: Creates a teleport connection between two buildings.
- **has_route**: Checks if a route exists between two buildings.
- **calculate_distance**: Computes the distance between two buildings based on their coordinates.
- **find_optimal_connection_point**: Determines the best existing building to connect a new building based on distance and astronaut compatibility.
- **initialize_network_state**: Sets up the connectivity status of buildings based on established routes.

#### Logic Flow
1. **Building Addition**: When a new building is added, the system checks its type (landing pad or module) and assigns it to the appropriate category.
2. **Route Management**: Routes and teleports are managed to facilitate movement between buildings.
3. **Connection Optimization**: For each new building, the system identifies the most suitable existing building to connect to, considering distance and astronaut assignments.
4. **Network Initialization**: The initial connection states of buildings are established, ensuring at least one building is marked as connected.

#### Use Cases
- **Space Station Expansion**: As new modules or landing pads are added, the system optimally connects them to the existing infrastructure.
- **Resource Management**: By efficiently connecting buildings, the solution enhances the management of resources and astronauts on the space station.

### Conclusion
This solution provides a structured approach to managing a space station's buildings and their connections. It allows for efficient growth and resource management, ensuring the station can adapt as new buildings are added.

### Results

![Results Diagram](./p1.png)
![Results Diagram](./p2.png)


## 6. Source Code
The game's source code is available [here](#) (https://github.com/CodinGame/FallChallenge2024-SeleniaCity).
