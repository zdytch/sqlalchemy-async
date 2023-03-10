from db_config import Model
from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column as Column, relationship
from decimal import Decimal
from enum import StrEnum
from uuid import UUID


class Exchange(StrEnum):
    NYSE = 'NYSE'
    NASDAQ = 'NASDAQ'
    CME = 'CME'
    NYMEX = 'NYMEX'
    BINANCE = 'BINANCE'


class InstrumentType(StrEnum):
    STOCK = 'STK'
    FUTURE = 'FUT'
    CRYPTO = 'CRP'


class TradeSide(StrEnum):
    BUY = 'BUY'
    SELL = 'SELL'


class TradeStatus(StrEnum):
    IDEA = 'IDEA'
    PENDING = 'PENDING'
    SUBMITTED = 'SUBMITTED'
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CANCELED = 'CANCELED'


class OrderType(StrEnum):
    LIMIT = 'LIMIT'
    STOP = 'STOP'
    STOP_LIMIT = 'STOP_LIMIT'
    MARKET = 'MARKET'


class OrderRole(StrEnum):
    ENTRY_POINT = 'ENTRY_POINT'
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP_LOSS = 'STOP_LOSS'


class OrderStatus(StrEnum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    FILLED = 'FILLED'


class Instrument(Model):
    symbol: Mapped[str]
    exchange: Mapped[Exchange]
    type: Mapped[InstrumentType]
    description: Mapped[str]

    __table_args__ = (UniqueConstraint('symbol', 'exchange'),)


class Trade(Model):
    instrument_id: Mapped[UUID] = Column(ForeignKey('instrument.id'))
    instrument: Mapped[Instrument] = relationship()
    side: Mapped[TradeSide]
    status: Mapped[TradeStatus] = Column(Enum(TradeStatus), default=TradeStatus.IDEA)


class Order(Model):
    trade_id: Mapped[UUID] = Column(ForeignKey('trade.id', ondelete='CASCADE'))
    trade: Mapped[Trade] = relationship(back_populates='orders')
    type: Mapped[OrderType]
    role: Mapped[OrderRole]
    status: Mapped[OrderStatus] = Column(Enum(OrderStatus), default=OrderStatus.DRAFT)
    price: Mapped[Decimal] = Column(default=Decimal('0.0'))
    trigger_price: Mapped[Decimal] = Column(default=Decimal('0.0'))

    __table_args__ = (UniqueConstraint('trade_id', 'role'),)
