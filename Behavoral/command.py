from abc import ABC, abstractmethod
from typing import List, Optional

# --- The Receiver (The object that knows how to perform the operations) ---
class TextEditor:
    """The component that holds the application state."""
    def __init__(self, content: str = ""):
        self.content = content
        print(f"EDITOR: Initial content: '{self.content}'")

    def insert_text(self, text: str, position: int) -> None:
        """Performs the insertion."""
        self.content = self.content[:position] + text + self.content[position:]

    def delete_text(self, start: int, end: int) -> str:
        """Performs the deletion and returns the deleted text."""
        deleted_text = self.content[start:end]
        self.content = self.content[:start] + self.content[end:]
        return deleted_text

# --- Step 1: Define Command Interface ---
class Command(ABC):
    """
    Defines the contract for all actions.
    step_result:: Unified contract for encapsulated actions.
    """
    @abstractmethod
    def execute(self) -> None:
        """Executes the action."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Reverses the action."""
        pass

# --- 2. Concrete Command Classes ---

class InsertTextCommand(Command):
    """
    Command to insert text. Undo requires deleting the inserted text.
    step_result:: Modular, reversible action logic.
    """
    def __init__(self, editor: TextEditor, text: str, position: int):
        self._editor = editor
        self._text = text
        self._position = position

    def execute(self) -> None:
        self._editor.insert_text(self._text, self._position)
        print(f"COMMAND: Executed Insert('{self._text}') -> '{self._editor.content}'")

    def undo(self) -> None:
        # Reversal: Delete the text that was just inserted
        self._editor.delete_text(self._position, self._position + len(self._text))
        print(f"COMMAND: Undone Insert -> '{self._editor.content}'")


class DeleteTextCommand(Command):
    """
    Command to delete text. Undo requires re-inserting the deleted text.
    """
    def __init__(self, editor: TextEditor, start: int, end: int):
        self._editor = editor
        self._start = start
        self._end = end
        self._deleted_text: Optional[str] = None # Stores state needed for undo

    def execute(self) -> None:
        # Must save the deleted state for undo
        self._deleted_text = self._editor.delete_text(self._start, self._end)
        print(f"COMMAND: Executed Delete('{self._deleted_text}') -> '{self._editor.content}'")

    def undo(self) -> None:
        # Reversal: Insert the previously deleted text back
        if self._deleted_text is not None:
            self._editor.insert_text(self._deleted_text, self._start)
            print(f"COMMAND: Undone Delete -> '{self._editor.content}'")

# --- 3. The Invoker (History Manager) ---
class CommandInvoker:
    """
    Manages the command execution and history stacks.
    step_result:: Centralized control and traceability of actions.
    """
    def __init__(self):
        # step_traceability:: History stack for executed commands.
        self._history: List[Command] = []
        self._redo_stack: List[Command] = []

    def execute_command(self, command: Command) -> None:
        """Executes a command and stores it in history."""
        command.execute()

        # Step 4: Store commands in history
        self._history.append(command)
        self._redo_stack.clear() # Clear redo stack upon any new action
        print(f"INVOKER: Command executed and saved to history. History size: {len(self._history)}")

    def undo(self) -> None:
        """
        Reverses the last action by popping from the history stack.
        step_traceability:: Pop or replay commands from the stack as needed.
        """
        if not self._history:
            print("INVOKER: Cannot undo. History is empty.")
            return

        command = self._history.pop()
        command.undo()
        self._redo_stack.append(command)
        print(f"INVOKER: Undo successful. History size: {len(self._history)}. Redo size: {len(self._redo_stack)}")

    def redo(self) -> None:
        """Reapplies the last undone action."""
        if not self._redo_stack:
            print("INVOKER: Cannot redo. Redo stack is empty.")
            return

        command = self._redo_stack.pop()
        command.execute()
        self._history.append(command)
        print(f"INVOKER: Redo successful. History size: {len(self._history)}. Redo size: {len(self._redo_stack)}")

# --- Client Usage ---
if __name__ == "__main__":

    editor = TextEditor(content="The quick brown fox.")
    invoker = CommandInvoker()

    # 1. Execute Command: Insert text
    insert_cmd_1 = InsertTextCommand(editor, "lazy ", 4) # Insert at position 4
    invoker.execute_command(insert_cmd_1)

    # 2. Execute Command: Delete text
    delete_cmd_1 = DeleteTextCommand(editor, 14, 20) # Delete "brown "
    invoker.execute_command(delete_cmd_1)

    # --- Undo Operations ---
    print("\n--- UNDO 1 (Reverses Delete) ---")
    invoker.undo() # Undoes the Delete, re-inserting "brown "

    print("\n--- UNDO 2 (Reverses Insert) ---")
    invoker.undo() # Undoes the Insert, deleting "lazy "

    # --- Redo Operations ---
    # step_result:: Flexible, user-driven control over application state.
    print("\n--- REDO 1 (Reapplies Insert) ---")
    invoker.redo()

    print("\n--- REDO 2 (Reapplies Delete) ---")
    invoker.redo()
