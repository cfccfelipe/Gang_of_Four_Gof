from abc import ABC, abstractmethod

# --- Target Interface (What the New Platform Expects - Step 1) ---
class PaymentProcessor(ABC):
    """
    The interface expected by the new e-commerce platform.
    step_result:: Clear contract for integration.
    """
    @abstractmethod
    def authorize(self, amount: float) -> str:
        """Requests authorization for a given amount."""
        pass

    @abstractmethod
    def capture(self) -> str:
        """Captures the previously authorized funds."""
        pass

# --- Adaptee (The Legacy System) ---
class LegacyGateway:
    """
    The existing payment gateway with incompatible method names.
    We cannot modify this class.
    """
    def init_transaction(self, amount: float) -> str:
        """Legacy method to start a transaction."""
        print(f"LEGACY: Initiating transaction for ${amount:.2f}")
        return f"Auth_Code_LGC-{int(amount * 100)}"

    def finalize_payment(self, auth_code: str) -> str:
        """Legacy method to finalize (capture) the payment."""
        print(f"LEGACY: Finalizing payment using {auth_code}")
        return "SUCCESS"

# --- State Management (Internal to the Adapter) ---
class AdapterState:
    """Simple class to hold the internal authorization code for the Adapter."""
    auth_code: str = ""

# --- 2. The Adapter Class ---
class PaymentAdapter(PaymentProcessor):
    """
    The Adapter implements the Target interface and wraps the Adaptee (LegacyGateway).
    step_result:: Seamless translation between interfaces.
    """
    def __init__(self, legacy_gateway: LegacyGateway):
        self._legacy_gateway = legacy_gateway
        self._state = AdapterState() # Holds the state needed between calls

    def authorize(self, amount: float) -> str:
        """
        Translates 'authorize()' call to 'init_transaction()'.
        step_traceability:: Adapter implements the target interface and delegates calls.
        """
        print("ADAPTER: Translating authorize() to init_transaction()...")
        auth_code = self._legacy_gateway.init_transaction(amount)
        self._state.auth_code = auth_code
        return f"Authorization successful: {auth_code}"

    def capture(self) -> str:
        """
        Translates 'capture()' call to 'finalize_payment()', passing state data.
        step_traceability:: Ensure parameters and return types are correctly translated.
        """
        if not self._state.auth_code:
            return "ERROR: Cannot capture; authorization missing."

        print("ADAPTER: Translating capture() to finalize_payment()...")
        result = self._legacy_gateway.finalize_payment(self._state.auth_code)

        # Reset state after finalization
        self._state.auth_code = ""
        return f"Capture result: {result}"

# --- 3. Client Code Execution ---
if __name__ == "__main__":

    # Instantiate the Adaptee (Legacy)
    legacy_system = LegacyGateway()

    # Wrap the Adaptee with the Adapter
    # The client (new platform) only sees the PaymentProcessor interface.
    # step_traceability:: Replace direct legacy calls with Adapter usage.
    payment_processor: PaymentProcessor = PaymentAdapter(legacy_system)

    print("--- Client Scenario: Processing a $120.50 Order ---")

    # 1. Authorize the transaction using the expected interface
    auth_response = payment_processor.authorize(120.50)
    print(f"PLATFORM: Received Auth Response: {auth_response}")

    print("-" * 20)

    # 2. Capture the funds using the expected interface
    capture_response = payment_processor.capture()
    print(f"PLATFORM: Received Capture Response: {capture_response}")

    print("\n--- Validation: Attempting Capture without Auth ---")
    # This demonstrates consistent behavior and error handling (Step 4)
    payment_processor_b = PaymentAdapter(LegacyGateway())
    print(payment_processor_b.capture())
