"""
Service untuk operasi terkait tabel `orders`.
"""

from datetime import datetime, timedelta
from typing import Optional, Sequence

from sqlalchemy import func, select

from bot.database import get_session
from bot.models.order import Order, OrderStatus
from bot.utils.logger import get_logger

logger = get_logger(__name__)


async def create_order(
    telegram_id: int,
    username: Optional[str],
    paket: str,
    durasi: str,
    jumlah_lpm: str,
    request_lpm: Optional[str],
    teks_sebar: str,
) -> Order:
    """Menyimpan order baru ke database."""
    async with get_session() as session:
        order = Order(
            telegram_id=telegram_id,
            username=username,
            paket=paket,
            durasi=durasi,
            jumlah_lpm=jumlah_lpm,
            request_lpm=request_lpm,
            teks_sebar=teks_sebar,
            status=OrderStatus.PENDING,
        )
        session.add(order)
        await session.flush()
        await session.refresh(order)
        logger.info("Order baru dibuat: id=%s telegram_id=%s paket=%s", order.id, telegram_id, paket)
        return order


async def get_order_by_id(order_id: int) -> Optional[Order]:
    async with get_session() as session:
        result = await session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()


async def update_order_status(order_id: int, status: str) -> None:
    async with get_session() as session:
        result = await session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order is not None:
            order.status = status
            session.add(order)
            logger.info("Status order id=%s diubah menjadi %s", order_id, status)


async def get_orders_page(page: int, per_page: int = 5) -> tuple[Sequence[Order], int]:
    """Mengambil order dengan pagination, diurutkan dari yang terbaru."""
    async with get_session() as session:
        count_result = await session.execute(select(func.count(Order.id)))
        total = count_result.scalar_one()

        offset = max(page - 1, 0) * per_page
        result = await session.execute(
            select(Order).order_by(Order.created_at.desc()).offset(offset).limit(per_page)
        )
        orders = result.scalars().all()
        return orders, total


async def count_total_orders() -> int:
    async with get_session() as session:
        result = await session.execute(select(func.count(Order.id)))
        return result.scalar_one()


async def count_orders_today() -> int:
    async with get_session() as session:
        start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        result = await session.execute(
            select(func.count(Order.id)).where(
                Order.created_at >= start_of_day,
                Order.created_at < end_of_day,
            )
        )
        return result.scalar_one()
