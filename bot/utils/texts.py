"""
Kumpulan teks statis yang ditampilkan bot ke customer.
Dipisah dari handler supaya lebih mudah diedit tanpa menyentuh logika.
"""

WELCOME_TEXT = (
    "🍓 <b>Selamat Datang di Mochi Blast</b> 🍡\n\n"
    "Solusi sebar promosi otomatis 24 jam.\n\n"
    "Silakan pilih menu di bawah."
)

PRICELIST_TITLE = "🎀 <b>PRICELIST MOCHI BLAST</b> 🎀\n\nSilakan pilih paket di bawah ini."

MOCHI_BASIC_TEXT = (
    "☁️ <b>MOCHI BASIC</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "【10 GRUP / LPM】\n"
    "3 Hari — Rp5.000\n"
    "5 Hari — Rp10.000\n"
    "7 Hari — Rp15.000\n"
    "1 Bulan — Rp45.000\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "【20 GRUP / LPM】\n"
    "3 Hari — Rp10.000\n"
    "5 Hari — Rp20.000\n"
    "7 Hari — Rp25.000\n"
    "1 Bulan — Rp55.000\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "【30 GRUP / LPM】\n"
    "3 Hari — Rp20.000\n"
    "5 Hari — Rp30.000\n"
    "7 Hari — Rp45.000\n"
    "1 Bulan — Rp65.000"
)

MOCHI_PREMIUM_TEXT = (
    "👑 <b>MOCHI PREMIUM</b>\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "【10 GRUP / LPM】\n"
    "3 Hari — Rp10.000\n"
    "5 Hari — Rp15.000\n"
    "7 Hari — Rp30.000\n"
    "1 Bulan — Rp55.000\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "【20 GRUP / LPM】\n"
    "3 Hari — Rp20.000\n"
    "5 Hari — Rp30.000\n"
    "7 Hari — Rp40.000\n"
    "1 Bulan — Rp75.000\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "【30 GRUP / LPM】\n"
    "3 Hari — Rp30.000\n"
    "5 Hari — Rp45.000\n"
    "7 Hari — Rp55.000\n"
    "1 Bulan — Rp85.000"
)

CARA_ORDER_TEXT = (
    "📖 <b>CARA ORDER</b>\n\n"
    "1. Subscribe @mochi_blast\n"
    "2. Pilih paket\n"
    "3. Isi format\n"
    "4. Kirim order\n"
    "5. Tunggu admin"
)

KEUNGGULAN_TEXT = (
    "⭐ <b>KEUNGGULAN MOCHI BLAST</b>\n\n"
    "✨ Sistem otomatis 24 jam\n"
    "⚡ Cepat\n"
    "💖 Bisa request LPM\n"
    "📈 Cocok semua promosi\n"
    "🤖 Stabil"
)

ADMIN_INFO_TEXT = "👩‍💼 <b>Admin Mochi Blast</b>\n\n@{admin_username}"

CHANNEL_INFO_TEXT = "📢 <b>Channel Mochi Blast</b>\n\n@{channel_username}"

ORDER_ASK_USERNAME = "🛒 Yuk mulai order!\n\nSilakan kirim <b>username Telegram</b> kamu (contoh: @username)."
ORDER_ASK_TEKS_SEBAR = "📝 Silakan kirim <b>teks/isi promosi</b> yang ingin disebar."
ORDER_ASK_DURASI = "⏳ Silakan pilih <b>durasi</b> paket."
ORDER_ASK_JUMLAH_LPM = "📊 Silakan pilih <b>jumlah grup/LPM</b>."
ORDER_ASK_REQUEST_LPM = (
    "💬 Ada <b>request khusus</b> untuk LPM/grup? Kirim pesannya sekarang.\n\n"
    "Jika tidak ada, tekan tombol di bawah."
)

ORDER_SUMMARY_TEMPLATE = (
    "🧾 <b>RINGKASAN ORDER</b>\n\n"
    "Username : {username}\n"
    "Paket : {paket}\n"
    "Durasi : {durasi}\n"
    "Jumlah LPM : {jumlah_lpm}\n"
    "Request : {request_lpm}\n"
    "Teks Sebar :\n{teks_sebar}\n\n"
    "Apakah data sudah benar?"
)

ORDER_CANCELLED_TEXT = "❌ Order dibatalkan."

ORDER_SENT_TO_CUSTOMER = (
    "✅ Order kamu sudah diterima dan diteruskan ke admin.\n"
    "Mohon tunggu, admin akan segera memproses order kamu."
)

ADMIN_NEW_ORDER_TEMPLATE = (
    "📥 <b>ORDER BARU</b>\n\n"
    "Nama : {nama}\n"
    "Username : {username}\n"
    "ID Telegram : {telegram_id}\n"
    "Paket : {paket}\n"
    "Durasi : {durasi}\n"
    "Jumlah LPM : {jumlah_lpm}\n"
    "Request : {request_lpm}\n"
    "Teks Sebar :\n{teks_sebar}\n\n"
    "Waktu : {waktu}\n\n"
    "<i>Balas (reply) pesan ini untuk mengirim balasan ke customer.</i>"
)

ADMIN_PANEL_TEXT = "🛠️ <b>PANEL ADMIN</b>\n\nSilakan pilih menu di bawah."

ADMIN_STATS_TEMPLATE = (
    "📊 <b>STATISTIK MOCHI BLAST</b>\n\n"
    "Total User : {total_user}\n"
    "Total Order : {total_order}\n"
    "Order Hari Ini : {order_hari_ini}"
)

ADMIN_SETTINGS_TEXT = (
    "⚙ <b>PENGATURAN</b>\n\n"
    "Fitur pengaturan lanjutan dapat dikembangkan sesuai kebutuhan, "
    "contohnya mengubah harga, mengubah kontak admin, atau mengubah channel."
)

ADMIN_BROADCAST_ASK_CONTENT = (
    "📢 Kirim konten yang ingin di-broadcast ke seluruh user.\n\n"
    "Bisa berupa Text, Foto, Video, Dokumen, atau Animasi/GIF."
)

ADMIN_BROADCAST_CONFIRM = "Apakah konten di atas sudah benar dan siap dikirim ke seluruh user?"

ADMIN_BROADCAST_RESULT_TEMPLATE = (
    "✅ Broadcast selesai.\n\n"
    "Total User : {total}\n"
    "Berhasil : {success}\n"
    "Gagal : {failed}"
)

UNKNOWN_COMMAND_TEXT = "🤔 Perintah tidak dikenali. Ketik /start untuk melihat menu utama."

NOT_ADMIN_TEXT = "⛔ Kamu tidak memiliki akses ke perintah ini."
