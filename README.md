# 🚀 Telegram Token Checker Bot 🤖

A professional Telegram bot for **checking bot tokens**, viewing detailed bot info, and updating bot profile pictures & names.  
Reliable, fast, and easy-to-use. ⚡

---

## 💎 Features

- ✅ Check bot token validity  
- 📊 View user and token statistics  
- 📸 Change bot profile photo  
- ✏️ Change bot name  
- 🗑️ Clear stored data & reset user state  
- ⚡ Quick and intuitive interface  

---

## 🛠 Requirements

- Python 3.10+  
- Termux (Android) or any Linux environment  
- Internet connection 🌐  

---

## 📦 Installation (Termux)

```bash
# 1️⃣ Update & upgrade system
pkg update -y && pkg upgrade -y

# 2️⃣ Install Python & pip
pkg install python -y

# 3️⃣ Install required tools
pkg install git curl nano -y

# 4️⃣ Install Python libraries
pip install -r requirements.txt

# 5️⃣ Clone the repository
git clone https://github.com/JavaKyoseva/telegram-token-checker
cd telegram-token-checker
export BOT_TOKEN="<BOT_TOKEN>"
```

---

⚡ Run the Bot
```bash
python main.py
```

---

🎯 Usage

Usage:

1. Send /start or select "🔍 Token check" from the main menu.
2. Submit the bot token you want to check.
3. The bot will display detailed information and status.
4. Use the buttons to change profile photo or bot name.
5. To clear stored data, use /clear.
6. To reset user state, use /reset.


---

⚠ Important Notes

Important Notes:

- Profile photo change may not work for all bots.
- Keep your bot tokens secure and do not share them.
- Images must be JPG/PNG format and under 5MB.
- Ensure a stable internet connection while performing operations.


---

🌟 Additional Information

Additional Information:

- The bot provides quick feedback on token validity.  
- Statistics include the number of users and scanned tokens.  
- Designed to be reliable on Termux and Linux environments.
