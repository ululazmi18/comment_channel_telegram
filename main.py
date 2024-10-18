import logging
import argparse
import os
import json
import random
from pyrogram import Client, errors
import asyncio
from colorama import Fore, Style, init

# Inisialisasi colorama
init()
# Konfigurasi logging
logging.basicConfig(level=logging.ERROR)

# Setup argparser
parser = argparse.ArgumentParser(description='Skrip Auto Comment Telegram')
parser.add_argument('--api', nargs=2, metavar=('API_ID', 'API_HASH'), help='API ID dan API Hash untuk Telegram')
parser.add_argument('--cdelay', nargs=2, type=int, metavar=('COMMENT_DELAY_MIN', 'COMMENT_DELAY_MAX'), help='Delay minimum dan maksimum untuk komentar dalam detik')
parser.add_argument('--sdelay', nargs=2, type=int, metavar=('SWITCH_DELAY_MIN', 'SWITCH_DELAY_MAX'), help='Delay minimum dan maksimum untuk pergantian akun dalam detik')
parser.add_argument('--limit', type=int, metavar='LIMIT', help='Jumlah pesan yang diambil dari setiap saluran (default: 2)')
parser.add_argument('--add', type=str, metavar='PHONE_NUMBER', help='Nomor telepon baru untuk ditambahkan (format: +123456789)')

args = parser.parse_args()

# Ambil argumen dari parser
api_id = args.api[0] if args.api else None
api_hash = args.api[1] if args.api else ""
comment_delay_min = args.cdelay[0] if args.cdelay else 1
comment_delay_max = args.cdelay[1] if args.cdelay else 5
switch_delay_min = args.sdelay[0] if args.sdelay else 300
switch_delay_max = args.sdelay[1] if args.sdelay else 600
message_limit = args.limit if args.limit is not None else 2

config_file = 'config.json'
# Jika config.json belum ada, buat dengan default
default_config = {
    "api_id": None,
    "api_hash": "",
    "comment_delay_min": comment_delay_min,
    "comment_delay_max": comment_delay_max,
    "switch_delay_min": switch_delay_min,
    "switch_delay_max": switch_delay_max,
    "message_limit": message_limit
}

if not os.path.exists(config_file):
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=4)
    print("python main.py API_ID API_Hash")
    exit()

# Baca config.json yang ada
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Memperbarui config jika argumen diberikan
if args.api:
    config['api_id'] = api_id
    config['api_hash'] = api_hash
if args.cdelay:
    config['comment_delay_min'] = comment_delay_min
    config['comment_delay_max'] = comment_delay_max
if args.sdelay:
    config['switch_delay_min'] = switch_delay_min
    config['switch_delay_max'] = switch_delay_max
if args.limit is not None:
    config['message_limit'] = message_limit

# Simpan kembali config jika ada perubahan
with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=4)

# Validasi api_id dan api_hash
api_id = config.get('api_id')
api_hash = config.get('api_hash')

if api_id is None or api_hash == "":
    print("python main.py API_ID API_Hash")
    exit()

# Tambahkan nomor telepon baru jika ada argumen
if args.add:
    phone_number = args.add.strip()
    session_file = f"{phone_number}.session"
    # Periksa apakah file session sudah ada
    if not os.path.exists(session_file):
        with Client(phone_number, api_id=api_id, api_hash=api_hash, phone_number=phone_number) as app:
            app.get_me()
            print(f"{phone_number} berhasil ditambahkan.")
    else:
        print(f"{phone_number} sudah ada.")

# Mendapatkan semua file .session dan nomor telepon
session_files = [f for f in os.listdir('.') if f.endswith('.session')]
phone_numbers = [f[:-8] for f in session_files]  # Menghilangkan .session

# Jika tidak ada nomor yang ditemukan
if not phone_numbers:
    print("Tidak ada file session ditemukan.")
    exit()

async def countdown(t):
    for i in range(t, 0, -1):
        print(f"Wait - {i}          ", flush=True, end="\r")
        await asyncio.sleep(1)

async def process_channel(phone_number):
    app = Client(phone_number, api_id=api_id, api_hash=api_hash, phone_number=phone_number)

    async with app:
        await main(app)

async def main(app):
    # Ambil nilai dari config
    message_limit = config.get('message_limit', 2)
    comment_delay_min = config.get('comment_delay_min', 1)
    comment_delay_max = config.get('comment_delay_max', 5)
    switch_delay_min = config.get('switch_delay_min', 300)
    switch_delay_max = config.get('switch_delay_max', 600)

    os.makedirs('text', exist_ok=True)

    default_channels = "test13524\nayayawae15243"
    
    if not os.path.exists('channels.txt'):
        with open('channels.txt', 'w', encoding='utf-8') as channels_file:
            channels_file.write(default_channels)
            print("File channels.txt telah dibuat dengan isi default.")

    # Membaca saluran dari file
    with open('channels.txt', 'r') as file:
        target_channels = [line.strip().replace('https://t.me/', '') for line in file if line.strip()]

    text_files = [f for f in os.listdir('text') if f.endswith('.txt')]
    media_files = [f for f in os.listdir('media') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.avi'))]

    for channel_username in target_channels:
        # Mendapatkan pesan terbaru dari setiap saluran
        async for message in app.get_chat_history(channel_username, limit=message_limit):
            comment_delay = random.randint(comment_delay_min, comment_delay_max)
            message_id = message.id
            try:
                # Mendapatkan pesan diskusi
                discussion_message = await app.get_discussion_message(channel_username, message_id)

                if text_files:
                    random_text_file = random.choice(text_files)
                    with open(os.path.join('text', random_text_file), 'r', encoding='utf-8') as text_file:
                        message_text = text_file.read().strip()
                else:
                    message_text = "Tidak ada teks untuk dikirim."
                komentar = message_text
                
                # Memeriksa apakah komentar bisa dikirim
                if discussion_message:
                    if media_files:
                        media_file = random.choice(media_files)
                        media_path = os.path.join('media', media_file)
                        try:
                            if media_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                                await discussion_message.reply_photo(photo=media_path, caption=komentar)
                                random_text_file = random_text_file.split('.')[0]
                                media_file = media_file.split('.')[0]
                                print("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file} | {media_file}")
                            elif media_path.lower().endswith(('.mp4', '.avi')):
                                await discussion_message.reply_video(video=media_path, caption=komentar)
                                random_text_file = random_text_file.split('.')[0]
                                media_file = media_file.split('.')[0]
                                print("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file} | {media_file}")
                        except Exception:
                            pass  # Mengabaikan kesalahan ketika tidak bisa mengirim
                    else:
                        await discussion_message.reply(komentar)
                        random_text_file = random_text_file.split('.')[0]
                        media_file = media_file.split('.')[0]
                        print("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file}")

            except errors.FloodWait as e:
                print(f"Flood wait: {e.x + 10} detik. Menghentikan sementara...")
                await countdown(e.x + 10)  # Menunggu e.x + 10 detik
            
            except Exception as e:
                print("❌ " + Fore.RED + f"{channel_username}" + Style.RESET_ALL)

            await countdown(comment_delay)

        # Delay sebelum berpindah akun
        switch_delay = random.randint(switch_delay_min, switch_delay_max)
        await countdown(switch_delay)

async def run_all_sessions():
    for phone_number in phone_numbers:
        print(f"Using : {phone_number}")
        await process_channel(phone_number)

# Menjalankan semua sesi
asyncio.run(run_all_sessions())
