"""Project domain entities."""
import datetime
import decimal
import typing
import uuid

import pydantic


TgID = typing.NewType('TgID', int)
StockName = typing.NewType('StockName', str)


class User(pydantic.BaseModel):
    """User."""

    tg_id: TgID
    tg_username: typing.Optional[str]
    tg_first_name: typing.Optional[str]
    tg_last_name: typing.Optional[str]

    voting_state: typing.Optional[str]
    voting_stocks: typing.List[str] = pydantic.Field(default_factory=list)
    voting_steaks: int = 0

    is_blocked: bool = False

    @property
    def pk(self) -> str:
        """Return primary key."""
        return str(self.tg_id)

    def name(self) -> str:
        """Return user's name."""
        chunks = filter(bool, [
            self.tg_first_name,
            self.tg_last_name,
            f'[{self.tg_username}]' if self.tg_username else None,
        ])
        return ' '.join(chunks)


class Voting(pydantic.BaseModel):
    """Voting."""

    id: uuid.UUID
    participants: typing.List[TgID]

    max_stocks: int
    max_steaks: int

    voted_stocks: typing.List[StockName]
    voted_steaks: typing.List[int]

    started_at: datetime.datetime
    finished_at: typing.Optional[datetime.datetime]

    @property
    def pk(self) -> str:
        """Return primary key."""
        return str(self.id)


class Stock(pydantic.BaseModel):
    """Stock."""

    name: StockName
    code: str
    order: int
    lot: int


class Quote(pydantic.BaseModel):
    """Quote."""

    open_price: decimal.Decimal
    close_price: decimal.Decimal


class PurchaseItem(pydantic.BaseModel):
    """Purchase item."""

    name: StockName
    quantity: int


class Purchase(pydantic.BaseModel):
    """Stock purchase."""

    id: uuid.UUID
    date: datetime.date
    stocks: typing.List[PurchaseItem]
    commission: decimal.Decimal
    cost: decimal.Decimal
    cash: decimal.Decimal

    @property
    def pk(self) -> str:
        """Return primary key."""
        return str(self.id)
