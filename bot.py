#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Telegram Bot to offer covid-19 information from THL database as a reply to certain messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Covid-19 bot for to easily get new information of corona situation in Finland. 
For now it gives information of Helsingin ja Uudenmaan, Varsinais-Suomen and Pirkanmaan areas. 
On Telegram, send "/ohje" -message to the bot and it will give you further instructions on how to use it
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import restapi
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from decouple import config

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def ohje(update, context):
    """Send instructions message when the command /ohje is issued."""
    update.message.reply_text('OHJEET: \n- kooste tai k: Hae koronakooste isoimmilta alueilta lähettämällä viesti "kooste" tai viesti "k"\n- vs tai tku: Hae kooste Varsinais-Suomen alueelta lähettämällä viesti "vs" tai "tku"\n- pm tai tre: Hae koronakooste Pirkanmaalta lähettämällä viesti "pm" tai "tre" \n- hus tai hki: Hae koronakooste Helsingin ja Uudenmaan alueelta lähettämällä viesti "hus" tai "hki"\n- suomi tai s: Hae koronakooste koskien koko Suomen aluetta lähettämällä viesti "suomi" tai "s"')
    

def vastaus(update, context):
    """
    Send newest total number of covid-19 cases of the area as a message when area shortcut letters (kooste, vs, pm, hus or s) are issued. 
    If any other text is issued, send instructions message.
    """
    areaArray=[]
    # Check if area shortcut letters are issued
    if update.message.text == "kooste":
        areaArray=restapi.idAreas
    elif update.message.text == "k":
        areaArray=restapi.idAreas
    elif update.message.text == "vs":
        areaArray=restapi.idVS
    elif update.message.text == "tku":
        areaArray=restapi.idVS
    elif update.message.text == "pm":
        areaArray=restapi.idPM
    elif update.message.text == "tre":
        areaArray=restapi.idPM
    elif update.message.text == "hus":
        areaArray=restapi.idHUS
    elif update.message.text == "hki":
        areaArray=restapi.idHUS
    elif update.message.text == "s":
        areaArray=restapi.idS
    # If area shortcut letters were issued, send total covid-19 cases of the required area
    if areaArray != []:
        # Get new data from the THL API
        labels, cases = restapi.haeData()
        rText=""
        for id in areaArray:
            index=restapi.idAreas.index(id)
            rText += labels[index] + ": " + cases[index]+"\n"
        update.message.reply_text(rText)
    else:
        # Else send instructions message
        ohje(update, context)


def virhe(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    API_KORONABOTTI_TOKEN = config('KORONABOTTI_TOKEN')
    updater = Updater(API_KORONABOTTI_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("ohje", ohje))
    
    # on noncommand i.e message create reply text based on the message
    dp.add_handler(MessageHandler(Filters.text, vastaus))

    # log all errors
    dp.add_error_handler(virhe)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
