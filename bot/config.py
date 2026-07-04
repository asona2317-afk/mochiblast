"""
Konfigurasi utama aplikasi Mochi Blast Bot.

Modul ini bertugas membaca seluruh environment variable dari file .env
(atau dari environment sistem, misalnya saat deploy di Railway) dan
mengekspornya dalam bentuk objek Settings yang mudah diakses di
seluruh bagian aplikasi.
"""

import os
from dataclasses import dataclass, field
from typing import List

from dotenv import load_dotenv

load_dotenv()


def _parse_admin_ids(raw: str) -> List[int]:
    """Mengubah string 'id1,id2,id3' menjadi list of int."""
    if not raw:
        return []
    result = []
    for part in raw.split(","):
        part = part.strip()
        if part.isdigit():
            result.append(int(part))
    return result


@dataclass(frozen=True)
class Settings:
    bot_token: str
    admin_ids: List[int] = field(default_factory=list)
    admin_username: str = "Cici_Mochi"
    channel_username: str = "mochi_blast"
    channel_url: str = "https://t.me/mochi_blast"
    database_url: str = "sqlite+aiosqlite:///mochi_blast.db"
    log_level: str = "INFO"


def _load_settings() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    if not bot_token:
        raise RuntimeError(
            "BOT_TOKEN belum diset. Silakan isi file .env atau environment "
            "variable BOT_TOKEN terlebih dahulu."
        )

    admin_ids = _parse_admin_ids(os.getenv("ADMIN_IDS", ""))
    admin_username = os.getenv("ADMIN_USERNAME", "Cici_Mochi").strip().lstrip("@")
    channel_username = os.getenv("CHANNEL_USERNAME", "mochi_blast").strip().lstrip("@")
    channel_url = os.getenv("CHANNEL_URL", f"https://t.me/{channel_username}").strip()
    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///mochi_blast.db").strip()
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()

    return Settings(
        bot_token=bot_token,
        admin_ids=admin_ids,
        admin_username=admin_username,
        channel_username=channel_username,
        channel_url=channel_url,
        database_url=database_url,
        log_level=log_level,
    )


settings = _load_settings()
