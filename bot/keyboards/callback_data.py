"""
Kumpulan konstanta callback_data yang dipakai di seluruh inline keyboard.
Disentralisasi di satu file supaya tidak ada typo saat mencocokkan
callback_data di handler.
"""

# Menu utama
MENU_MAIN = "menu:main"
MENU_PRICELIST = "menu:pricelist"
MENU_CARA_ORDER = "menu:cara_order"
MENU_KEUNGGULAN = "menu:keunggulan"
MENU_ADMIN = "menu:admin"
MENU_CHANNEL = "menu:channel"

# Pricelist
PRICELIST_BASIC = "pricelist:basic"
PRICELIST_PREMIUM = "pricelist:premium"

# Order
ORDER_START_BASIC = "order:start:basic"
ORDER_START_PREMIUM = "order:start:premium"
ORDER_DURASI_PREFIX = "order:durasi:"
ORDER_LPM_PREFIX = "order:lpm:"
ORDER_CONFIRM = "order:confirm"
ORDER_CANCEL = "order:cancel"
ORDER_SKIP_REQUEST = "order:skip_request"

# Admin panel
ADMIN_PANEL = "admin:panel"
ADMIN_STATS = "admin:stats"
ADMIN_ORDERS = "admin:orders"
ADMIN_BROADCAST = "admin:broadcast"
ADMIN_USERS = "admin:users"
ADMIN_SETTINGS = "admin:settings"
ADMIN_ORDERS_PAGE_PREFIX = "admin:orders:page:"

# Broadcast
BROADCAST_CONFIRM = "broadcast:confirm"
BROADCAST_CANCEL = "broadcast:cancel"
