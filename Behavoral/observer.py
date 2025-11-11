from abc import ABC, abstractmethod
from typing import List, Any

# --- Step 3: Define Observer Interface ---
class Observer(ABC):
    """
    Defines the contract for classes that react to changes.
    step_result:: Unified contract for reactive behavior.
    """
    @abstractmethod
    def update(self, subject: Any) -> None:
        """Method called by the subject to notify of a change."""
        pass

# --- Step 1: Define Subject Interface ---
class Subject(ABC):
    """
    Defines the contract for managing observers.
    step_traceability:: Includes attach(observer), detach(observer), and notify().
    step_result:: Centralized subscription control.
    """
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        """Notifies all attached observers about an event."""
        pass

# --- Step 2: Implement Concrete Subject (Stock) ---
class Stock(Subject):
    """
    The concrete subject, tracking its price and notifying observers upon change.
    step_result:: Encapsulated state and notification trigger.
    """
    def __init__(self, symbol: str, initial_price: float):
        self._symbol: str = symbol
        self._price: float = initial_price
        self._observers: List[Observer] = []
        print(f"Stock {self._symbol} created. Initial price: ${self._price:.2f}")

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float):
        """
        State change method that triggers notification.
        step_traceability:: Call notify() after updating the subject’s state.
        """
        if new_price != self._price:
            print(f"\n--- STATE CHANGE: {self._symbol} to ${new_price:.2f} ---")
            self._price = new_price
            self.notify() # <-- Triggers notification
        else:
            print(f"{self._symbol} price unchanged.")

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"  > Observer {type(observer).__name__} attached.")

    def detach(self, observer: Observer) -> None:
        try:
            self._observers.remove(observer)
            print(f"  > Observer {type(observer).__name__} detached.")
        except ValueError:
            pass

    def notify(self) -> None:
        """step_result:: Real-time propagation of changes."""
        for observer in self._observers:
            observer.update(self)

# --- Step 4: Implement Concrete Observers ---
class PriceAlert(Observer):
    """Reacts to price changes to trigger threshold alerts."""
    def __init__(self, threshold: float):
        self._threshold = threshold

    def update(self, subject: Stock) -> None:
        if subject.price > self._threshold:
            print(f"  [ALERT] 🚨 {subject._symbol}: Price ${subject.price:.2f} exceeds threshold of ${self._threshold:.2f}!")

class AnalyticsModule(Observer):
    """Reacts to changes to log data and perform analysis."""
    def update(self, subject: Stock) -> None:
        print(f"  [ANALYTICS] 📊 {subject._symbol}: Logging new price ${subject.price:.2f} for analysis.")

class UIComponent(Observer):
    """Reacts to changes to update the user interface."""
    def update(self, subject: Stock) -> None:
        print(f"  [UI] 🖼️ {subject._symbol}: Updating widget with new price ${subject.price:.2f}.")

# --- Step 5: Test Workflow (Trigger Notifications) ---
if __name__ == "__main__":

    # 1. Create the Subject
    tesla_stock = Stock("TSLA", 250.00)

    # 2. Create the Observers
    ui_display = UIComponent()
    analytics_logger = AnalyticsModule()
    alert_system = PriceAlert(threshold=255.00) # Alert if it goes above 255

    # 3. Attach Observers (Subscription)
    tesla_stock.attach(ui_display)
    tesla_stock.attach(analytics_logger)
    tesla_stock.attach(alert_system)

    # --- Scenario 1: Price changes below threshold ---
    print("\n\n=== Scenario 1: Price goes up slightly ===")
    tesla_stock.price = 252.00 # Triggers notify()

    # --- Scenario 2: Price changes and exceeds threshold ---
    print("\n\n=== Scenario 2: Price exceeds threshold ===")
    tesla_stock.price = 260.00 # Triggers notify() and activates the Alert

    # 4. Detach an observer
    print("\n\n=== Scenario 3: Detaching Analytics ===")
    tesla_stock.detach(analytics_logger)
    tesla_stock.price = 265.00 # Analytics will no longer receive this update
