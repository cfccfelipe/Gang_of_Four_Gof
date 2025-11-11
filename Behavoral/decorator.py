from abc import ABC, abstractmethod
from typing import Dict, Any

# --- Step 1: Define Base Interface (Component) ---
class Notifier(ABC):
    """
    Defines the contract for all notification behaviors.
    step_result:: Unified contract for all notification behaviors.
    """
    @abstractmethod
    def send(self, message: str) -> None:
        pass

# --- Step 2: Implement Base Components (Concrete Components) ---
class EmailNotifier(Notifier):
    """Core functionality: Sends a message via Email."""
    def send(self, message: str) -> None:
        """step_traceability:: Implement Notifier."""
        print(f"CORE: Sending EMAIL: '{message}'")

class SMSNotifier(Notifier):
    """Core functionality: Sends a message via SMS."""
    def send(self, message: str) -> None:
        """step_traceability:: Implement Notifier."""
        print(f"CORE: Sending SMS: '{message}'")

# --- Step 3: Create Decorator Classes (Decorator Base) ---
class NotifierDecorator(Notifier, ABC):
    """
    Base class for all decorators. Implements the Notifier interface and holds a reference.
    """
    def __init__(self, wrapped_notifier: Notifier):
        self._wrapped_notifier = wrapped_notifier

    # Delegates the core functionality to the wrapped object
    @abstractmethod
    def send(self, message: str) -> None:
        self._wrapped_notifier.send(message)

# --- Concrete Decorators ---

class LoggingNotifier(NotifierDecorator):
    """Adds logging capability before sending."""
    def send(self, message: str) -> None:
        """
        Adds logging behavior before delegating to the next component.
        step_traceability:: Wraps a Notifier and adds behavior before/after delegation.
        """
        print(f"DECORATOR: 📝 Logging message content: '{message[:20]}...'")
        super().send(message)
        print("DECORATOR: 📝 Logging successful transmission status.")

class EncryptedNotifier(NotifierDecorator):
    """Adds encryption capability before sending."""
    def _encrypt(self, message: str) -> str:
        """Simulates an encryption process."""
        return f"[ENCRYPTED({message})]"

    def send(self, message: str) -> None:
        """
        Adds encryption behavior before delegating.
        """
        encrypted_message = self._encrypt(message)
        print("DECORATOR: 🔒 Encrypting message.")
        super().send(encrypted_message)
        print("DECORATOR: 🔒 Encryption layer complete.")

class RetryNotifier(NotifierDecorator):
    """Adds retry logic around the send operation."""
    def send(self, message: str) -> None:
        """
        Adds retry logic around the delegation.
        """
        print("DECORATOR: 🔄 Initiating send attempt (with retry logic).")
        try:
            super().send(message)
            print("DECORATOR: 🔄 Send successful on first attempt.")
        except Exception as e:
            # Simulate retry logic here
            print(f"DECORATOR: 🔄 Send failed, initiating retry... Error: {e}")
            # In a real app, logic would re-call super().send(message)

# --- Step 4 & 5: Runtime Composition and Validation ---
if __name__ == "__main__":

    test_message = "Your account balance has been updated to $500.00."

    # 1. Simple Email (Base Component)
    print("--- 1. Base Email Notification ---")
    base_email = EmailNotifier()
    base_email.send(test_message)

    # 2. Email with Logging (One Decorator)
    print("\n--- 2. Email + Logging ---")
    # step_traceability:: Wrap EmailNotifier with LoggingNotifier.
    logged_email = LoggingNotifier(EmailNotifier())
    logged_email.send(test_message)

    # 3. SMS with Encryption and Retry (Stacked Decorators)
    print("\n--- 3. SMS + Retry + Encryption ---")
    # Composition: Encryption wraps Retry, Retry wraps SMS.
    # The order matters: Retry will handle the result of Encryption + SMS.
    # step_result:: Flexible, dynamic behavior composition.

    # 📝 Logic Stack: SMS -> RetryNotifier -> EncryptedNotifier
    # The message is encrypted LAST, but the logic flows from outer to inner.
    retry_sms = RetryNotifier(SMSNotifier()) # SMS is the core

    # EncryptNotifier wraps the entire Retry/SMS block
    secure_sms_with_retry = EncryptedNotifier(retry_sms)

    secure_sms_with_retry.send(test_message)

    # 4. Email with Logging AND Encryption (Validation of Order)
    print("\n--- 4. Email + Logging + Encryption (Order Test) ---")

    # Composition: Logging wraps Email. Encryption wraps Logging.
    # LOGIC FLOW: Encryption -> Logging -> Email
    # The message is encrypted FIRST, then logged, then sent.

    # This demonstrates LIFO (Last In, First Out) processing for pre-send logic:
    # 1. Encryption decorator receives the message.
    # 2. Encryption calls Logging's send() with the ENCRYPTED message.
    # 3. Logging calls Email's send() with the ENCRYPTED message.

    # step_result:: Reliable, predictable behavior across compositions.
    logged_email_core = LoggingNotifier(EmailNotifier())
    secure_logged_email = EncryptedNotifier(logged_email_core)

    secure_logged_email.send(test_message)
