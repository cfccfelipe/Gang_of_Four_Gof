from abc import ABC, abstractmethod
from typing import List

# --- Step 1: Define Common Interface (Component) ---
class UIComponent(ABC):
    """
    Defines the common interface for both leaf and composite components.
    step_result:: Unified contract for all components.
    """
    @abstractmethod
    def render(self) -> None:
        """Renders the component."""
        pass

    @abstractmethod
    def resize(self, new_size: int) -> None:
        """Resizes the component."""
        pass

# --- Step 5: Extend Composites for Modification (Base Class) ---
class UINode(UIComponent):
    """Base class to provide common structure management methods."""
    def addChild(self, component: 'UIComponent') -> None:
        """Default implementation for adding a child (useful for Composites)."""
        pass

    def removeChild(self, component: 'UIComponent') -> None:
        """Default implementation for removing a child."""
        pass

# --- 2. Leaf Components ---
class Button(UINode):
    """Independent component with atomic behavior."""
    def __init__(self, name: str):
        self._name = name
        self._size = 10
        print(f"Created Button: {self._name}")

    def render(self) -> None:
        print(f"  [Leaf] Rendering Button '{self._name}' (Size: {self._size})")

    def resize(self, new_size: int) -> None:
        self._size = new_size
        print(f"  [Leaf] Resizing Button '{self._name}' to {new_size}")

class Slider(UINode):
    """Independent component with atomic behavior."""
    def __init__(self, name: str):
        self._name = name
        self._size = 20
        print(f"Created Slider: {self._name}")

    def render(self) -> None:
        print(f"  [Leaf] Rendering Slider '{self._name}' (Size: {self._size})")

    def resize(self, new_size: int) -> None:
        self._size = new_size
        print(f"  [Leaf] Resizing Slider '{self._name}' to {new_size}")

# --- 3. Composite Component ---
class Panel(UINode):
    """
    Component that stores and manages child components.
    step_result:: Recursive behavior across nested structures.
    """
    def __init__(self, name: str):
        self._name = name
        self._children: List[UIComponent] = []
        print(f"Created Composite Panel: {self._name}")

    # --- Step 5: Methods for Dynamic Modification ---
    def addChild(self, component: UIComponent) -> None:
        """step_traceability:: Add methods like addChild() to manage structure."""
        self._children.append(component)
        print(f"    Added {type(component).__name__} to Panel '{self._name}'")

    def removeChild(self, component: UIComponent) -> None:
        if component in self._children:
            self._children.remove(component)
            print(f"    Removed component from Panel '{self._name}'")

    # --- Delegation and Recursive Operations ---
    def render(self) -> None:
        """Renders self, then recursively renders all children."""
        print(f"  [Composite] Rendering Panel '{self._name}'...")
        for child in self._children:
            child.render() # Recursive call

    def resize(self, new_size: int) -> None:
        """Resizes self, then recursively resizes all children."""
        print(f"  [Composite] Resizing Panel '{self._name}' and its children to {new_size}...")
        for child in self._children:
            child.resize(new_size) # Recursive call

# --- 4. Client Usage and Hierarchy Traversal ---
if __name__ == "__main__":

    # 1. Build the Hierarchy

    # Outer Structure
    main_window = Panel("Main Window")

    # Inner Panel 1 (Composite)
    header_panel = Panel("Header")
    header_panel.addChild(Button("Save Button"))
    header_panel.addChild(Slider("Zoom Slider"))

    # Inner Panel 2 (Composite)
    footer_panel = Panel("Footer")
    footer_panel.addChild(Button("Help Button"))

    # Nested the inner panels into the main window
    main_window.addChild(header_panel)
    main_window.addChild(footer_panel)

    # 2. Uniform Operation (Rendering)
    print("\n--- ACTION 1: Rendering the Entire Window ---")
    # Client code calls render() without knowing it contains leaves and composites.
    # step_traceability:: Client code calls render() without knowing if the component is a leaf or composite.
    main_window.render()
    # step_result:: Simplified logic and flexible hierarchy traversal.

    # 3. Uniform Operation (Resizing)
    print("\n--- ACTION 2: Resizing the Entire Window ---")
    main_window.resize(new_size=50)
