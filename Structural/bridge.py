from abc import ABC, abstractmethod


# --- Step 3: Define Implementation Interface (Renderer) ---
class Renderer(ABC):
    """
    Unified contract for rendering across platforms.
    step_result:: Unified contract for rendering across platforms.
    """
    @abstractmethod
    def render_circle(self) -> None:
        pass

    @abstractmethod
    def render_square(self) -> None:
        pass

# --- Step 4: Implement Concrete Renderers ---
class WindowsRenderer(Renderer):
    """Platform-specific logic for Windows."""
    def render_circle(self) -> None:
        print("PLATFORM: 🖼️ Drawing Circle using Windows GDI/DirectX.")

    def render_square(self) -> None:
        print("PLATFORM: 🖼️ Drawing Square using Windows GDI/DirectX.")

class LinuxRenderer(Renderer):
    """Platform-specific logic for Linux."""
    def render_circle(self) -> None:
        print("PLATFORM: 🐧 Drawing Circle using Linux X11/Wayland.")

    def render_square(self) -> None:
        print("PLATFORM: 🐧 Drawing Square using Linux X11/Wayland.")
        # step_result:: Scalable support for multiple platforms.

# --- 2. The Abstraction Hierarchy (Shape) ---

# --- Step 1: Define Abstraction Interface (Shape) ---
class Shape(ABC):
    """
    Decoupled abstraction layer that supports delegation.
    step_result:: Decoupled abstraction layer that supports delegation.
    """
    # Step 5: Inject renderer into shape via constructor
    def __init__(self, renderer: Renderer):
        self._renderer = renderer

    @abstractmethod
    def draw(self) -> None:
        """The main method that delegates the rendering task."""
        pass

    def resize(self, factor: float) -> None:
        """Abstraction method that doesn't depend on the Renderer."""
        print(f"SHAPE: Resizing by factor {factor} (Logic independent of platform).")

# --- Step 2: Implement Concrete Abstractions (Shapes) ---
class Circle(Shape):
    """Flexible shape definition independent of platform logic."""
    def draw(self) -> None:
        """Calls the appropriate method on the injected Renderer."""
        print("SHAPE: Preparing to draw a Circle...")
        self._renderer.render_circle() # Delegation

class Square(Shape):
    """Flexible shape definition independent of platform logic."""
    def draw(self) -> None:
        """Calls the appropriate method on the injected Renderer."""
        print("SHAPE: Preparing to draw a Square...")
        self._renderer.render_square() # Delegation
        # step_result:: Flexible shape definitions independent of platform logic.

# --- Client Usage ---
if __name__ == "__main__":

    # 1. Setup Renderers
    windows_impl = WindowsRenderer()
    linux_impl = LinuxRenderer()

    # 2. Setup Shapes and Inject Renderers (Step 5)

    # --- Windows Platform Rendering ---
    print("\n=== Scenario 1: Windows Platform ===")

    # Inject WindowsRenderer into Circle and Square
    windows_circle = Circle(windows_impl)
    windows_square = Square(windows_impl)

    windows_circle.draw()
    windows_square.draw()
    windows_circle.resize(1.5) # Non-platform specific behavior

    # --- Linux Platform Rendering ---
    print("\n=== Scenario 2: Linux Platform ===")

    # Inject LinuxRenderer into Circle and Square
    linux_circle = Circle(linux_impl)
    linux_square = Square(linux_impl)

    linux_circle.draw()
    linux_square.draw()

    # Demonstration of independent variation:
    # Adding a new shape (e.g., Triangle) only requires one new class.
    # Adding a new platform (e.g., MacRenderer) only requires one new class.
