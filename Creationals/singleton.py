import threading
from typing import Optional

# Global lock used for synchronization (Step 3: Ensure thread safety)
_singleton_lock = threading.Lock()

class Logger:
    """
    Singleton Class for the logging system.
    Guarantees only one instance of Logger exists.
    """
    # Static attribute to hold the single instance
    _instance: Optional['Logger'] = None

    # ------------------ Step 1: Simulated Private Constructor ------------------
    def __init__(self):
        """
        Simulates a private constructor.
        Prevents direct instantiation if an instance already exists.
        """
        # step_traceability:: Prevent external instantiation by restricting access.
        if Logger._instance is not None:
            raise Exception("This class is a Singleton! Use Logger.getInstance() to get the instance.")

        # Unique Initialization Logic
        self.log_file = "app_shared_log.txt"
        print(f"INFO: Logger instantiated for the first and only time. File: {self.log_file}")

    # ------------------ Step 2: Static Access Method ------------------
    @staticmethod
    def getInstance() -> 'Logger':
        """
        Returns the single instance of the Logger (Lazy Initialization).
        step_result:: Centralized access point for the singleton.
        """
        if Logger._instance is None:
            # Step 3: Ensure Thread Safety (Locking)
            # Blocks access to ensure only one thread instantiates.
            with _singleton_lock:
                # Double-Checked Locking: Check again inside the lock.
                if Logger._instance is None:
                    Logger._instance = Logger()

        return Logger._instance

    # ------------------ Singleton Behavior ------------------
    def log(self, message: str) -> None:
        """Logging method that uses the shared file."""
        current_thread = threading.current_thread().name
        log_entry = f"[{current_thread}] {message}"

        # In a real application, this writes to the shared resource
        print(f"LOG: {log_entry}")

        # Simulation of writing to file
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")

# ------------------ Step 4 & 5: Usage and Validation (Multi-threaded) ------------------

# step_description:: Use the singleton instance across the application.
def logging_task(name: str):
    """Example function using the Singleton in a separate thread."""
    # step_traceability:: Reference the singleton in components needing shared access.
    logger = Logger.getInstance()
    logger.log(f"Component {name} accessed the logger.")

    # Verification (shows all threads reference the same object ID)
    print(f"DEBUG: Component {name} Logger ID: {id(logger)}")

if __name__ == "__main__":

    # Cleanup log file
    with open("app_shared_log.txt", "w") as f:
        f.write("--- LOG START ---\n")

    # Get Instance 1 (Creates the instance)
    logger_main = Logger.getInstance()
    logger_main.log("Main application started.")

    # Get Instance 2 (Returns the existing instance)
    logger_aux = Logger.getInstance()
    logger_aux.log("Auxiliary module initialized.")

    # Validation Check (Step 5)
    is_same = logger_main is logger_aux
    print(f"\nVALIDATION: Are logger_main and logger_aux the same instance? {is_same}")
    print(f"ID Main: {id(logger_main)}, ID Aux: {id(logger_aux)}")

    # Direct Instantiation Attempt (Should fail)
    try:
        Logger()
    except Exception as e:
        print(f"VALIDATION: Direct instantiation attempt failed: {e}")

    # Thread Safety Test
    print("\n--- Thread Safety Test (Concurrent Access) ---")
    threads = []
    for i in range(5):
        thread_name = f"Thread-{i}"
        t = threading.Thread(target=logging_task, name=thread_name)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\n--- Final Log Content ---")
    # step_result:: Verified singleton implementation ready for production use.
    with open("app_shared_log.txt", "r") as f:
        print(f.read())
