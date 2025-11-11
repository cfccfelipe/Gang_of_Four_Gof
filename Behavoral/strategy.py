from abc import ABC, abstractmethod
from typing import Dict, Any

# --- Step 1: Strategy Interface ---
class PricingStrategy(ABC):
    """
    Defines the contract for all pricing strategies.
    step_result:: Unified contract for interchangeable logic.
    """
    @abstractmethod
    def calculate_total(self, order: Dict[str, Any]) -> float:
        pass

# --- Step 2: Concrete Strategies ---
class FlatRateStrategy(PricingStrategy):
    """Flat rate: Applies a fixed cost regardless of order details."""
    FLAT_RATE = 20.00
    def calculate_total(self, order: Dict[str, Any]) -> float:
        print(f"-> Using Flat Rate Strategy: ${self.FLAT_RATE:.2f}")
        return self.FLAT_RATE

class TieredPricingStrategy(PricingStrategy):
    """Tiered pricing: Price per item changes based on total quantity."""
    def calculate_total(self, order: Dict[str, Any]) -> float:
        total_items: int = sum(item['quantity'] for item in order['items'])
        base_price_per_item = 10.00
        discount_per_item = 0.50 if total_items > 10 else 0.00
        final_price_per_item = base_price_per_item - discount_per_item
        total = total_items * final_price_per_item
        print(f"-> Using Tiered Strategy: {total_items} items @ ${final_price_per_item:.2f} each.")
        return total

# --- Step 3: Context Class ---
class BillingProcessor:
    """
    Context class that holds a reference to a Strategy and delegates the task.
    step_result:: Decoupled behavior selection.
    """
    def __init__(self, strategy: PricingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PricingStrategy):
        """Allows swapping the strategy at runtime."""
        self._strategy = strategy

    def process_billing(self, order: Dict[str, Any]) -> float:
        """Delegates calculation to the current strategy."""
        print(f"Processing bill for Customer ID: {order['customer_id']}...")
        final_total = self._strategy.calculate_total(order)
        return final_total

# --- Step 4 & 5: Runtime Execution and Validation ---
if __name__ == "__main__":
    order_A = {'customer_id': 'VIP-100', 'items': [{'price': 50.00, 'quantity': 1}]}
    order_B = {'customer_id': 'REG-200', 'items': [{'price': 10.00, 'quantity': 12}]}

    # Initialize with Flat Rate
    billing_system = BillingProcessor(FlatRateStrategy())
    billing_system.process_billing(order_A)

    # Swap Strategy at runtime
    print("\nSwapping Strategy...")
    billing_system.set_strategy(TieredPricingStrategy())
    billing_system.process_billing(order_B)
