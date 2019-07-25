from telegram.ext import Updater, CommandHandler
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
parser.add_argument('--key', '-k', type=str,
                    help='Pfad zum SSL certificate key')
parser.add_argument('--cert', '-c', type=str,
                    help='Pfad zum SSL certificate')
parser.add_argument('--domain', '-d', type=str,
                    help='Domain, auf der der Server läuft')

def send_file(update, context, file_path):
    if context.user_data.get('auth', False):
        context.bot.send_document(
            chat_id=update.message.chat_id,
            document=open(file_path, 'rb')
        )
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=' '.join([
                'Das geht leider noch nicht.',
                'Erst möchte ich überprüfen, ob du wirklich zur FDP gehörst.',
                'Nenne mir bitte das Passwort, indem du zunächst /start eingibst.'
            ])
        )

def main():
    args = parser.parse_args()
    updater = Updater(token=args.token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(login.conversation_handler(args.password))
    dispatcher.add_handler(plakate.conversation_handler(args.file))
    dispatcher.add_handler(
        CommandHandler('daten', lambda u, c: send_file(u, c, args.file))
    )

    if args.key and args.cert:
        logging.info('Starting webhook')
        updater.start_webhook(listen='0.0.0.0',
                              port=8443,
                              url_path=args.token,
                              key=args.key,
                              cert=args.cert,
                              webhook_url=f'https://{args.domain}:8443/{args.token}')
    else:
        logging.info('Start polling')
        updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
