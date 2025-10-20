import telebot

import requests

import json

from datetime import datetime

import time

import io



# Your bot token

BOT_TOKEN = "<BOT_TOKEN>"

#A luxurious admin panel will be added soon.



bot = telebot.TeleBot(BOT_TOKEN)



# Dictionary for storing user state

user_states = {}

user_tokens = {}



# Different cases

STATE_WAITING_TOKEN = "waiting_token"

STATE_WAITING_PHOTO = "waiting_photo"

STATE_WAITING_NAME = "waiting_name"





def check_bot_token(token):

    """Check the token and get bot information"""

    try:

        url = f"https://api.telegram.org/bot{token}/getMe"

        response = requests.get(url, timeout=10)



        if response.status_code == 200:

            data = response.json()

            if data.get("ok"):

                bot_info = data["result"]

                return {

                    "valid": True,

                    "username": bot_info.get("username", "undefined"),

                    "first_name": bot_info.get("first_name", "undefined"),

                    "id": bot_info.get("id", "undefined"),

                    "can_join_groups": bot_info.get("can_join_groups", False),

                    "can_read_all_group_messages": bot_info.get(

                        "can_read_all_group_messages", False

                    ),

                    "supports_inline_queries": bot_info.get(

                        "supports_inline_queries", False

                    ),

                }



        return {"valid": False, "error": "Invalid token or bot not found"}



    except requests.exceptions.Timeout:

        return {"valid": False, "error": "Connection timed out"}

    except requests.exceptions.RequestException:

        return {"valid": False, "error": "Internet connection error"}

    except Exception as e:

        return {"valid": False, "error": f"Unexpected error: {str(e)}"}





def get_bot_creation_time(bot_id):

    """Calculating the approximate bot creation date from the ID"""

    try:

        timestamp = (int(bot_id) >> 32) + 1293840000

        creation_date = datetime.fromtimestamp(timestamp)

        return creation_date.strftime("%Y-%m-%d %H:%M:%S")

    except:

        return "undefined"





def create_main_keyboard():

    """Main keyboard"""

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    keyboard.add(

        telebot.types.KeyboardButton("🔍 Token check"),

        telebot.types.KeyboardButton("📊 statistics"),

    )

    keyboard.add(

        telebot.types.KeyboardButton("❓ help"),

        telebot.types.KeyboardButton("⚙️ Settings"),

    )

    return keyboard





def create_token_actions_keyboard():

    """Token Actions Keyboard"""

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)

    keyboard.add(

        telebot.types.InlineKeyboardButton(

            "📸 Change image", callback_data="change_photo"

        ),

        telebot.types.InlineKeyboardButton(

            "✏️ Change name", callback_data="change_name"

        ),

    )

    keyboard.add(

        telebot.types.InlineKeyboardButton(

            "🔄 Re-examine", callback_data="recheck_token"

        ),

        telebot.types.InlineKeyboardButton(

            "🗑️ Scan image", callback_data="delete_photo"

        ),

    )

    return keyboard





@bot.message_handler(commands=["start"])

def start(message):

    user_id = message.from_user.id

    user_states[user_id] = None



    welcome_text = f"""🤖 Welcome to the Token Checker Bot!



👋 Hello {message.from_user.first_name}



🔍 This bot helps you:

• Check the validity of bot tokens

• View detailed bot information

• Change bot images and names

• Useful statistics



⚠ Important note: The image change command may not work with some bots.



📝 To start the scan, click "Scan Token" or submit. /check"""



    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_keyboard())





@bot.message_handler(commands=["check"])

def check_command(message):

    request_token(message)





@bot.message_handler(func=lambda message: message.text == "🔍 Token check")

def request_token(message):

    user_id = message.from_user.id

    user_states[user_id] = STATE_WAITING_TOKEN



    bot.send_message(

        message.chat.id,

        "🔑 Submit the token you want to checke:\n\n"

        "Example: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ\n\n"

        "⚠️ Verify the token is valid before sending.",

        reply_markup=telebot.types.ReplyKeyboardRemove(),

    )





@bot.message_handler(func=lambda message: message.text == "📊 statistics")

def show_stats(message):

    stats_text = f"""📊 Bot statistics:



👥 Number of users: {len(user_states)}

🔍 Number of tokens examined: {len(user_tokens)}

⏰ Uptime: Since session started

🌟 Bot status: Running normally



💡 Tips:

• Keep your tokens in a safe place

• Do not share tokens with untrusted people

• Check your tokens regularly."""



    bot.send_message(message.chat.id, stats_text, reply_markup=create_main_keyboard())





@bot.message_handler(func=lambda message: message.text == "❓ help")

def show_help(message):

    help_text = """❓ Bot usage help:



🔍 Token check:

• Click "Check Token" or submit. /check

• Send the bot token

• You will get comprehensive information about the bot.



🔄 Change bot settings:

• After checking the token, click the buttons.

• You can change the image and name.



📸 Change the image:

• Click "Change Image"

• Send the new image



✏️ Change Name:

• Click "Change Name"

• Send the new name



💡 Important Tips:

• Ensure the token is valid

• Use high-quality images

• Choose clear names for your bots"""



    bot.send_message(message.chat.id, help_text, reply_markup=create_main_keyboard())





@bot.message_handler(func=lambda message: message.text == "⚙️ Settings")

def show_settings(message):

    settings_text = """⚙️ Bot settings:



🔧 Available settings:

• Clear token history

• Reset user status

• View the last checked token



📝 To clean data send: /clear

🔄 To reset send: /reset"""



    keyboard = telebot.types.InlineKeyboardMarkup()

    keyboard.add(

        telebot.types.InlineKeyboardButton(

            "🗑️ Data cleansing", callback_data="clear_data"

        ),

        telebot.types.InlineKeyboardButton(

            "🔄 Reset", callback_data="reset_state"

        ),

    )



    bot.send_message(message.chat.id, settings_text, reply_markup=keyboard)





@bot.message_handler(

    func=lambda message: user_states.get(message.from_user.id) == STATE_WAITING_TOKEN

)

def handle_token(message):

    user_id = message.from_user.id

    token = message.text.strip()



    # Check the basic token format

    if ":" not in token or len(token) < 35:

        bot.send_message(

            message.chat.id,

            "❌ Invalid token format!\n\n"

            "The token should be in this format::\n"

            "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ",

            reply_markup=create_main_keyboard(),

        )

        user_states[user_id] = None

        return



    # Send a download message

    loading_msg = bot.send_message(message.chat.id, "🔍 Token is being checked...")



    # Token check

    result = check_bot_token(token)



    bot.delete_message(message.chat.id, loading_msg.message_id)



    if result["valid"]:

        # Save user token

        user_tokens[user_id] = token

        user_states[user_id] = None



        bot_info = result

        creation_time = get_bot_creation_time(bot_info["id"])



        # Create result message

        result_text = f"""✅ The token is correct!



🤖 Bot Information:

• the name: {bot_info['first_name']}

• Usernim: @{bot_info['username']}

• hands: {bot_info['id']}

• Date of establishment: {creation_time}



⚙️ Powers:

• Join groups: {'✅' if bot_info['can_join_groups'] else '❌'}

• Read all messages: {'✅' if bot_info['can_read_all_group_messages'] else '❌'}

• Embedded queries: {'✅' if bot_info['supports_inline_queries'] else '❌'}



🎯 Select the operation you want to perform:"""



        bot.send_message(

            message.chat.id, result_text, reply_markup=create_token_actions_keyboard()

        )



    else:

        bot.send_message(

            message.chat.id,

            f"❌ Token check failed!\n\n"

            f"the reason: {result['error']}\n\n"

            "Make sure:\n"

            "• Token validity\n"

            "• The bot has not been deleted.\n"

            "• Internet connection",

            reply_markup=create_main_keyboard(),

        )

        user_states[user_id] = None





@bot.callback_query_handler(func=lambda call: True)

def handle_callback(call):

    user_id = call.from_user.id



    if call.data == "change_photo":

        if user_id not in user_tokens:

            bot.answer_callback_query(call.id, "❌ No saved token found!")

            return



        user_states[user_id] = STATE_WAITING_PHOTO

        bot.send_message(

            call.message.chat.id,

            "📸 Send the new image you want to assign to the bot.:\n\n"

            "⚠️ Make sure the image is:\n"

            "• High quality\n"

            "• Suitable for boots\n"

            "• Less than 10 MB",

        )

        bot.answer_callback_query(call.id, "📸 Send new photo")



    elif call.data == "change_name":

        if user_id not in user_tokens:

            bot.answer_callback_query(call.id, "❌ No saved token found!")

            return



        user_states[user_id] = STATE_WAITING_NAME

        bot.send_message(

            call.message.chat.id,

            "✏️ Send the new name to the bot:\n\n"

            "📝 The name can be:\n"

            "• From 1 to 64 letters\n"

            "• Contains letters, numbers and symbols\n"

            "• clear and understandable",

        )

        bot.answer_callback_query(call.id, "✏️ Send new name")



    elif call.data == "recheck_token":

        if user_id in user_tokens:

            token = user_tokens[user_id]

            result = check_bot_token(token)



            if result["valid"]:

                bot.answer_callback_query(call.id, "✅ The token is still valid!")

            else:

                bot.answer_callback_query(call.id, "❌ The token is no longer valid!")

        else:

            bot.answer_callback_query(call.id, "❌ No saved token found!")



    elif call.data == "delete_photo":

        if user_id not in user_tokens:

            bot.answer_callback_query(call.id, "❌ No saved token found!")

            return



        token = user_tokens[user_id]

        try:

            url = f"https://api.telegram.org/bot{token}/deleteMyProfilePhoto"

            response = requests.post(url, timeout=10)



            if response.status_code == 200 and response.json().get("ok"):

                bot.answer_callback_query(call.id, "🗑️ Bot image deleted!")

                bot.send_message(call.message.chat.id, "✅ Bot image successfully scanned!")

            else:

                bot.answer_callback_query(call.id, "❌ Failed to scan image!")

        except:

            bot.answer_callback_query(call.id, "❌ Image scanning error!")



    elif call.data == "clear_data":

        if user_id in user_tokens:

            del user_tokens[user_id]

        if user_id in user_states:

            user_states[user_id] = None

        bot.answer_callback_query(call.id, "🗑️ Data cleaned!")



    elif call.data == "reset_state":

        user_states[user_id] = None

        bot.answer_callback_query(call.id, "🔄 Status reset!")





@bot.message_handler(content_types=["photo"])

def handle_photo(message):

    user_id = message.from_user.id



    if user_states.get(user_id) == STATE_WAITING_PHOTO:

        if user_id not in user_tokens:

            bot.send_message(message.chat.id, "❌ Error: No saved token found!")

            return



        token = user_tokens[user_id]



        try:

            loading_msg = bot.send_message(

                message.chat.id, "📸 Bot image is being changed..."

            )



            # Get image information

            file_info = bot.get_file(message.photo[-1].file_id)

            file_url = (

                f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"

            )



            # Download image

            photo_response = requests.get(file_url)



            # Upload image to the specified bot

            upload_url = f"https://api.telegram.org/bot{token}/setMyProfilePhoto"



            files = {"photo": ("profile.jpg", photo_response.content, "image/jpeg")}



            response = requests.post(upload_url, files=files, timeout=30)



            bot.delete_message(message.chat.id, loading_msg.message_id)



            if response.status_code == 200:

                result = response.json()

                if result.get("ok"):

                    bot.send_message(

                        message.chat.id,

                        "✅ Bot image changed successfully! 📸\n\n"

                        "Now you can change the name too if you want..",

                        reply_markup=create_main_keyboard(),

                    )



                    # Switch to automatic name change mode

                    user_states[user_id] = STATE_WAITING_NAME

                    bot.send_message(message.chat.id, "✏️ Now send the new name to the bot:")

                else:

                    error_msg = result.get("description", "Unknown error")

                    bot.send_message(

                        message.chat.id,

                        f"❌ Failed to change image!\n\n"

                        f"the reason: {error_msg}\n\n"

                        "💡 advice:\n"

                        "• Use an image less than 5MB in size.\n"

                        "• Make sure the image is in JPG or PNG format.\n"

                        "• Try a square image.",

                        reply_markup=create_main_keyboard(),

                    )

            else:

                bot.send_message(

                    message.chat.id,

                    f"❌ Connection error! Error code: {response.status_code}\n\n"

                    "Verify the validity of the token and internet connection..",

                    reply_markup=create_main_keyboard(),

                )



        except requests.exceptions.Timeout:

            bot.send_message(

                message.chat.id,

                "❌ Connection timed out!\nTry again with a smaller image..",

                reply_markup=create_main_keyboard(),

            )

        except Exception as e:

            bot.send_message(

                message.chat.id,

                f"❌ An error occurred while changing the image.:\n{str(e)}",

                reply_markup=create_main_keyboard(),

            )



        user_states[user_id] = None





@bot.message_handler(

    func=lambda message: user_states.get(message.from_user.id) == STATE_WAITING_NAME

)

def handle_name_change(message):

    user_id = message.from_user.id

    new_name = message.text.strip()



    if user_id not in user_tokens:

        bot.send_message(message.chat.id, "❌ Error: No saved token found!")

        return



    if len(new_name) < 1 or len(new_name) > 64:

        bot.send_message(message.chat.id, "❌ Name must be between 1 and 64 characters.!")

        return



    token = user_tokens[user_id]



    try:

        # Change bot name

        url = f"https://api.telegram.org/bot{token}/setMyName"

        data = {"name": new_name}



        response = requests.post(url, data=data)



        if response.status_code == 200 and response.json().get("ok"):

            bot.send_message(

                message.chat.id,

                f"✅ Bot name changed successfully!\n\n"

                f"New name: {new_name}\n\n"

                "🎉 All changes are done!",

                reply_markup=create_main_keyboard(),

            )

        else:

            bot.send_message(

                message.chat.id,

                "❌ Failed to change name!\n"

                "Make sure the name is appropriate and does not contain prohibited words..",

                reply_markup=create_main_keyboard(),

            )



    except Exception as e:

        bot.send_message(

            message.chat.id,

            f"❌ An error occurred while changing the name.:\n{str(e)}",

            reply_markup=create_main_keyboard(),

        )



    user_states[user_id] = None





@bot.message_handler(commands=["clear"])

def clear_data(message):

    user_id = message.from_user.id

    if user_id in user_tokens:

        del user_tokens[user_id]

    user_states[user_id] = None

    bot.send_message(

        message.chat.id,

        "🗑️ All saved data has been cleaned!",

        reply_markup=create_main_keyboard(),

    )





@bot.message_handler(commands=["reset"])

def reset_state(message):

    user_id = message.from_user.id

    user_states[user_id] = None

    bot.send_message(

        message.chat.id,

        "🔄 User status has been reset!",

        reply_markup=create_main_keyboard(),

    )





@bot.message_handler(func=lambda message: True)

def handle_other_messages(message):

    user_id = message.from_user.id



    if user_states.get(user_id) is None:

        bot.send_message(

            message.chat.id,

            "👋 Hello! Use the buttons below to navigate the bot..\n\n"

            "Or send /check to check a new token..",

            reply_markup=create_main_keyboard(),

        )





# Run the bot

if __name__ == "__main__":

    print("🚀 Starting the token inspection bot...")

    print("📝 Make sure to replace toke_gizawi with the real token")



    try:

        bot.infinity_polling(timeout=10, long_polling_timeout=5)

    except Exception as e:

        print(f"❌ bot startup error: {e}")

        print("🔄 Try again...")

        time.sleep(5)

        bot.infinity_polling(timeout=10, long_polling_timeout=5)
