from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from punq import Container

from src.logic.init import init_container
from src.logic.services.base import BaseTradeService

scheduler = AsyncIOScheduler()

container: Container = init_container()


async def start_scheduler():
    trade_service: BaseTradeService = container.resolve(BaseTradeService)
    scheduler.add_job(
        trade_service.delete_old_trades,
        IntervalTrigger(hours=12),
        name="Delete old trades",
    )
    scheduler.start()
