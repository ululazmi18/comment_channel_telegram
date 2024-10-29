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

config_file = 'config.json'
# Jika config.json belum ada, buat dengan default
default_config = {
    "api_id": None,
    "api_hash": "",
    "comment_delay_min": 1,
    "comment_delay_max": 5,
    "switch_delay_min": 300,
    "switch_delay_max": 600,
    "message_limit": 2
}

if not os.path.exists(config_file):
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=4)
    print("python main.py API_ID API_Hash")
    exit()

# Baca config.json yang ada
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Simpan kembali config jika ada perubahan
with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=4)

# Validasi api_id dan api_hash
api_id = config.get('api_id')
api_hash = config.get('api_hash')

if api_id is None or api_hash == "":
    print("python main.py API_ID API_Hash")
    exit()

# Mendapatkan semua file .session dan nomor telepon
session_files = [f for f in os.listdir('.') if f.endswith('.session')]
phone_numbers = [f[:-8] for f in session_files]  # Menghilangkan .session

# Jika tidak ada nomor yang ditemukan
if not phone_numbers:
    print("Tidak ada file session ditemukan.")
    exit()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    clear_terminal()
    print("1. Jalankan Sekali")
    print("2. Jalankan Berulang")
    print("3. Buat Session Baru")
    print("4. Jeda Komentar (", config['comment_delay_min'], "-", config['comment_delay_max'], ") detik")
    print("5. Jeda Akun (", config['switch_delay_min'], "-", config['switch_delay_max'], ") detik")
    print("6. Jumlah Post yang dikomentari dari yang terbaru (", config['message_limit'], ")")
    print("7. Exit")

def display_log_file():
    try:
        with open("log.txt", 'r', encoding='utf-8') as f:
            content = f.read()  # Membaca seluruh isi file
            print(content)  # Menampilkan isi file
    except FileNotFoundError:
        print("File log.txt tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

def log_to_file(line):
    with open("log.txt", 'a', encoding='utf-8') as f:
        f.write(str(line) + '\n')

def clear_log_file():
    with open("log.txt", 'w', encoding='utf-8') as f:
        pass

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

    os.makedirs('text', exist_ok=True)

    default_channels = "test13524\nayayawae15243"
    
    if not os.path.exists('channels.txt'):
        with open('channels.txt', 'w', encoding='utf-8') as channels_file:
            channels_file.write(default_channels)
            print("File channels.txt telah dibuat dengan isi default.")
            log_to_file("File channels.txt telah dibuat dengan isi default.")

    # Membaca saluran dari file
    with open('channels.txt', 'r') as file:
        target_channels = [line.strip().replace('https://t.me/', '') for line in file if line.strip()]

    text_files = [f for f in os.listdir('text') if f.endswith('.txt')]
    media_files = [f for f in os.listdir('media') if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.avi'))]

    for channel_username in target_channels:
        # Mendapatkan pesan terbaru dari setiap saluran
        async for message in app.get_chat_history(channel_username, limit=message_limit):
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
                                log_to_file("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file} | {media_file}")
                            elif media_path.lower().endswith(('.mp4', '.avi')):
                                await discussion_message.reply_video(video=media_path, caption=komentar)
                                random_text_file = random_text_file.split('.')[0]
                                media_file = media_file.split('.')[0]
                                print("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file} | {media_file}")
                                log_to_file("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file} | {media_file}")
                        except Exception:
                            pass  # Mengabaikan kesalahan ketika tidak bisa mengirim
                    else:
                        await discussion_message.reply(komentar)
                        random_text_file = random_text_file.split('.')[0]
                        media_file = media_file.split('.')[0]
                        print("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file}")
                        log_to_file("✅ " + Fore.GREEN + f"{channel_username}" + Style.RESET_ALL + f" | {random_text_file}")

            except errors.FloodWait as e:
                print(f"Flood wait: {e.x + 10} detik. Menghentikan sementara...")
                log_to_file(f"Flood wait: {e.x + 10} detik. Menghentikan sementara...")
                await countdown(e.x + 10)  # Menunggu e.x + 10 detik
            
            except Exception as e:
                print("❌ " + Fore.RED + f"{channel_username}" + Style.RESET_ALL)
                log_to_file("❌ " + Fore.RED + f"{channel_username}" + Style.RESET_ALL)

            
            comment_delay = random.randint(comment_delay_min, comment_delay_max)
            await countdown(comment_delay)
            log_to_file(comment_delay)

async def run_all_sessions():
    total_numbers = len(phone_numbers)
    for index, phone_number in enumerate(phone_numbers):
        print(f"Using : {phone_number}")
        log_to_file(f"Using : {phone_number}")
        await process_channel(phone_number)
            
        switch_delay_min = config.get('switch_delay_min', 300)
        switch_delay_max = config.get('switch_delay_max', 600)
        # Jika bukan nomor terakhir, jalankan countdown switch delay
        if index < total_numbers - 1:
            switch_delay = random.randint(switch_delay_min, switch_delay_max)
            await countdown(switch_delay)
            log_to_file(switch_delay)

async def main_menu():
    while True:
        display_menu()
        choice = input("Pilih opsi: ")

        if choice == "1":
            await run_all_sessions()
            input("Mission Complete. \nPress the Enter key to the main menu.")
        elif choice == "2":
            while True:
                await run_all_sessions()
                switch_delay = random.randint(config.get('switch_delay_min', 300), config.get('switch_delay_max', 600))
                await countdown(switch_delay)
        elif choice == "3":
            phone_number = input("nomor telepon: ").strip()
            session_file = f"{phone_number}.session"
            if not os.path.exists(session_file):
                async with Client(phone_number, api_id=api_id, api_hash=api_hash, phone_number=phone_number) as app:
                    await app.get_me()  # Menggunakan await di sini
                    print(f"{phone_number} berhasil ditambahkan.")
                    log_to_file(f"{phone_number} berhasil ditambahkan.")
            else:
                print(f"{phone_number} sudah ada.")
                log_to_file(f"{phone_number} sudah ada.")
            input("Press the Enter key to return to the main menu.")
        elif choice == "4":
            min_delay = input("jeda minimum: ")
            max_delay = input("jeda maksimum: ")
            config['comment_delay_min'] = int(min_delay) if min_delay else 1
            config['comment_delay_max'] = int(max_delay) if max_delay else 5
        elif choice == "5":
            min_delay = input("jeda minimum: ")
            max_delay = input("jeda maksimum: ")
            config['switch_delay_min'] = int(min_delay) if min_delay else 300
            config['switch_delay_max'] = int(max_delay) if max_delay else 600
        elif choice == "6":
            limit = input("Jumlah Post: ")
            config['message_limit'] = int(limit) if limit else 2
        elif choice == "7":
            exit()
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)

# Titik masuk program
async def main_run():
    clear_log_file()
    await main_menu()

if __name__ == "__main__":
    asyncio.run(main_run())
