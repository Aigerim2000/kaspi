from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


class InsufficientFundsError(ValueError):
    print('Your account has insufficient funds')

@dataclass
class Transaction:
    id_: UUID
    source_account: UUID
    target_account: UUID
    balance_brutto: Decimal
    balance_netto: Decimal
    currency: str
    status: str


    def confirm(self)->None:
            if self.send_account.balance<self.amount:
                raise InsufficientFundsError
