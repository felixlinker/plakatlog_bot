from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import re


LOGIN, ANONIMITY = range(2)


def start(update, context):
    if not context.user_data.get('auth', False):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=' '.join([
                'Hallo! Ich helfe dir zu verfolgen, wo du wieviele Plakate aufgehängt hast.',
                'Damit ich aber weiß, dass du einer von uns bist, nenne mir doch bitte das Passwort.'
            ])
        )
        return LOGIN
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text='Hallo! Dich kenne ich ja schon - das Passwort brauche ich also nicht noch mal.'
        )
        return pw(update, context)


def pw(update, context):
    context.user_data['auth'] = True
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Ist es okay, wenn wir deinen Namen mit den Plakaten speichern, die du aufhängst? (ja,offen/nein,anonym)',
            'Du kannst diese Einstellunge jederzeit über /start ändern.'
        ]),
        reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton('Offen'), KeyboardButton('Anonym')]
        ])
    )
    return ANONIMITY


def be_anonymous(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Deine Einstellungen wurden gespeichert und es kann losgehen!',
            'Gib einfach /plakate ein und wir fangen an!'
        ]),
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def be_public(update, context):
    context.user_data['anonymous'] = False
    return be_anonymous(update, context)


def cancel(update, context):
    return ConversationHandler.END


def no_parse(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Das war leider die falsche Eingabe oder ich konnte sie nicht verstehen.',
            'Versuch es noch mal.',
            'Alternativ kannst du /abbrechen.'
        ])
    )


def conversation_handler(actual_password):
    return ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOGIN: [MessageHandler(
                Filters.regex(re.compile(f'^{actual_password}$', re.I)),
                pw
            )],
            ANONIMITY: [
                MessageHandler(Filters.regex(
                    re.compile('^(ja|offen)$', re.I)), be_public),
                MessageHandler(Filters.regex(re.compile(r'^(nein|anonym)$', re.I)),
                               be_anonymous)
            ]
        },
        fallbacks=[
            CommandHandler('abbrechen', cancel),
            CommandHandler('start', start),
            MessageHandler(Filters.update, no_parse)
        ]
    )
