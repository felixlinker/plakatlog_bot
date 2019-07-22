# plakatlog_bot

This repository has code for a telegram bot that simply provides help for
tracking posters hung.
It is intended to be used for a selected group of peoples which - in my case -
is located in Germany. Therefore all dialogues are written in German.

It was initially written for the
[Junge Liberale, Leipzig](https://www.julis-leipzig.de/) but as the use case may
apply to other parties feel free to use the code to track your posters as well.

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
pipenv install
pipenv run python ./plakatlog_bot.py
```
This will prompt you the help for the bot explaining all command line options
available.
These arguments for the most-part are self explanatory.
The bot can be either launched on a local machine that pulls updates from the
telegram API manually or as a webhook on a server.
For this you will need an SSL certificate.
How one can be generated is explained in https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
