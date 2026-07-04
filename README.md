# 🍓 Mochi Blast Bot

Bot Telegram order otomatis untuk layanan Jaseb (Jasa Sebar), dibangun dengan
**Python 3.12**, **aiogram 3.x**, **SQLAlchemy (async)**, dan **SQLite**.

## ✨ Fitur

**Customer**
- Menu utama interaktif (`/start`) dengan inline keyboard
- Pricelist Mochi Basic & Mochi Premium
- Alur order berbasis FSM (username → teks sebar → durasi → jumlah LPM → request → konfirmasi)
- Notifikasi order otomatis ke admin
- Admin membalas order cukup dengan reply pesan, otomatis diteruskan ke customer
- Menu Cara Order, Keunggulan, Admin, dan Channel

**Admin**
- Panel admin (`/admin`)
- Statistik (total user, total order, order hari ini)
- Daftar order masuk dengan pagination
- Broadcast pesan (text, foto, video, dokumen, animasi/GIF) ke seluruh user
- Total user terdaftar
- Menu pengaturan (dasar, siap dikembangkan)

## 🗂️ Struktur Project

```
bot/
├── main.py              # Entry point aplikasi
├── config.py            # Konfigurasi & environment variable
├── loader.py            # Inisialisasi Bot & Dispatcher
├── database.py          # Koneksi & session SQLAlchemy async
├── middlewares/         # Error handler & registrasi user otomatis
├── handlers/            # Handler customer, order, admin, fallback
├── keyboards/           # Inline keyboard & callback data
├── states/              # FSM states (order, broadcast)
├── services/            # Business logic (user, order, broadcast)
├── models/              # Model SQLAlchemy (User, Order)
└── utils/                # Logger & teks statis
requirements.txt
.env.example
railway.json
Procfile
```

## ⚙️ Instalasi Lokal

1. Clone/salin project ini, lalu masuk ke foldernya.

2. Buat virtual environment (opsional tapi disarankan):

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Install dependency:

   ```bash
   pip install -r requirements.txt
   ```

4. Salin `.env.example` menjadi `.env`, lalu isi sesuai kebutuhan:

   ```bash
   cp .env.example .env
   ```

   | Variable            | Keterangan                                             |
   |---------------------|---------------------------------------------------------|
   | `BOT_TOKEN`         | Token bot dari [@BotFather](https://t.me/BotFather)      |
   | `ADMIN_IDS`         | ID Telegram admin, pisahkan koma jika lebih dari satu    |
   | `ADMIN_USERNAME`    | Username admin (tanpa @) untuk tombol "Hubungi Admin"    |
   | `CHANNEL_USERNAME`  | Username channel (tanpa @)                               |
   | `CHANNEL_URL`       | Link lengkap channel                                     |
   | `DATABASE_URL`      | URL database SQLAlchemy (default SQLite lokal)           |
   | `LOG_LEVEL`         | Level logging (`DEBUG`, `INFO`, `WARNING`, `ERROR`)       |

5. Jalankan bot:

   ```bash
   python -m bot.main
   ```

Database SQLite (`mochi_blast.db`) beserta seluruh tabel akan otomatis dibuat
saat bot pertama kali dijalankan.

## 🚀 Deploy ke Railway

1. Push project ini ke repository GitHub.
2. Buat project baru di [Railway](https://railway.app/), pilih **Deploy from GitHub Repo**.
3. Tambahkan environment variable yang sama seperti `.env.example` di tab **Variables**.
4. Railway akan otomatis mendeteksi `railway.json`/`Procfile` dan menjalankan:

   ```
   python -m bot.main
   ```

5. Setelah deploy sukses, bot berjalan dalam mode **polling** selama service aktif.

> Catatan: Karena menggunakan SQLite berbasis file, pastikan Railway service
> menggunakan **Volume** jika ingin data order/user tetap tersimpan permanen
> antar deployment. Untuk kebutuhan skala lebih besar, `DATABASE_URL` dapat
> diganti ke PostgreSQL (misalnya `postgresql+asyncpg://...`) tanpa mengubah
> kode aplikasi karena sudah berbasis SQLAlchemy.

## 🧩 Alur Order Singkat

1. Customer memilih paket di menu **Pricelist** → tekan **Order Basic/Premium**.
2. Bot menanyakan username, teks sebar, durasi, jumlah LPM, dan request (opsional).
3. Bot menampilkan ringkasan order dengan tombol **✅ Kirim** / **❌ Batal**.
4. Setelah dikonfirmasi, order tersimpan di database dan notifikasi dikirim ke admin.
5. Admin cukup **reply** pesan notifikasi order tersebut untuk membalas customer.

## 🛠️ Tech Stack

- Python 3.12
- aiogram 3.x (async, FSM, inline keyboard)
- SQLAlchemy 2.x (async ORM)
- aiosqlite (driver SQLite async)
- python-dotenv

## 📄 Lisensi

Project ini dapat dimodifikasi dan digunakan sesuai kebutuhan bisnis Anda.
