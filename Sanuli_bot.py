import asyncio
from telegram import Update, Poll, Bot
from telegram.ext import Application, CommandHandler, ContextTypes
import aiocron
import datetime
from bot_token import BOT_TOKEN
from csv_util import read_last_poll_ids, read_registered_groups, write_last_poll_id, write_registered_group, overwrite_registered_groups

token = BOT_TOKEN


async def is_admin(update: Update) -> bool:
    chat = update.effective_chat
    user = update.effective_user

    chat_member = await chat.get_member(user.id)

    return chat_member.status in ["administrator", "creator"] or update.effective_chat.type not in ["group", "supergroup"]


async def current_time_tell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"The current time is {current_time}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await is_admin(update):
        if update.effective_chat.type not in ["group", "supergroup"]:
            username = update.message.from_user.username
            await update.message.reply_text(
                f"1 x Huutinen käyttäjälle @{username}"
            )
        else:
            write_registered_group(update.effective_chat.id)
            await update.message.reply_text("Aamul nähää")
    else:
        await update.message.reply_text("What is bro doing")
    
    
    
async def stop_krapolli(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await is_admin(update):
        registered_groups = read_registered_groups()
        chat_id = update.effective_chat.id
        if chat_id in registered_groups:  
            registered_groups.remove(chat_id)
            overwrite_registered_groups(registered_groups)
            await update.message.reply_text("Ok ne loppuu kyl mut miks")
        else:
            await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('goofy-ahh-sounds.mp3', 'rb'))
    else:
        await update.message.reply_text("What is bro doing")
    
    
async def close_poll(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id) -> None:
    chat_id = update.effective_chat.id 
    last_polls = read_last_poll_ids() 
    
    if chat_id in last_polls:
        message_id = last_polls[chat_id]
        try:
            await context.bot.stop_poll(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            print(f"Couldn't stop poll: {e}")
            await update.message.reply_text(f"Couldn't stop poll: {e}")
        

async def create_polls(bot: Bot) -> None:
    registered_groups = read_registered_groups()
    for chat_id in registered_groups:
        await post_poll(bot, chat_id, "Krapolli", ["0", "1", "2", "3", "4", "5 (selitä)"])

async def force_polls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await is_admin(update):
        chat_id = update.effective_chat.id
        await close_poll(update, context, chat_id)
        await post_poll(context.bot, chat_id, "Krapolli", ["0", "1", "2", "3", "4", "5 (selitä)"])
    else:
        await update.message.reply_text("What is bro doing")
    
    



  
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo_path = 'ilmeeni.jpg'
    
    await update.message.reply_photo(photo=open(photo_path, 'rb'))
    


async def post_poll(bot, chat_id, question: str, options: list) -> None:
    message = await bot.send_poll(
        chat_id, question, options, type=Poll.REGULAR, is_anonymous=False
    )
    write_last_poll_id(chat_id, message.message_id)

    
async def start_krapollis(bot):
        current_time = datetime.datetime.now().strftime("%H:%M")
        aiocron.crontab('00 09 * * *', func=create_polls, args=[bot], start=True)
        await bot.send_message(5160204048, f"Bot started at {current_time}")
        
async def goofy_ahh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open('goofy-ahh-sounds.mp3', 'rb'))

def main() -> None:
    
    application = Application.builder().token(token).build()
    bot = application.bot    
    loop = asyncio.get_event_loop()

    
    loop.run_until_complete(start_krapollis(bot))

  
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop_krapolli))
    application.add_handler(CommandHandler("force_poll", force_polls))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("current_time", current_time_tell))
    application.add_handler(CommandHandler("moro", goofy_ahh))

    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    
if __name__ == "__main__":
    main()

