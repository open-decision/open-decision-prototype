# -*- coding: utf-8 -*-
import re
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
from json_logic import jsonLogic
import html2markdown
import re

from django_telegrambot.apps import DjangoTelegramBot

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
tree = {}
#  Moegliche States werden definiert
START, CHECK_ANSWER, CHECK_ACCESS_CODE, END = range(4)

def start(bot, update, chat_data):
    start_query = update.message.text[7::]
    if re.match("^[a-z]{10}$", start_query):
        tree = json.loads(PublishedTree.objects.get(url=start_query).tree_data)
        if tree:
            if tree[tree['header']['start_node']]['answers']:
                reply_keyboard = [tree[tree['header']['start_node']]['answers']]
                update.message.reply_text(
                html2markdown.convert(tree[tree['header']['start_node']]['question']),
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                parse_mode=ParseMode.MARKDOWN)
            else:
                update.message.reply_text(
                html2markdown.convert(tree[tree['header']['start_node']]['question']),
                parse_mode=ParseMode.MARKDOWN)
            chat_data['current_node'] = tree['header']['start_node']
            chat_data['log'] = {'nodes': [], 'answers': []}
            return CHECK_ANSWER
    else:
        update.message.reply_text(
        'Please enter your Access Code or click the link you received. Please click /cancel',
        parse_mode=ParseMode.MARKDOWN)
        return CHECK_ACCESS_CODE

def check_access_code(bot, update, chat_data):
    start_query = update.message.text
    if re.match("^[a-z]{10}$", start_query):
        if tree[tree['header']['start_node']]['answers']:
            reply_keyboard = [tree[tree['header']['start_node']]['answers']]
            update.message.reply_text(
            html2markdown.convert(tree[tree['header']['start_node']]['question']),
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text(
            html2markdown.convert(tree[tree['header']['start_node']]['question']),
            parse_mode=ParseMode.MARKDOWN)
        chat_data['current_node'] = tree['header']['start_node']
        chat_data['log'] = {'nodes': [], 'answers': []}
        return CHECK_ANSWER
    else:
        update.message.reply_text(
        'Please enter your Access Code or click the link you received. Please click /cancel',
        parse_mode=ParseMode.MARKDOWN)
        return CHECK_ACCESS_CODE

def display_node (bot, update, chat_data, current_node):
    if tree[current_node]['answers']:
        reply_keyboard = [tree[current_node]['answers']]
        update.message.reply_text(
                html2markdown.convert(tree[current_node]['question']),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(
                html2markdown.convert(tree[current_node]['question']),
        parse_mode=ParseMode.MARKDOWN)
    chat_data['current_node'] = current_node
    return CHECK_ANSWER


def check_answer (bot, update, chat_data):
    #Get answer
    answer = update.message.text.encode('ascii', 'ignore')
    #If input_type is number but input no valid number prompt user again
    if (tree[chat_data['current_node']]['input_type'] == 'number') and not (is_number(answer)):
        update.message.reply_text('Bitte gib eine Zahl ein. Benutze als Trennzeichen bitte einen Punkt und kein Komma.')
        current_node = chat_data['current_node']
        display_node (bot, update, chat_data, current_node)
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

# Default dispatcher (this is related to the first bot in settings.DJANGO_TELEGRAMBOT['BOTS'])
    dp = DjangoTelegramBot.dispatcher

    # Add conversation handler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_chat_data=True)],

        states={
            CHECK_ANSWER: [MessageHandler(Filters.text, check_answer, pass_chat_data=True)],
            CHECK_ACCESS_CODE : [MessageHandler(Filters.text, check_access_code, pass_chat_data=True)]
        },

        fallbacks=[CommandHandler('cancel', start, pass_chat_data=True)]
    )

    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)
