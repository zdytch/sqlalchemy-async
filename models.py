from db_config import DBModel
from sqlmodel import Field, Column, Enum, Relationship, ForeignKey
from sqlalchemy import UniqueConstraint
from uuid import UUID
from decimal import Decimal
import enum


class Exchange(enum.Enum):
    NYSE = 'NYSE'
    NASDAQ = 'NASDAQ'
    CME = 'CME'
    NYMEX = 'NYMEX'
    BINANCE = 'BINANCE'


class InstrumentType(enum.Enum):
    STOCK = 'STK'
    FUTURE = 'FUT'
    CRYPTO = 'CRP'


class TradeSide(enum.Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class TradeStatus(enum.Enum):
    IDEA = 'IDEA'
    PENDING = 'PENDING'
    SUBMITTED = 'SUBMITTED'
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    CANCELED = 'CANCELED'


class OrderType(enum.Enum):
    LIMIT = 'LIMIT'
    STOP = 'STOP'
    STOP_LIMIT = 'STOP_LIMIT'
    MARKET = 'MARKET'


class OrderRole(enum.Enum):
    ENTRY_POINT = 'ENTRY_POINT'
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP_LOSS = 'STOP_LOSS'


class OrderStatus(enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    FILLED = 'FILLED'


class Instrument(DBModel, table=True):
    symbol: str
    exchange: Exchange = Field(sa_column=Column(Enum(Exchange), nullable=False))
    type: InstrumentType = Field(sa_column=Column(Enum(InstrumentType), nullable=False))
    description: str

    __table_args__ = (UniqueConstraint('symbol', 'exchange'),)


class Trade(DBModel, table=True):
    instrument_id: UUID = Field(foreign_key='instrument.id')
    instrument: Instrument = Relationship()
    side: TradeSide = Field(sa_column=Column(Enum(TradeSide), nullable=False))
    status: TradeStatus = Field(
        sa_column=Column(Enum(TradeStatus), nullable=False), default=TradeStatus.IDEA
    )


class Order(DBModel, table=True):
    trade_id: UUID = Field(
        sa_column=Column(ForeignKey('trade.id', ondelete='CASCADE'), nullable=False)
    )
    trade: Trade = Relationship(back_populates='orders')
    type: OrderType = Field(sa_column=Column(Enum(OrderType), nullable=False))
    role: OrderRole = Field(sa_column=Column(Enum(OrderRole), nullable=False))
    status: OrderStatus = Field(
        sa_column=Column(Enum(OrderStatus), nullable=False), default=OrderStatus.DRAFT
    )
    price: Decimal = Field(default=Decimal('0.0'), nullable=False)
    trigger_price: Decimal = Field(default=Decimal('0.0'), nullable=False)

    __table_args__ = (UniqueConstraint('trade_id', 'role'),)
