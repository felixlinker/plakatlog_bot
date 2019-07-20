from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler
from argparse import ArgumentParser

# basic logging settings
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def mk_plakat_button(number):
    return KeyboardButton(str(number), request_location=True)

BUTTONS = [
    list(map(mk_plakat_button, range(1, 5))),
    list(map(mk_plakat_button, range(5, 9))),
    list(map(mk_plakat_button, range(9, 13)))
]

def start(update, context):
    markup = ReplyKeyboardMarkup(BUTTONS)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Ich speichere die Plakate, die du aufgehangen hast. Wie viele hast du gerade aufgehängt?',
        reply_markup=markup
    )

def end(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text='Okay, ich verfolge eure Plakate nicht weiter.',
        reply_markup=ReplyKeyboardRemove()
    )

# Configure command line arguments to the bot
parser = ArgumentParser(description='Starte einen Server, der für einen Telegram Bot pollt, wo du Plakate aufgehangen hast.')
parser.add_argument('--token', '-t', type=str, help='Der Bot Access Token')

# Start the polling-"server"
def main():
    args = parser.parse_args()
    updater = Updater(token=args.token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('end', end))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
