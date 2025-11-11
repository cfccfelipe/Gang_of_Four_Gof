from abc import ABC, abstractmethod

class DataProcessor(ABC):
    """
    Abstract base class defining the algorithm's fixed structure.
    step_result:: Structured algorithm skeleton.
    """

    # --- The Template Method (Fixed Sequence - Step 1) ---
    def process(self) -> None:
        """
        The template method that defines the invariant sequence of steps:
        preProcess -> load -> transform -> validate -> export -> postProcess
        """
        print(f"\n--- Starting Pipeline for {self.__class__.__name__} ---")

        self.preProcess()  # Optional hook
        self.load()
        self.transform()
        self.validate()
        self.export()
        self.postProcess() # Optional hook

        print(f"--- Pipeline Finished ---")

    # --- Abstract Methods (Must be implemented by Subclasses - Step 2) ---
    @abstractmethod
    def load(self) -> None:
        """Loads data from the source."""
        pass

    @abstractmethod
    def transform(self) -> None:
        """Applies source-specific data transformations."""
        pass

    @abstractmethod
    def validate(self) -> None:
        """Performs data integrity checks."""
        pass

    @abstractmethod
    def export(self) -> None:
        """Writes the processed data to the destination."""
        pass
        # step_result:: Customizable hooks for subclasses.

    # --- Optional Hook Methods (Step 5) ---
    def preProcess(self) -> None:
        """Optional setup step before loading (Default implementation)."""
        print("HOOK: Initializing pipeline environment.")
        # step_result:: Flexible extension points for customization.

    def postProcess(self) -> None:
        """Optional cleanup step after export (Default implementation)."""
        print("HOOK: Cleaning up temporary resources.")

# ----------------------------------------------------------------------
# --- 2. Concrete Subclasses (Source-Specific Implementations) ---

class CSVProcessor(DataProcessor):
    """
    Concrete implementation for processing CSV files.
    step_result:: Source-specific behavior within a shared structure.
    """
    def load(self) -> None:
        print("CSV: Loading data from local CSV file into memory.")

    def transform(self) -> None:
        print("CSV: Converting string timestamps to datetime objects.")

    def validate(self) -> None:
        print("CSV: Ensuring all rows have 5 columns and no nulls.")

    def export(self) -> None:
        print("CSV: Exporting processed data to a SQL database table.")

    # Override an optional hook for custom setup
    def preProcess(self) -> None:
        print("CSV HOOK: Opening and locking the CSV file for exclusive read access.")


class APIProcessor(DataProcessor):
    """
    Concrete implementation for processing data from a REST API.
    """
    def load(self) -> None:
        print("API: Making authenticated GET request to external endpoint.")

    def transform(self) -> None:
        print("API: Flattening nested JSON structure and renaming keys (snake_case).")

    def validate(self) -> None:
        print("API: Validating response status code and schema against Pydantic model.")

    def export(self) -> None:
        print("API: Sending processed payload to internal microservice via POST request.")

    # Override an optional hook for custom cleanup
    def postProcess(self) -> None:
        print("API HOOK: Invalidating API cache for downstream systems.")

# ----------------------------------------------------------------------
# --- 3. Client Usage ---

if __name__ == "__main__":

    # 1. Process a CSV file
    csv_pipeline = CSVProcessor()
    # step_traceability:: Use processor.process() to execute the full pipeline.
    csv_pipeline.process()

    print("\n" + "=" * 50 + "\n")

    # 2. Process data from an API
    api_pipeline = APIProcessor()
    api_pipeline.process()
    # step_result:: Consistent execution flow across implementations.
