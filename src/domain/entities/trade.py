from dataclasses import dataclass

from src.domain.entities.base import BaseEntity


@dataclass
class TradeEntity(BaseEntity):
    symbol: str
    trade_id: int
    price: float
    quantity: float
    buyer_order_id: int
    seller_order_id: int
    is_buyer_market_maker: bool
