from telegram.ext import Updater
from argparse import ArgumentParser

import convs.login as login
import convs.plakate as plakate

# basic logging settings
import logging
logging.basicConfig(
    filename='./plakatlog_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configure command line arguments to the bot
parser = ArgumentParser(
    description='Starte einen Server, der für einen Telegram Bot pollt, wo du Plakate aufgehangen hast.')
parser.add_argument('--token', '-t', type=str,
                    required=True, help='Der Bot Access Token')
parser.add_argument('--file', '-f', type=str,
                    required=True, help='Pfad zur .csv Datei')
parser.add_argument('--password', '-p', type=str, required=True,
                    help='Passwort, das ein Nutzer eingeben muss, um den Bot freizuschalten.')

# Start the polling-"server"


def main():
    args = parser.parse_args()
    updater = Updater(token=args.token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(login.conversation_handler(args.password))
    dispatcher.add_handler(plakate.conversation_handler(args.file))

    logging.info('Now polling')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
