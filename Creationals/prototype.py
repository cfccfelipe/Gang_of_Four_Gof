import copy
from abc import ABC, abstractmethod
from typing import Dict, Any, List

# --- Step 1: Define Prototype Interface ---
class GameEntityPrototype(ABC):
    """
    Defines the contract for cloneable objects.
    step_result:: Reusable object creation logic decoupled from constructors.
    """
    @abstractmethod
    def clone(self) -> 'GameEntityPrototype':
        """Performs a deep copy of the entity."""
        pass

class GameEntity(GameEntityPrototype):
    """
    The concrete prototype, holding stats and behaviors.
    """
    def __init__(self, name: str, health: int, speed: float, equipment: List[str]):
        # Intrinsic/Shared State
        self.name = name
        self.health = health
        self.speed = speed
        # Mutable Field (Requires deep copy)
        self.equipment = equipment

        # Extrinsic/Unique State (will be set after cloning)
        self.position: List[int] = [0, 0]

    # --- Step 4: Ensure deep cloning of mutable fields ---
    def clone(self) -> 'GameEntity':
        """
        Creates a deep copy to ensure the new instance has independent state.
        step_result:: Independent instances with isolated state.
        """
        # copy.deepcopy handles the deep copying of mutable lists like self.equipment
        return copy.deepcopy(self)

    # --- Step 5: Support Dynamic Configuration ---
    def initialize_position(self, x: int, y: int) -> None:
        """
        Hook to set the extrinsic (contextual) state after cloning.
        step_result:: Flexible reuse with contextual customization.
        """
        self.position = [x, y]
        print(f"ENTITY: {self.name} initialized at ({x}, {y}).")

    def display_status(self) -> None:
        print(f"ENTITY: {self.name} | HP: {self.health} | Pos: {self.position} | Equip ID: {id(self.equipment)}")

# --- 2. The Prototype Registry ---
class EntityRegistry:
    """
    Manages pre-configured prototype instances.
    step_result:: Centralized access to reusable templates.
    """
    _prototypes: Dict[str, GameEntity] = {}

    @staticmethod
    def register_prototype(key: str, prototype: GameEntity) -> None:
        EntityRegistry._prototypes[key] = prototype

    @staticmethod
    def get_prototype(key: str) -> GameEntity:
        if key not in EntityRegistry._prototypes:
            raise ValueError(f"Prototype '{key}' not registered.")
        return EntityRegistry._prototypes[key]

# --- Client Usage ---
if __name__ == "__main__":

    # 1. Create the base prototype (expensive initialization simulated here)
    base_orc_prototype = GameEntity(
        name="OrcGrunt",
        health=100,
        speed=5.0,
        equipment=["Axe", "Shield"]
    )

    # 2. Store the prototype in the registry
    EntityRegistry.register_prototype("Orc", base_orc_prototype)
    print("REGISTRY: Base Orc Prototype stored.")

    # 3. Spawn 3 new enemies by cloning

    # Spawn Enemy 1
    orc_1 = EntityRegistry.get_prototype("Orc").clone()
    orc_1.initialize_position(10, 20) # Set extrinsic state

    # Spawn Enemy 2
    orc_2 = EntityRegistry.get_prototype("Orc").clone()
    orc_2.initialize_position(50, 75)

    # Spawn Enemy 3
    orc_3 = EntityRegistry.get_prototype("Orc").clone()
    orc_3.initialize_position(90, 10)

    # --- Step 3: Fast, consistent instantiation ---
    print("\n--- Displaying Spawned Entities ---")
    orc_1.display_status()
    orc_2.display_status()
    orc_3.display_status()

    # --- Validation of Isolation (Deep Cloning Check) ---
    print("\n--- Validation Check: Isolation ---")

    # Change mutable state in one clone
    orc_1.equipment.append("Potion")
    print("CHECK: Orc-1 equipment modified.")

    # Check if others were affected (they shouldn't be)
    print(f"Orc-1 Equipment: {orc_1.equipment}")
    print(f"Orc-2 Equipment: {orc_2.equipment}")

    # The IDs of the equipment lists must be different (due to deepcopy)
    is_isolated = orc_1.equipment is not orc_2.equipment
    print(f"Isolation check passed (independent lists)? {is_isolated}")
