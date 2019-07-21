from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


HANGING, AMOUNT = range(2)


def start(update, context):
    if context.user_data.get('auth', False):
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=' '.join([
                'Alles klar, fangen wir an!',
                'Ich merke mir, wo du Plakate aufhängst.',
            ])
        )
        return hanging(update, context)
    else:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=' '.join([
                'Das geht leider noch nicht.',
                'Erst möchte ich überprüfen, ob du wirklich zur FDP gehörst.',
                'Nenne mir bitte das Passwort, indem du zunächst /start eingibst.'
            ])
        )
        return ConversationHandler.END


HANGING_MARKUP = ReplyKeyboardMarkup(
    [[KeyboardButton('Plakat hängt', request_location=True)]],
    one_time_keyboard=True
)


def hanging(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Drück das Knöpfchen oder teile deinen Standort mit mir, wenn du die nächsten Plakate aufgehängt hast!',
            'Mit /fertig kannst du beenden.'
        ]),
        reply_markup=HANGING_MARKUP)
    return HANGING


def mk_plakat_button(number):
    return KeyboardButton(str(number))


HUNG_MARKUP = ReplyKeyboardMarkup(
    [
        [mk_plakat_button(i) for i in range(1, 5)],
        [mk_plakat_button(i) for i in range(5, 9)],
        [mk_plakat_button(i) for i in range(9, 13)]
    ],
    one_time_keyboard=True
)


def hung(update, context):
    location = update.message.location
    context.user_data['last_location'] = f'({location.latitude},{location.longitude})'
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Klasse!',
            'Wie viele hast du aufgehängt?'
        ]),
        reply_markup=HUNG_MARKUP
    )
    return AMOUNT


def amount(update, context, fp):
    sender = update.message.from_user
    who = 'N/A' if context.user_data.get('anonymous',
                                         True) else f'{sender.first_name} {sender.last_name}'
    where = context.user_data['last_location']
    when = update.message.date.strftime('%Y-%m-%d %H:%M:%S')
    hung_amount = int(update.message.text)
    fp.write(f'{who};{where};{when};{hung_amount}\n')
    # TODO: actually handle amount
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Alles klar!',
            'Das habe ich mir gemerkt!'
        ])
    )
    return hanging(update, context)


def done(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Danke für deine Arbeit!',
            'Solltest du noch mal aufhängen wollen, gib einfach wieder /plakate ein.'
        ]),
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def no_parse(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=' '.join([
            'Das war leider die falsche Eingabe oder ich konnte sie nicht verstehen.',
            'Versuch es noch mal.',
            'Alternativ kannst du mir /fertig abbrechen.'
        ])
    )


def conversation_handler(write_to):
    fp = open(write_to, 'a')
    return ConversationHandler(
        entry_points=[CommandHandler('plakate', start)],
        states={
            HANGING: [MessageHandler(Filters.location, hung)],
            AMOUNT: [MessageHandler(Filters.regex(
                r'^\d+$'), lambda u, c: amount(u, c, fp))]
        },
        fallbacks=[
            CommandHandler('fertig', done),
            CommandHandler('plakate', start),
            MessageHandler(~Filters.command, no_parse)
        ]
    )
