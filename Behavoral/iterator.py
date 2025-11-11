from abc import ABC, abstractmethod
from typing import List, Any, Optional

# --- Step 1: Define Iterator Interface ---
class Iterator(ABC):
    """
    Defines the contract for traversal.
    step_result:: Standardized traversal contract.
    """
    @abstractmethod
    def has_next(self) -> bool:
        """Checks if there are more elements."""
        pass

    @abstractmethod
    def next_item(self) -> Any:
        """Returns the next element in the sequence."""
        pass

# --- 2. Concrete Iterators (Strategies) ---
class ForwardIterator(Iterator):
    """Iterates through the list elements from start to end."""
    def __init__(self, collection: List[Any]):
        self._collection = collection
        self._position = 0
        # step_result:: Encapsulated traversal logic.

    def has_next(self) -> bool:
        return self._position < len(self._collection)

    def next_item(self) -> Any:
        if self.has_next():
            item = self._collection[self._position]
            self._position += 1
            return item
        raise StopIteration("Iteration finished.")

class ReverseIterator(Iterator):
    """Iterates through the list elements from end to start."""
    def __init__(self, collection: List[Any]):
        self._collection = collection
        # Start at the last index
        self._position = len(self._collection) - 1

    def has_next(self) -> bool:
        return self._position >= 0

    def next_item(self) -> Any:
        if self.has_next():
            item = self._collection[self._position]
            self._position -= 1
            return item
        raise StopIteration("Iteration finished.")

# --- The Aggregate (The Collection) ---
class CustomCollection:
    """
    The collection (Aggregate) that creates Iterator instances.
    """
    def __init__(self, items: List[Any]):
        self._items = items
        print(f"COLLECTION: Data loaded: {self._items}")

    def get_items(self) -> List[Any]:
        return self._items

    # --- Step 3: Add createIterator() method ---
    def create_forward_iterator(self) -> Iterator:
        """
        Returns an instance of the forward traversal strategy.
        step_result:: Decoupled traversal from collection logic.
        """
        return ForwardIterator(self._items)

    def create_reverse_iterator(self) -> Iterator:
        """Returns an instance of the reverse traversal strategy."""
        return ReverseIterator(self._items)

# --- 4. Client Usage ---
def client_code(collection: CustomCollection):
    """Client code uses the standardized Iterator interface."""

    # --- Forward Traversal ---
    print("\n--- FORWARD TRAVERSAL (Standard) ---")
    forward_iterator = collection.create_forward_iterator()

    # step_traceability:: Loop through elements using while (iterator.hasNext()) pattern.
    output = []
    while forward_iterator.has_next():
        output.append(forward_iterator.next_item())
    print(f"Client Output: {output}")

    # --- Reverse Traversal ---
    print("\n--- REVERSE TRAVERSAL ---")
    reverse_iterator = collection.create_reverse_iterator()

    output = []
    while reverse_iterator.has_next():
        output.append(reverse_iterator.next_item())
    # step_result:: Clean, consistent iteration across collections.
    print(f"Client Output: {output}")


if __name__ == "__main__":

    data = ["Alpha", "Beta", "Gamma", "Delta"]
    my_collection = CustomCollection(data)

    client_code(my_collection)
