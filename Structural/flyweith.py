from typing import Dict, Tuple, Any

# --- Step 2: Create a Flyweight class to store intrinsic state ---
class CharacterFlyweight:
    """
    Stores the shared, intrinsic state (font, size, color).
    step_result:: Lightweight object definition for reuse.
    """
    def __init__(self, font: str, size: int, color: str):
        self._font = font
        self._size = size
        self._color = color
        # Note: This is where memory is saved, as this object is shared.

    def render(self, content: str, x: int, y: int) -> None:
        """
        Accepts the extrinsic state and performs the operation.
        step_traceability:: Provide position and content at render time.
        """
        # step_result:: Contextual flexibility without memory overhead.
        print(f"  Rendering '{content}' at ({x}, {y}) with {self._font}/{self._size}pt/{self._color}.")

# --- 2. The Flyweight Factory ---
class FlyweightFactory:
    """
    Manages the pool of shared CharacterFlyweight instances.
    step_result:: Centralized control of shared objects.
    """
    # Key: Tuple of (font, size, color)
    _flyweights: Dict[Tuple[str, int, str], CharacterFlyweight] = {}

    @staticmethod
    def get_flyweight(font: str, size: int, color: str) -> CharacterFlyweight:
        key = (font, size, color)

        # Step 3: Use a map to return existing flyweights or create new ones.
        if key not in FlyweightFactory._flyweights:
            print(f"FACTORY: Creating new Flyweight for {key}")
            FlyweightFactory._flyweights[key] = CharacterFlyweight(font, size, color)

        return FlyweightFactory._flyweights[key]

    @staticmethod
    def get_count() -> int:
        return len(FlyweightFactory._flyweights)

# --- 3. The Client and Extrinsic State ---
class DocumentCharacter:
    """
    Represents a character instance in the document, storing only the extrinsic state.
    """
    # step_traceability:: Intrinsic: font, style. Extrinsic: position, content.
    def __init__(self, content: str, x: int, y: int, flyweight: CharacterFlyweight):
        # Extrinsic State (unique per character instance)
        self.content = content
        self.x = x
        self.y = y
        # Intrinsic State (shared reference)
        self._flyweight = flyweight

    def draw(self) -> None:
        """Delegates rendering and passes the extrinsic state."""
        self._flyweight.render(self.content, self.x, self.y)

# --- Client Usage and Validation ---
if __name__ == "__main__":

    # Simulate a document with 10,000 characters
    text = "The quick brown fox jumps over the lazy dog."
    editor_characters: list[DocumentCharacter] = []

    # Define common styles
    style_normal = ("Arial", 12, "Black")
    style_bold = ("Arial", 12, "BoldBlue")
    style_heading = ("TimesNewRoman", 24, "Red")

    current_x = 0

    # Build the document structure (10,000 characters, but only 3 Flyweights)
    for i, char in enumerate(text * 250): # 10,000 characters total

        # Decide the style (Intrinsic state)
        if i < 1000:
            font, size, color = style_heading
        elif i < 5000:
            font, size, color = style_bold
        else:
            font, size, color = style_normal

        # Get the Flyweight (reuse if possible)
        flyweight = FlyweightFactory.get_flyweight(font, size, color)

        # Create the specific character instance (Extrinsic state)
        # It only stores the character, position, and a pointer to the Flyweight.
        instance = DocumentCharacter(char, current_x, 10, flyweight)
        editor_characters.append(instance)

        current_x += 1 # Move position

    # 4. Validation
    print("\n--- Validation ---")

    # Total number of character objects created (Extrinsic state holders)
    total_objects = len(editor_characters)
    # Total number of unique Flyweights created (Intrinsic state holders)
    unique_flyweights = FlyweightFactory.get_count()

    print(f"Total Character Objects Created: {total_objects}")
    print(f"Total Unique Flyweights (Shared Objects): {unique_flyweights}")

    # step_result:: Quantified performance improvement.
    print(f"\nMEMORY SAVINGS: Instead of {total_objects} full objects, we only stored {unique_flyweights} full objects.")

    # Render a small section to show usage
    print("\n--- Sample Rendering ---")
    editor_characters[500].draw()   # Heading style
    editor_characters[4500].draw()  # Bold style
    editor_characters[9000].draw()  # Normal style
