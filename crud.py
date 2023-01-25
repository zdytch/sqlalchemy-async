from .models import Trade, TradeSide
from .db import DB
from sqlmodel import select, delete
from sqlalchemy.orm import joinedload
from uuid import UUID


async def create_trade(db: DB, instrument_id: UUID, side: TradeSide) -> Trade:
    trade = Trade(instrument_id=instrument_id, side=side)
    db.add(trade)
    await db.commit()

    return trade


async def read_trade(db: DB, **kwargs) -> Trade:
    result = await db.execute(
        select(Trade).filter_by(**kwargs).options(joinedload(Trade.instrument))
    )

    return result.unique().scalar_one()


async def update_trade(db: DB, trade_id: UUID, side: TradeSide) -> Trade:
    trade = await read_trade(db, id=trade_id)
    trade.side = side
    await db.commit()

    return trade


async def delete_trade(db: DB, trade_id: UUID) -> None:
    await db.execute(delete(Trade).filter_by(trade_id=trade_id))
    await db.commit()
