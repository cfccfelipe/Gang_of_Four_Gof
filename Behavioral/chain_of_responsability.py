from abc import ABC, abstractmethod
from typing import Optional, Any

# Define the structure for a support request
class SupportRequest:
    def __init__(self, topic: str, description: str, priority: str):
        self.topic = topic
        self.description = description
        self.priority = priority

    def __str__(self):
        return f"[{self.priority} Priority] Topic: {self.topic}, Desc: '{self.description[:20]}...'"

# --- Step 1: Define Handler Interface ---
class SupportHandler(ABC):
    """
    Defines the contract for chaining and processing requests.
    step_result:: Unified contract for chaining and processing.
    """
    def __init__(self):
        self._next_handler: Optional[SupportHandler] = None

    def set_next(self, handler: 'SupportHandler') -> 'SupportHandler':
        """step_traceability:: Include setNext(handler) and handle(request)."""
        self._next_handler = handler
        return handler # Return the handler for easy chaining

    @abstractmethod
    def handle(self, request: SupportRequest) -> Optional[str]:
        """Processes the request or delegates to the next handler."""
        pass

    def _pass_to_next(self, request: SupportRequest) -> Optional[str]:
        """Helper method to delegate the request."""
        if self._next_handler:
            print(f"HANDLER: ➡️ {self.__class__.__name__} cannot handle. Passing to {self._next_handler.__class__.__name__}.")
            return self._next_handler.handle(request)

        # End of the chain
        print("HANDLER: 🛑 End of chain reached. Request remains unhandled.")
        return None

# --- 2. Concrete Handlers ---
class BillingHandler(SupportHandler):
    """Handles requests related to billing and payments."""
    def handle(self, request: SupportRequest) -> Optional[str]:
        if request.topic == "billing":
            # step_result:: Modular, focused request processors.
            print(f"HANDLER: 💰 {self.__class__.__name__} processed: {request}")
            return f"Processed Billing Request for {request.description}"
        else:
            return self._pass_to_next(request)

class TechHandler(SupportHandler):
    """Handles requests related to technical support and bugs."""
    def handle(self, request: SupportRequest) -> Optional[str]:
        if request.topic == "technical":
            print(f"HANDLER: 💻 {self.__class__.__name__} processed: {request}")
            return f"Processed Technical Request for {request.description}"
        else:
            return self._pass_to_next(request)

class LegalHandler(SupportHandler):
    """Handles requests related to legal terms and compliance."""
    def handle(self, request: SupportRequest) -> Optional[str]:
        if request.topic == "legal":
            print(f"HANDLER: ⚖️ {self.__class__.__name__} processed: {request}")
            return f"Processed Legal Request for {request.description}"
        else:
            return self._pass_to_next(request)

# --- 3. Configuration and Client Usage ---
if __name__ == "__main__":

    # Instantiate Handlers
    billing = BillingHandler()
    tech = TechHandler()
    legal = LegalHandler()

    # --- Step 3: Configure the chain at runtime ---
    # Chain setup: Billing -> Tech -> Legal
    # step_traceability:: Link handlers using setNext() to form a sequence.
    billing.set_next(tech).set_next(legal)

    # 1. Billing Request (Handled by the first link)
    request_1 = SupportRequest("billing", "Why was I charged twice this month?", "HIGH")
    print(f"\nCLIENT: Submitting Request 1: {request_1.topic}")
    billing.handle(request_1)

    # 2. Tech Request (Passed through Billing, handled by Tech)
    request_2 = SupportRequest("technical", "My service is down and shows error 404.", "CRITICAL")
    print(f"\nCLIENT: Submitting Request 2: {request_2.topic}")
    # step_traceability:: Call handle(request) on the first handler.
    billing.handle(request_2)

    # 3. Legal Request (Passed through Billing and Tech, handled by Legal)
    request_3 = SupportRequest("legal", "What are the terms for data retention?", "MEDIUM")
    print(f"\nCLIENT: Submitting Request 3: {request_3.topic}")
    billing.handle(request_3)

    # 4. Unhandled Request (Goes to the end of the chain)
    request_4 = SupportRequest("general", "Can I get a new feature added?", "LOW")
    print(f"\nCLIENT: Submitting Request 4: {request_4.topic}")
    billing.handle(request_4)
