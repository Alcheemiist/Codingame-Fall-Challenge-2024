import sys
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import math

@dataclass
class Building:
    id: int
    type: int  # 0 for landing pad, >0 for module
    x: int
    y: int
    astronauts: List[int] = None
    exit: bool = False
    entrance: bool = False
    connected: bool = False

    def __post_init__(self):
        self.astronauts = self.astronauts or []

class GameState:
    def __init__(self):
        self.resources = 0
        self.buildings: Dict[int, Building] = {}
        self.routes: Set[Tuple[int, int]] = set()
        self.pods: Set[int] = set()
        self.teleports: Set[Tuple[int, int]] = set()
        self.landing_pads: Dict[int, Building] = {}
        self.modules: Dict[int, List[Building]] = defaultdict(list)
        self.pod_routes: Set[Tuple[int, int]] = set()

    def add_building(self, building: Building) -> None:
        self.buildings[building.id] = building
        if building.type == 0:
            self.landing_pads[building.id] = building
        else:
            self.modules[building.type].append(building)

    def add_route(self, id1: int, id2: int) -> None:
        self.routes.add(tuple(sorted([id1, id2])))

    def add_teleport(self, id1: int, id2: int) -> None:
        self.teleports.add(tuple(sorted([id1, id2])))

    def has_route(self, id1: int, id2: int) -> bool:
        return tuple(sorted([id1, id2])) in self.routes

    def has_teleport(self, id1: int, id2: int) -> bool:
        return tuple(sorted([id1, id2])) in self.teleports

    def has_pod_route(self, id1: int, id2: int) -> bool:
        return tuple(sorted([id1, id2])) in self.pod_routes

    def calculate_distance(self, id1: int, id2: int) -> int:
        b1 = self.buildings[id1]
        b2 = self.buildings[id2]
        return int(math.hypot(b1.x - b2.x, b1.y - b2.y) * 10)

    def find_optimal_connection_point(self, new_building: Building) -> Tuple[Optional[Building], float]:
        best_score = float('inf')
        best_target = None

        def update_best(building: Building, score: float) -> None:
            nonlocal best_score, best_target
            if score < best_score:
                best_score = score
                best_target = building

        if new_building.type == 0:  # Landing pad
            for astronaut_type in new_building.astronauts:
                for module in self.modules[astronaut_type]:
                    if module.connected:
                        distance = self.calculate_distance(new_building.id, module.id)
                        update_best(module, distance * 0.8)
        else:  # Module
            for pad in self.landing_pads.values():
                if pad.connected and new_building.type in pad.astronauts:
                    distance = self.calculate_distance(new_building.id, pad.id)
                    update_best(pad, distance * 0.8)

        # Fallback: connect to closest connected building
        if best_target is None:
            for building in self.buildings.values():
                if building.id != new_building.id and building.connected:
                    distance = self.calculate_distance(new_building.id, building.id)
                    update_best(building, distance)

        return best_target, best_score

    def initialize_network_state(self) -> None:
        for building in self.buildings.values():
            building.connected = False

        if not self.routes and self.buildings:
            next(iter(self.buildings.values())).connected = True
            return

        for id1, id2 in self.routes:
            if id1 in self.buildings:
                self.buildings[id1].connected = True
            if id2 in self.buildings:
                self.buildings[id2].connected = True

def connect_new_buildings(game: GameState, new_buildings: List[Building]) -> List[str]:
    actions = []
    sorted_buildings = sorted(new_buildings, key=lambda b: b.type != 0)
    
    for new_building in sorted_buildings:
        if not new_building.connected:
            best_target, distance = game.find_optimal_connection_point(new_building)
            
            if best_target and distance <= game.resources:
                actions.append(f"TUBE {new_building.id} {best_target.id}")
                game.resources -= 1
                game.add_route(new_building.id, best_target.id)
                new_building.connected = True

                # Secondary connection for redundancy
                if game.resources >= 1000:
                    second_target, second_distance = game.find_optimal_connection_point(new_building)
                    if (second_target and second_target.id != best_target.id 
                        and second_distance <= game.resources):
                        actions.append(f"TUBE {new_building.id} {second_target.id}")
                        game.resources -= 1
                        game.add_route(new_building.id, second_target.id)
    return actions

def setup_teleporters(game: GameState, new_buildings: List[Building]) -> List[str]:
    actions = []
    for building in new_buildings:
        if building.type == 0 and not building.entrance:
            building.entrance = True
            
            for astronaut_type in building.astronauts:
                suitable_module = next(
                    (module for module in game.modules[astronaut_type]
                     if not module.exit and not game.has_teleport(building.id, module.id)),
                    None
                )
                
                if suitable_module and game.resources >= 5000:
                    suitable_module.exit = True
                    actions.append(f"TELEPORT {building.id} {suitable_module.id}")
                    game.resources -= 5000
                    game.add_teleport(building.id, suitable_module.id)

    return actions

def setup_pods(game: GameState, new_buildings: List[Building]) -> List[str]:
    actions = []
    next_pod_id = max(game.pods, default=0) + 1

    for building in new_buildings:
        if building.type == 0:
            for astronaut_type in building.astronauts:
                for module in game.modules[astronaut_type]:
                    if (game.has_route(building.id, module.id) and 
                        not game.has_pod_route(building.id, module.id) and 
                        game.resources >= 1000):
                        
                        actions.append(f"POD {next_pod_id} {building.id} {module.id} {building.id}")
                        game.resources -= 1000
                        game.pods.add(next_pod_id)
                        game.pod_routes.add(tuple(sorted([building.id, module.id])))
                        next_pod_id += 1

    return actions

def setup_routes_and_pods(game: GameState, new_buildings: List[Building]) -> List[str]:
    actions = []
    next_pod_id = max(game.pods, default=0) + 1
    
    # Helper function to process building connections
    def process_building_connections(landing_pad: Building, is_new: bool) -> None:
        for astronaut_type in landing_pad.astronauts:
            for module in game.modules[astronaut_type]:
                # Skip if buildings aren't connected yet
                if not (landing_pad.connected and module.connected):
                    continue
                    
                # Check if route exists, if not and we have resources, create it
                if (not game.has_route(landing_pad.id, module.id) and 
                    game.resources >= game.calculate_distance(landing_pad.id, module.id)):
                    distance = game.calculate_distance(landing_pad.id, module.id)
                    if game.resources >= distance:
                        actions.append(f"TUBE {landing_pad.id} {module.id}")
                        game.resources -= distance
                        game.add_route(landing_pad.id, module.id)
                
                # Check if pod exists for the route
                if (game.has_route(landing_pad.id, module.id) and 
                    not game.has_pod_route(landing_pad.id, module.id) and 
                    game.resources >= 1000):
                    nonlocal next_pod_id
                    actions.append(f"POD {next_pod_id} {landing_pad.id} {module.id} {landing_pad.id}")
                    game.resources -= 1000
                    game.pods.add(next_pod_id)
                    game.pod_routes.add(tuple(sorted([landing_pad.id, module.id])))
                    next_pod_id += 1

    # Process new buildings first
    for building in new_buildings:
        if building.type == 0:  # Landing pad
            process_building_connections(building, is_new=True)

    # Process existing buildings
    if game.resources >= 1000:  # Only check existing if we have resources for at least one pod
        for landing_pad in game.landing_pads.values():
            if landing_pad not in new_buildings:  # Skip buildings we already processed
                process_building_connections(landing_pad, is_new=False)

    return actions

def main():
    game = GameState()

    while True:
        game.resources = int(input())
        
        num_travel_routes = int(input())
        game.routes.clear()
        for _ in range(num_travel_routes):
            id1, id2, capacity = map(int, input().split())
            game.add_route(id1, id2)
        
        num_pods = int(input())
        game.pods.clear()
        for _ in range(num_pods):
            pod_data = list(map(int, input().split()))
            game.pods.add(pod_data[0])
        
        num_new_buildings = int(input())
        new_buildings = []
        for _ in range(num_new_buildings):
            data = list(map(int, input().split()))
            building = Building(
                id=data[1],
                type=data[0],
                x=data[2],
                y=data[3],
                astronauts=data[5:] if data[0] == 0 else None
            )
            game.add_building(building)
            new_buildings.append(building)

        game.initialize_network_state()

        actions = []
       
        actions.extend(connect_new_buildings(game, new_buildings))
        actions.extend(setup_routes_and_pods(game, new_buildings))
        actions.extend(setup_teleporters(game, new_buildings))
        
        print(";".join(actions) if actions else "WAIT", file=sys.stderr)
        print(";".join(actions) if actions else "WAIT")

if __name__ == "__main__":
    main()