from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

# --- Forward Declaration/Base Class for Participants ---
class Participant(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def receive(self, sender: str, message: str) -> None:
        """Receives a message."""
        pass

# --- Step 1: Define Mediator Interface ---
class ChatMediator(ABC):
    """
    Defines the contract for communication coordination.
    step_result:: Centralized contract for message routing.
    """
    @abstractmethod
    def register_participant(self, participant: Participant, uid: str) -> None:
        pass

    @abstractmethod
    def send_message(self, sender_id: str, receiver_id: str, message: str) -> None:
        pass

# --- 2. Concrete Mediator Logic ---
class ConcreteChatMediator(ChatMediator):
    """
    Handles message routing, filtering, and logging.
    step_result:: Encapsulated coordination and filtering.
    """
    def __init__(self):
        # Internal map for routing
        self._participants: Dict[str, Participant] = {}

    # Step 3 & 4: Registration
    def register_participant(self, participant: Participant, uid: str) -> None:
        """
        Adds a component to the routing map.
        step_result:: Structured communication network.
        """
        if uid in self._participants:
            print(f"MEDIATOR: ⚠️ UID {uid} already registered. Skipping.")
            return
        self._participants[uid] = participant
        print(f"MEDIATOR: ✅ Registered {participant.name} with ID: {uid}")

    def send_message(self, sender_id: str, receiver_id: str, message: str) -> None:
        """
        Handles routing, logging, and filtering.
        step_traceability:: Add hooks to monitor traffic and apply business rules.
        """
        sender = self._participants.get(sender_id)

        if not sender:
            print(f"MEDIATOR: ❌ Error: Sender ID {sender_id} not found.")
            return

        print(f"\nMEDIATOR: ➡️ Logging traffic: {sender.name} to {receiver_id}...")

        # Look up receiver
        receiver = self._participants.get(receiver_id)

        if receiver:
            # Step 5: Extend mediator (Simple filtering example)
            if "spam" in message.lower():
                print("MEDIATOR: 🛑 Filtered message: Contains forbidden words.")
                return

            # Delegate message delivery
            receiver.receive(sender.name, message)
        else:
            print(f"MEDIATOR: ❌ Error: Receiver ID {receiver_id} not found.")

# --- 3. Concrete Participants (Components) ---
class User(Participant):
    """Component for individual users."""
    def __init__(self, name: str, uid: str, mediator: ChatMediator):
        super().__init__(name)
        self._mediator = mediator
        mediator.register_participant(self, uid)

    def send(self, receiver_id: str, message: str) -> None:
        """Calls the mediator instead of talking directly to the receiver."""
        self._mediator.send_message(self.name, receiver_id, message)

    def receive(self, sender: str, message: str) -> None:
        print(f"USER ({self.name}): Received message from {sender}: '{message}'")

class Group(Participant):
    """Component for group chat (simplified receiver)."""
    def receive(self, sender: str, message: str) -> None:
        print(f"GROUP ({self.name}): Broadcasted message from {sender}: '{message}'")

class Bot(Participant):
    """Component for a bot (simplified receiver)."""
    def receive(self, sender: str, message: str) -> None:
        print(f"BOT ({self.name}): New input from {sender}: '{message}'. Processing response...")
        # In a real system, the bot would then use the mediator to send a response back.

# --- Client Usage ---
if __name__ == "__main__":

    chat_system = ConcreteChatMediator()

    # 1. Register Participants
    user_alice = User("Alice", "alice_id", chat_system)
    user_bob = User("Bob", "bob_id", chat_system)

    # Manually register Group and Bot (simplification)
    chat_system.register_participant(Group("DevTeam"), "team_dev")
    chat_system.register_participant(Bot("SupportBot"), "bot_support")

    # 2. Alice sends a direct message to Bob
    user_alice.send("bob_id", "Hey Bob, are you ready for the meeting?")

    # 3. Bob sends a message to the Group
    user_bob.send("team_dev", "Team, the build passed successfully!")

    # 4. Alice sends a message to the Bot
    user_alice.send("bot_support", "I need help with billing.")

    # 5. Message gets filtered (Validation)
    print("\n--- Sending a Filtered Message ---")
    user_alice.send("bob_id", "Buy this product (spam!) now.")
