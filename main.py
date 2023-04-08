import logging
from telegram import InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,ConversationHandler,CallbackQueryHandler
import os
from voice.voice import Voice


# Global variables
# Conversations states
recive_audio_state,save_audio_state,menu,search_word=range(4)
TOKEN = '6038975530:AAHLkgPEKYvs7Dud83dISYfOn_yF6ZLVZSk'
user_id = []
# PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# MARKUPS
options1 = [
    [InlineKeyboardButton("Search", callback_data='search'),
     InlineKeyboardButton("Resume", callback_data='resume'),
     InlineKeyboardButton("All2text", callback_data='to_text')],
]
options_markup= InlineKeyboardMarkup(options1)

options2 = [
    [InlineKeyboardButton("Send Audio", callback_data='send_audio')],
]
send_markup= InlineKeyboardMarkup(options2)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    # userName = update.effective_user['first_name']
    user_id.append(update.effective_user['id'] )  
    info="Wellcome!!!"
    update.message.reply_text(info, reply_markup=send_markup)
    return recive_audio_state


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def recive_audio(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        "Send Me the audio"
    )
    return save_audio_state

def save_voice(update, context):
    print("Save Audio Flag")
    voice_msg=update.message.voice.get_file().download(custom_path=str(user_id[0])+".wav")
    print("File Saved \n"
          " Runing  transcription \n")
    global aud
    aud =Voice(voice_msg)
    update.message.reply_text('Recived!!',reply_markup=options_markup)
    return menu

def save_audio(update, context):
    print("Save Audio Flag")
    voice_msg=update.message.audio.get_file().download(custom_path=str(user_id[0])+".wav")
    print("File Saved \n"
          " Runing  transcription \n")
    global aud
    aud = Voice(voice_msg)
    update.message.reply_text('Recived!!',reply_markup=options_markup)
    return menu

def search_button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        'Send me a word to find'
    )
    return search_word
    
def search(update, context ):
    phrase_start_times= aud.search_phrase(str(update.message.text).lower())
    update.message.reply_text(str(phrase_start_times),reply_markup=options_markup)
    return menu

def resume_button(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        'Resume',reply_markup=options_markup
    )
    return ConversationHandler.END

def to_text(update, context):
    query = update.callback_query
    query.answer()
    text=aud.audio_to_text()
    query.edit_message_text(
        str(text),reply_markup=options_markup
    )
    return menu

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
           recive_audio_state:[CallbackQueryHandler(recive_audio, pattern='send_audio'),],
           save_audio_state:[
                MessageHandler( Filters.audio , save_audio),
                MessageHandler( Filters.voice , save_voice)
            ],
           menu: [
                CallbackQueryHandler(search_button, pattern='search'),
                CallbackQueryHandler(resume_button, pattern='resume'), 
                CallbackQueryHandler(to_text, pattern='to_text'),       
            ],
            search_word:[
                MessageHandler( Filters.text , search)
            ]

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
