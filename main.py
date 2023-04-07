import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,ConversationHandler
import os


# Global
audio_recive=1
TOKEN = '6038975530:AAHLkgPEKYvs7Dud83dISYfOn_yF6ZLVZSk'

# PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)





# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    # userName = update.effective_user['first_name']
    # user_id = update.effective_user['id']  
    info="Hello, send your audio."
    update.message.reply_text(info)
    return audio_recive


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def save_audio(update, context):
    """Echo the user message."""
    print("Save Audio Flag")
    voice_msg=update.message.voice.get_file().download(custom_path="audio.wav")
    print("Archivo Guardado \n Comienza la transcripcion \n")
    # Aqui se llama directamente al metodo de transcripcion en paralelo
    return ConversationHandler.END



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher



    # on different commands - answer in Telegram
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler("start", start)
        ],
        states={
            audio_recive: [
                MessageHandler( Filters.audio | Filters.voice , save_audio),
            ],

        },
        fallbacks=[],
    ))
    # dp.add_handler(CommandHandler("help", help))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook('https://botgetid.herokuapp.com/' + TOKEN)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
