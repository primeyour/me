import asyncio
from pyrogram import Client, filters
from instagrapi import Client as InstaClient
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton

#env Change This to your varible's
TELEGRAM_API_ID = "20836266"  #here put your api id
TELEGRAM_API_HASH = "bbdd206f92e1ca4bc4935b43dfd4a2a1"  #hash id
TELEGRAM_BOT_TOKEN = "8054568983:AAHWTggsclivHKu8JgZRIyY8Gfd1RhEnVfg" #bot token
INSTAGRAM_USERNAME = "" #instagram user
INSTAGRAM_PASSWORD = "" # password the instagram account
AUTHORIZED_USERS_FILE = "authorized_users.txt" # this file save allowed users id to use bot 
CAPTION_FILE = "caption.txt" # this file save caption to use in reels
DEFAULT_LANGUAGE = "en"  # here you can change language (en=english fa=farsi)


insta_client = InstaClient()
insta_client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)


app = Client("my_bot", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH, bot_token=TELEGRAM_BOT_TOKEN)


main_menu_fa = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📤 Upload a Reels")],
        [KeyboardButton("📤 Upload Multiple Reels")]
    ],
    resize_keyboard=True
)

main_menu_en = ReplyKeyboardMarkup(
    [
        [KeyboardButton("📤 Upload a Reels")],
        [KeyboardButton("📤 Upload Multiple Reels")]
    ],
    resize_keyboard=True
)


def save_language(user_id, language):
    try:
        with open("languages.txt", "a") as file:
            file.write(f"{user_id}:{language}\n")
    except Exception as e:
        print(f"Error saving language: {e}")


def get_language(user_id):
    try:
        with open("languages.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                uid, lang = line.strip().split(":")
                if uid == str(user_id):
                    return lang
    except FileNotFoundError:
        return DEFAULT_LANGUAGE
    return DEFAULT_LANGUAGE


def is_authorized(user_id):
    try:
        with open(AUTHORIZED_USERS_FILE, "r") as file:
            authorized_ids = file.read().splitlines()
        return str(user_id) in authorized_ids
    except FileNotFoundError:
        return False


@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    
    
    if not is_authorized(user_id):
        
        language = get_language(user_id)

        if language == "fa":
            await message.reply(
                f"🔎You are not authorized to use this bot.\n\n🆔 Your user ID: {user_id}"
            )
        else:
            await message.reply(
                f"⛔ You are not authorized to use this bot.\n\n🆔 Your user ID: {user_id}"
            )
        return

    
    language = get_language(user_id)

    if language == "fa":
        await message.reply(
            "👋 Welcome to the bot!\nClick on the buttons below to upload a Reels or multiple Reels at once.",
            reply_markup=main_menu_fa
        )
    else:
        await message.reply(
            "👋 Welcome to the bot!\nClick on the buttons below to upload a Reels or multiple Reels at once.",
            reply_markup=main_menu_en
        )


@app.on_message(filters.text & filters.regex("^📤 Upload a Reels$"))
async def request_single_reels_fa(client, message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        await message.reply("You are not authorized to use this bot.")
        return

    await message.reply("🎥 Please send your video.")

@app.on_message(filters.text & filters.regex("^📤 Upload a Reels$"))
async def request_single_reels_en(client, message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        await message.reply("⛛ You are not authorized to use this bot.")
        return

    await message.reply("🎥 Please send your video.")


@app.on_message(filters.text & filters.regex("^📤 Upload Multiple Reels"))
async def request_multiple_reels_fa(client, message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        await message.reply("⛔ You are not authorized to use this bot.")
        return

    await message.reply("🎥  Please send your videos. The bot will upload them one by one with a 30-second gap.")

@app.on_message(filters.text & filters.regex("^📤 Upload Multiple Reels$"))
async def request_multiple_reels_en(client, message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        await message.reply("⛛ You are not authorized to use this bot.")
        return

    await message.reply("🎥 Please send your videos. The bot will upload them one by one with a 30-second gap.")


@app.on_message(filters.video)
async def upload_multiple_reels(client, message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        await message.reply("⛔ Please.")
        return

    try:
        
        language = get_language(user_id)

        
        video_path = await message.download()

        
        with open(CAPTION_FILE, "r", encoding="utf-8") as file:
            caption = file.read().strip()

        
        insta_client.clip_upload(video_path, caption)

        
        if language == "fa":
            await message.reply("✅ The video was successfully uploaded as a Reels on Instagram.")
        else:
            await message.reply("✅ The video was successfully uploaded as a Reels on Instagram.")

        
        await asyncio.sleep(30)

    except Exception as e:
        
        if language == "fa":
            await message.reply(f"⚠️ خطا: {e}")
        else:
            await message.reply(f"⚠️ Error: {e}")


app.run()
