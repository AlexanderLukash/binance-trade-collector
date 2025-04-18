from src.domain.entities.trade import TradeEntity


def convert_data_to_entity(data: dict) -> TradeEntity:
    return TradeEntity(
        symbol=data["s"],
        trade_id=data["t"],
        price=float(data["p"]),
        quantity=float(data["q"]),
        is_buyer_market_maker=data["m"],
    )
