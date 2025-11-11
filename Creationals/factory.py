from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

# --- 1. Product Interface and Concrete Classes (Simplified) ---

class Transaction(ABC):
    def __init__(self, amount: float, source: str, destination: str):
        self.amount = amount
        self.source = source
        self.destination = destination
    @abstractmethod
    def process(self) -> str:
        pass

class CreditTransaction(Transaction):
    def process(self) -> str:
        return f"Credit Tx for ${self.amount:.2f} processed."

class CryptoTransaction(Transaction):
    def __init__(self, amount: float, source: str, destination: str, asset: str):
        super().__init__(amount, source, destination)
        self.asset = asset
    def process(self) -> str:
        return f"Crypto Tx of {self.amount} {self.asset} sent."

# --- 2. The Corrected Factory ---

class TransactionFactory:
    """Centralized factory with strict type handling for mypy compatibility."""
    @staticmethod
    def create_transaction(tx_type: str, data: Dict[str, Any]) -> Optional[Transaction]:

        # 1. Retrieve raw data
        amount = data.get('amount')
        source = data.get('source_id')
        destination = data.get('dest_id')

        # 2. Validation and Type Narrowing

        # Check if mandatory string/object fields are missing
        if not all([source, destination]):
            print("ERROR: Source or Destination missing.")
            return None

        # Check if the float field is missing (None) and handle type conversion safely
        if amount is None:
            print("ERROR: Amount is missing.")
            return None

        # 3. Instantiate the correct object

        if tx_type.upper() == 'CREDIT':
            return CreditTransaction(amount, str(source), str(destination))

        elif tx_type.upper() == 'CRYPTO':
            asset = data.get('crypto_asset')
            if not isinstance(asset, str):
                 # This also handles asset being None
                 print("ERROR: Crypto requires 'crypto_asset' as a string.")
                 return None
            return CryptoTransaction(amount, str(source), str(destination), asset)

        else:
            print(f"ERROR: Unknown transaction type '{tx_type}'.")
            return None

# --- 3. Client Code (Simple Use Case) ---

if __name__ == "__main__":

    # Correct data for a Crypto transaction
    crypto_data = {'amount': 0.05, 'source_id': 'Wallet-B', 'dest_id': 'Exchange-Y', 'crypto_asset': 'ETH'}

    # Client only interacts with the Factory
    crypto_tx = TransactionFactory.create_transaction('CRYPTO', crypto_data)

    if crypto_tx:
        print(crypto_tx.process())

    # Example of invalid data (missing destination) handled by the Factory
    invalid_data = {'amount': 100.00, 'source_id': 'User-A'}
    invalid_tx = TransactionFactory.create_transaction('CREDIT', invalid_data)
