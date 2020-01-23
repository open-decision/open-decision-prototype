# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from bot_data import *
import logging
from json_logic import jsonLogic
import html2markdown
from django_telegrambot.apps import DjangoTelegramBot


# Query database for the right tree using telegrams deeplink to pass init value



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
#  Moegliche States werden definiert
START, CHOICE, CHECK_ANSWER, END = range(4)

def start(bot, update, chat_data):
    if tree[tree['header']['start_node']]['answers']:
        reply_keyboard = [tree[tree['header']['start_node']]['answers']]
        update.message.reply_text(
        html2markdown.convert(tree[tree['header']['start_node']]['question']),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
        html2markdown.convert(tree[tree['header']['start_node']]['question']),
        parse_mode=ParseMode.HTML)
    chat_data['current_node'] = tree['header']['start_node']
    chat_data['log'] = {'nodes': [], 'answers': []}

    return CHECK_ANSWER


def display_node (bot, update, chat_data, current_node):
    if tree[current_node]['answers']:
        reply_keyboard = [tree[current_node]['answers']]
    update.message.reply_text(
                html2markdown.convert(tree[current_node]['question']),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.HTML)
    chat_data['current_node'] = current_node
    return CHECK_ANSWER


def check_answer (bot, update, chat_data):
    #Get answer
    answer = update.message.text.encode('ascii', 'ignore')
    #If input_type is number but input no valid number prompt user again
    if (tree[chat_data['current_node']]['input_type'] == 'number') and not (is_number(answer)):
        update.message.reply_text('Bitte gib eine Zahl ein. Benutze als Trennzeichen bitte einen Punkt und kein Komma.')
    #Use jsonLogic to parse the logic block of the node
    rule = jsonLogic(tree[chat_data['current_node']]['rules'], {"answer":answer})
    #Log node and answer
    chat_data['log']['nodes'].append(chat_data['current_node'])
    chat_data['log']['answers'].append(answer)
    #Set current node to the next that  is about to be
    current_node = tree[chat_data['current_node']]['results'][rule]['destination']
    display_node (bot, update, chat_data, current_node)

def end (bot, update, chat_data):
    update.message.reply_text('Danke, dass du den Bot benutzt hast! Schreibe /cancel um neuzustarten')

# Check if entered value is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # # Create the EventHandler and pass it your bot's token.
    # updater = Updater(token2)
    #
    # # Get the dispatcher to register handlers
    # dp = updater.dispatcher

# Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher
    # To get Dispatcher related to a specific bot
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_token')     #get by bot token
    # dp = DjangoTelegramBot.getDispatcher('BOT_n_username')  #get by bot username



    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_chat_data=True)],

        states={
            CHECK_ANSWER: [MessageHandler(Filters.text, check_answer, pass_chat_data=True)],
        },

        fallbacks=[CommandHandler('cancel', start, pass_chat_data=True)]
    )

    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
