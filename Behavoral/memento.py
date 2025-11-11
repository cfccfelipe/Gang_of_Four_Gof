from typing import Dict, Any, List

# --- Step 1: Define a Memento class ---
class FormState:
    """
    The Memento: Stores the internal state of the FormEditor.
    step_result:: Encapsulated state representation for recovery.
    """
    def __init__(self, field_values: Dict[str, str]):
        # Store a deep copy of the state to prevent external modification
        self._state = field_values.copy()
        self._timestamp = "Snapshot created at [Time/Date simulation]" # Optional metadata

    def get_saved_state(self) -> Dict[str, str]:
        """Method used by the Originator to retrieve the state."""
        return self._state.copy() # Return a copy for protection

    def get_metadata(self) -> str:
        """Method used by the Caretaker for history viewing."""
        return f"State: {self._timestamp}, Fields: {list(self._state.keys())}"

# --- 2. The Originator (The Editor) ---
class FormEditor:
    """
    The Originator: Holds the current state and controls Memento creation/restoration.
    step_result:: Controlled state transitions with encapsulation.
    """
    def __init__(self, initial_values: Dict[str, str]):
        self._field_values = initial_values
        self._last_change = "Initialization"

    @property
    def state(self) -> Dict[str, str]:
        return self._field_values

    def update_field(self, field_name: str, new_value: str) -> None:
        """Simulates a user changing an input field."""
        self._last_change = f"Changed '{field_name}' from '{self._field_values.get(field_name)}' to '{new_value}'"
        self._field_values[field_name] = new_value
        print(f"EDITOR: Change executed: {self._last_change}. Current State: {self._field_values}")

    def createMemento(self) -> FormState:
        """
        Captures the current state into a Memento.
        step_traceability:: Call createMemento() before modifying the editor.
        """
        print("EDITOR: 📸 Capturing state snapshot...")
        return FormState(self._field_values)

    def restoreMemento(self, memento: FormState) -> None:
        """
        Restores the editor's internal state from a Memento.
        step_traceability:: Retrieve last memento and call restoreMemento() on the editor.
        """
        self._field_values = memento.get_saved_state()
        self._last_change = "Restored from Memento"
        print(f"EDITOR: ⏪ State restored. Current State: {self._field_values}")

# --- 3. The Caretaker (History Manager) ---
class HistoryManager:
    """
    The Caretaker: Manages the collection of Mementos.
    step_result:: Organized state tracking for undo/redo.
    """
    def __init__(self):
        # step_traceability:: Implement HistoryManager with a stack of FormState objects.
        self._history: List[FormState] = []

    def save_state(self, memento: FormState) -> None:
        """Adds a Memento to the history stack."""
        self._history.append(memento)
        print(f"HISTORY: Saved Memento. Total snapshots: {len(self._history)}")

    def undo(self) -> FormState | None:
        """Retrieves the last saved Memento (the one *before* the current state)."""
        if len(self._history) < 2: # Need at least the initial state + one change
            print("HISTORY: Cannot undo. No previous state found.")
            return None

        # Pop the *current* state's snapshot, and return the one before it.
        # This is a common pattern in undo systems.
        self._history.pop() # Discard the Memento of the state we are about to leave
        return self._history[-1] # Return the Memento of the previous state

# --- Client Usage ---
if __name__ == "__main__":

    # 1. Initialization
    initial_data = {"name": "Alice", "email": "alice@example.com"}
    editor = FormEditor(initial_data)
    history = HistoryManager()

    # Save Initial State (Baseline)
    history.save_state(editor.createMemento())

    # 2. Change 1: Update name
    editor.update_field("name", "Bob")
    # Capture state before the next change (or after the current one, depending on design)
    history.save_state(editor.createMemento()) # Capture state "Bob"

    # 3. Change 2: Update email
    editor.update_field("email", "bob.smith@corp.com")
    history.save_state(editor.createMemento()) # Capture state "bob.smith"

    # 4. Change 3: Update name again
    editor.update_field("name", "Robert")
    history.save_state(editor.createMemento()) # Capture state "Robert"

    # --- Undo Operation ---
    print("\n=== Performing UNDO (Revert to Change 2) ===")

    # step_result:: Graceful recovery of previous state.
    memento_to_restore = history.undo()

    if memento_to_restore:
        editor.restoreMemento(memento_to_restore)
