#  Codingame-Fall-Challenge-2024 : Selenia City Transportation Network

## 1. Statement
### Objective
Welcome to **Selenia City**, the first city on the moon, set to be inaugurated in **2050**! As the architect of the first lunar transportation network, your task is to develop a dynamic solution adaptable to evolving city layouts. After your victory in the planetary programming games, you have been entrusted with designing the artificial intelligence for this ambitious project.

## 2. Rules
The game is played over **20 lunar months**, each consisting of **20 days**. 

### Monthly Cycle
- At the beginning of each month, you will receive resources and a list of new buildings constructed in Selenia City.
- Utilize your resources to connect new buildings to the transportation network or reinforce existing infrastructure.


## 3. Scoring
Your goal is to maximize your score before the end of the simulation. Points are awarded based on astronauts reaching their targets:
- **Up to 100 points** for each astronaut:
  - **Speed:** 50 points, minus the number of days taken to reach the destination.
  - **Population Balance:** 50 points, minus the number of astronauts who have already reached the same module in the current lunar month (negative scores reset to 0).

### Example Scenarios
- Details on scoring examples can be added here.

## 4. Implementation
Each lunar month occurs in **4 stages**:

1. **City Parsing**
   - Your code receives information about new constructions in Selenia City.
   
   **Program Input:**  
   - Details on program input can be added here.

2. **Transport Infrastructure Improvements**
   - Modify the city by implementing actions to enhance its transportation network.
   
   **Allowed Actions:**  
   - Details on allowed actions can be added here.

3. **Astronaut Movement**
   - After implementing network modifications, astronauts will autonomously move towards their target modules over **20 days**.

   **Movement Simulation:**  
   - Details on movement simulation can be added here.

4. **End of the Lunar Month**
   - At the end of each month, remaining astronauts disappear and all pods return to their starting points. Unused resources yield **10% interest** (rounded down).

### Constraints
- Up to **150 buildings** may be constructed.
- Each landing pad accommodates between **1 and 100 astronauts** monthly.
- Up to **1000 astronauts** can arrive each month.
- No building will obstruct existing tubes.
- Your program must return its list of actions within **500 milliseconds** (or **1000 milliseconds** for the first turn).
- Every astronaut arriving at a landing pad will have at least **1 module** of the same type already constructed.


## 5. Solution Summary

### Overview
The provided solution is a simulation for managing a space station's construction, where different types of buildings are connected to facilitate movement and resource management. The core components include the management of landing pads, modules, routes, and the connection of new buildings based on their types and existing structures.

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

## 6. Source Code
The game's source code is available [here](#) (https://github.com/CodinGame/FallChallenge2024-SeleniaCity).