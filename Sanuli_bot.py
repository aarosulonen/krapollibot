import asyncio
from telegram import Update, Poll, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import aiocron
import datetime

token_file = open("token.txt")
token = token_file.read()

group_ids_file = open("group_ids.txt")
group_ids = group_ids_file.read().split()

TESTING = False

registered = False

if TESTING:
    REGISTERED_CHAT_ID = group_ids[1]
else:
    REGISTERED_CHAT_ID = group_ids[0]

last_polls = []

async def current_time_tell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.username == "SulosenArska":  # Replace 'YourUsernameHere' with your username
        current_time = datetime.datetime.now().strftime("%H:%M:%S")  # Get the current time
        await update.message.reply_text(f"The current time is {current_time}")
    else:
        await update.message.reply_text("Ok, tilanne on nyt se että mua ei kiinnosta vastata tohon :D")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the message is from a private chat
    if update.message.chat.type == "private":
        username = update.message.from_user.username
        await update.message.reply_text(
            f"1 x Huutinen käyttäjälle @{username}"
        )
        await context.bot.send_message(5160204048, f"@{username} just talked to me") # Läpällä :D
    
    
async def stop_sanuli(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Not possible :DD")

async def close_polls(bot) -> None:
    ids = open("last_ids.txt").read().split()
    if ids and len(ids) == 2:
        for poll_id in ids:
            try:
                poll_id = int(poll_id.strip())
                await bot.stop_poll(chat_id=REGISTERED_CHAT_ID, message_id=poll_id)
            except Exception as e:
                print(f"Couldn't stop poll: {e}")

async def create_polls(bot) -> None:  
    await close_polls(bot)
    global last_polls
    last_polls = []
    await post_poll(bot, "Sanuli?", ["1", "2", "3", "4", "5", "6", "ei"])
    await post_poll(bot, "Wordle?", ["1", "2", "3", "4", "5", "6", "ei"])
    with open("last_ids.txt", 'w') as file:
        for new_id in last_polls:
            file.write(str(new_id) + " ")

async def force_polls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.username == "SulosenArska":    
        await close_polls(context.bot)
        global last_polls
        last_polls = []
        await post_poll(context.bot, "Sanuli?", ["1", "2", "3", "4", "5", "6", "ei"])
        await post_poll(context.bot, "Wordle?", ["1", "2", "3", "4", "5", "6", "ei"])
        with open("last_ids.txt", 'w') as file:
            for new_id in last_polls:
                file.write(str(new_id) + " ")
    else:
        await update.message.reply_text("🤨")

async def send_message_to_registered_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.from_user.username == "SulosenArska":
        global REGISTERED_CHAT_ID
        message_text = ' '.join(context.args)
        
        if message_text:
            await context.bot.send_message(REGISTERED_CHAT_ID, message_text)
        else:
            await update.message.reply_text("Please provide a message to send.")
    else:
        await update.message.reply_text("You are not arska >:(")
  
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = 'ilmeeni.jpg'
    
    await update.message.reply_photo(photo=open(photo_path, 'rb'))
    

async def delete_message_by_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        if update.message.from_user.username == "SulosenArska":
            ids = open("last_ids.txt").read().split()
            if ids and len(ids) == 2:
                for poll_id in ids:
                    try:
                        await context.bot.delete_message(chat_id=REGISTERED_CHAT_ID, message_id=poll_id)
                        print(f"Message with ID {poll_id} deleted successfully.")
                        await update.message.reply_text(f"Message with ID {poll_id} deleted successfully.")
                    except Exception as e:
                        print(f"Couldn't delete message: {e}")
                        await update.message.reply_text(f"Couldn't delete message: {e}")
        else:
            update.message.reply_text("Mega huutinen")
    
async def post_poll(bot, question: str, options: list) -> None:
    global REGISTERED_CHAT_ID
    message = await bot.send_poll(
        REGISTERED_CHAT_ID, question, options, type=Poll.REGULAR, is_anonymous=False
    )
    last_polls.append(message.message_id)

    
async def start_sanulis(bot):
        global registered
        current_time = datetime.datetime.now().strftime("%H:%M")
        if not registered:
            aiocron.crontab('00 22 * * *', func=create_polls, args=[bot], start=True)
            await bot.send_message(5160204048, f"Bot started at {current_time}\nTesting = {TESTING}")
            registered = True
        else:
            await bot.send_message(5160204048, f"This should not happen. start_sanulis failed somehow :D")

def main() -> None:
    
    application = Application.builder().token(token).build()
    bot = application.bot    
    loop = asyncio.get_event_loop()

    
    loop.run_until_complete(start_sanulis(bot))

  
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_message", send_message_to_registered_chat))
    application.add_handler(CommandHandler("stop", stop_sanuli))
    application.add_handler(CommandHandler("force_poll", force_polls))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("delete_last", delete_message_by_id))
    application.add_handler(CommandHandler("current_time", current_time_tell))

    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()

