# plakatlog_bot

This repository has code for a telegram bot that simply provides you a keyboard
with buttons from 1 to 12.
If you press one of these, your location will be saved to a google spreadsheet
alongside the number you pressed.

It is intended to be used for placards in hung during election campains.
These need to be removed once the election is over and this bot aids you in
tracking where placards have been hung.

## Setup

In order to use the bot you need to have `pipenv` installed.
You can probably do this by:
```sh
pip install pipenv --user
```

If this doesn't work for you, have a look at
https://docs.pipenv.org/en/latest/install/#installing-pipenv.

After you have installed `pipenv` and it has been added to your path, run
```sh
pipenv shell -c python ./plakatlog_bot.py --token <ACCESS-TOKEN>
```
and the app will start pulling the telegram API for updates.
Obiously, you need to replace the `<ACCESS-TOKEN>` with an appropriate
access-token for the telegram bot.
