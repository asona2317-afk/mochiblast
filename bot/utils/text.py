"""
Kumpulan helper untuk memformat teks yang dikirim ke pengguna.
"""

from html import escape


def safe_html(text: str) -> str:
    """Escape teks agar aman dikirim dengan parse_mode HTML."""
    if text is None:
        return ""
    return escape(str(text))


def format_datetime(dt) -> str:
    """Format objek datetime menjadi string yang mudah dibaca."""
    if dt is None:
        return "-"
    return dt.strftime("%d-%m-%Y %H:%M")
