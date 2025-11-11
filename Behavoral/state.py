from abc import ABC, abstractmethod

# --- Step 1: Define State Interface ---
class PlayerState(ABC):
    """
    Defines the contract for state-driven behavior.
    step_result:: Unified contract for state-driven behavior.
    """
    @abstractmethod
    def play(self, player: 'MediaPlayers') -> None:
        pass

    @abstractmethod
    def pause(self, player: 'MediaPlayers') -> None:
        pass

    @abstractmethod
    def stop(self, player: 'MediaPlayers') -> None:
        pass

# --- 3. The Context Class (The Player) ---
class MediaPlayers:
    """
    The Context holds the current state and delegates all state-dependent requests.
    step_result:: Dynamic behavior based on internal state.
    """
    def __init__(self):
        # Initialize in the default state (Stopped)
        self._state: PlayerState = StoppedState()
        print(f"PLAYER: Initialized in {type(self._state).__name__}.")

    @property
    def state(self) -> PlayerState:
        return self._state

    def set_state(self, new_state: PlayerState) -> None:
        """
        Allows state transition.
        step_traceability:: Use setState() to switch between states.
        """
        self._state = new_state
        print(f"PLAYER: State transitioned to {type(new_state).__name__}.")

    # Delegation methods (client calls these)
    def press_play(self) -> None:
        self._state.play(self)

    def press_pause(self) -> None:
        self._state.pause(self)

    def press_stop(self) -> None:
        self._state.stop(self)

# --- 2. Concrete State Classes ---

class StoppedState(PlayerState):
    """
    Behavior when the player is stopped.
    step_result:: Modular, encapsulated behavior per state.
    """
    def play(self, player: MediaPlayers) -> None:
        # Action: Start playing
        print("STATE: ▶️ Starting playback from the beginning.")
        player.set_state(PlayingState())

    def pause(self, player: MediaPlayers) -> None:
        # Action: Ignore
        print("STATE: ⚠️ Cannot pause when already stopped.")

    def stop(self, player: MediaPlayers) -> None:
        # Action: Ignore
        print("STATE: 🛑 Already stopped.")


class PlayingState(PlayerState):
    """Behavior when the player is playing."""
    def play(self, player: MediaPlayers) -> None:
        # Action: Ignore
        print("STATE: ⚠️ Already playing.")

    def pause(self, player: MediaPlayers) -> None:
        # Action: Pause and switch state
        print("STATE: ⏸️ Pausing playback.")
        player.set_state(PausedState())

    def stop(self, player: MediaPlayers) -> None:
        # Action: Stop and switch state
        print("STATE: ⏹️ Stopping playback. Rewinding.")
        player.set_state(StoppedState())


class PausedState(PlayerState):
    """Behavior when the player is paused."""
    def play(self, player: MediaPlayers) -> None:
        # Action: Resume playing
        print("STATE: ▶️ Resuming playback from current position.")
        player.set_state(PlayingState())

    def pause(self, player: MediaPlayers) -> None:
        # Action: Ignore
        print("STATE: ⚠️ Already paused.")

    def stop(self, player: MediaPlayers) -> None:
        # Action: Stop and switch state
        print("STATE: ⏹️ Stopping playback. Rewinding.")
        player.set_state(StoppedState())

# --- 5. Client Usage and Validation ---
if __name__ == "__main__":

    player = MediaPlayers()

    # Initial State: StoppedState

    # 1. Stopped -> Play -> PlayingState
    print("\n--- SCENARIO 1: Go from Stopped to Playing ---")
    player.press_play()

    # 2. Playing -> Pause -> PausedState
    print("\n--- SCENARIO 2: Go from Playing to Paused ---")
    player.press_pause()

    # 3. Paused -> Play -> PlayingState
    print("\n--- SCENARIO 3: Go from Paused back to Playing ---")
    player.press_play()

    # 4. Playing -> Stop -> StoppedState
    print("\n--- SCENARIO 4: Go from Playing to Stopped ---")
    player.press_stop()

    # 5. Validation of invalid actions
    # step_traceability:: Test method calls in different states to ensure correct delegation.
    print("\n--- SCENARIO 5: Invalid Actions (State Protection) ---")
    player.press_pause() # Should not pause from Stopped
    player.press_stop()  # Should not stop from Stopped
    # step_result:: Reliable, predictable state-dependent logic.
