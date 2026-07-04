"""
Model tabel `orders`.
"""

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from bot.models.base import Base


class OrderStatus:
    PENDING = "pending"
    PROCESSED = "processed"
    REJECTED = "rejected"
    DONE = "done"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    paket: Mapped[str] = mapped_column(String(50), nullable=False)
    durasi: Mapped[str] = mapped_column(String(50), nullable=False)
    jumlah_lpm: Mapped[str] = mapped_column(String(50), nullable=False)
    request_lpm: Mapped[str] = mapped_column(String(255), nullable=True)
    teks_sebar: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default=OrderStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Order id={self.id} telegram_id={self.telegram_id} paket={self.paket} status={self.status}>"
