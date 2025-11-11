from abc import ABC, abstractmethod

# --- Step 1: Define Common Interface (Subject) ---
class DocumentViewer(ABC):
    """
    Defines the common interface for real and proxy objects.
    step_result:: Unified contract for client interaction.
    """
    @abstractmethod
    def display(self) -> None:
        """Displays the document content."""
        pass

# --- 2. The Real Subject ---
class RealDocument(DocumentViewer):
    """
    The actual object that performs the expensive operation (loading and rendering).
    step_result:: Encapsulated core behavior.
    """
    def __init__(self, filename: str):
        self._filename = filename
        # Simulates a slow, expensive operation
        print(f"REAL: ⏳ Loading file '{filename}' from remote server...")

    def display(self) -> None:
        print(f"REAL: ✅ Rendering full content of '{self._filename}'.")

# --- 3. The Proxy ---
class ProxyDocument(DocumentViewer):
    """
    The Proxy controls access to the RealDocument, adding control and efficiency features.
    step_result:: Controlled, efficient access to the real object.
    """
    def __init__(self, filename: str, user_role: str):
        self._filename = filename
        self._user_role = user_role
        self._real_document: RealDocument  # Set to None for lazy loading
        print(f"PROXY: Document link established for {user_role}.")

    # --- Access Control Logic ---
    def _check_access(self) -> bool:
        """Checks if the current user role has permission to view the document."""
        # step_traceability:: Checks permissions.
        if self._user_role in ["ADMIN", "PREMIUM"]:
            print("PROXY: 👍 Access Granted based on role.")
            return True
        print(f"PROXY: 🛑 Access DENIED for role {self._user_role}.")
        return False

    # --- Lazy Loading Logic ---
    def _lazy_load(self) -> None:
        """Loads the RealDocument only when display() is called for the first time."""
        # step_traceability:: Loads RealDocument only when needed.
        if self._real_document is None:
            self._real_document = RealDocument(self._filename)
            print("PROXY: ⚡ Real document instance created (Lazy Load complete).")

    # --- Delegation Method ---
    def display(self) -> None:
        if self._check_access():
            self._lazy_load()

            # Delegation to the RealDocument
            self._real_document.display()
        else:
            print(f"PROXY: Display failed. User '{self._user_role}' lacks permission.")

# --- 4. Client Usage ---
def client_code(viewer: DocumentViewer, user: str) -> None:
    """
    Client interacts only with the DocumentViewer interface.
    step_result:: Transparent delegation with added control.
    """
    print(f"\n--- CLIENT: Attempting to view document as user: {user} ---")
    viewer.display()
    print("--------------------------------------------------")

if __name__ == "__main__":

    # The expensive document file
    pdf_file = "Large_Financial_Report.pdf"

    # 1. Setup Proxy for an Unauthorized user
    # Note: The RealDocument is NOT loaded yet.
    unauthorized_proxy = ProxyDocument(pdf_file, user_role="BASIC")
    client_code(unauthorized_proxy, "BASIC")

    # 2. Setup Proxy for an Authorized user (First time viewing)
    authorized_proxy = ProxyDocument(pdf_file, user_role="PREMIUM")

    # The RealDocument will be loaded *now* (lazy loading)
    client_code(authorized_proxy, "PREMIUM (First View)")

    # 3. Authorized user viewing again (Demonstrates caching/efficiency)
    # The RealDocument is already instantiated within the Proxy, so no slow loading occurs.
    client_code(authorized_proxy, "PREMIUM (Second View)")
