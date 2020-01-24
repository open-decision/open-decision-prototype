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

tree = {
  "header": {
    "version": 0.1,
    "build_date": "2020-01-20",
    "logic_type": "jsonLogic version X",
    "owner": "Testperson",
    "tree_name": "R\u00fccklastschriftgeb\u00fchren",
    "tree_slug": "rucklastschriftgebuhren",
    "start_node": "start",
    "vars": {}
  },
  "angemessen": {
    "name": "angemessen",
    "question": "Eine Geb\u00fchr von bis zu vier Euro ist leider angemessen.",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  },
  "ankundigung": {
    "name": "Ank\u00fcndigung",
    "question": "Wurde die Lastschrift vorher durch eine Rechnung angek\u00fcndigt oder zieht die Firma regelm\u00e4\u00dfig Geld ein?",
    "input_type": "button",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "==": [
            {
              "var": "answer"
            },
            "Ja"
          ]
        },
        "0",
        {
          "==": [
            {
              "var": "answer"
            },
            "Nein"
          ]
        },
        "1"
      ]
    },
    "answers": [
      "Ja",
      "Nein"
    ],
    "results": {
      "0": {
        "destination": "ankundigungsart"
      },
      "1": {
        "destination": "musterschreiben"
      }
    }
  },
  "start": {
    "name": "start",
    "question": "<p>Wie hoch sind die von Ihnen geforderten Geb&uuml;hren?</p>",
    "input_type": "number",
    "end_node": "false",
    "rules": {
      "if": [
        {
          ">=": [
            {
              "var": "answer"
            },
            4.0
          ]
        },
        "0",
        {
          "<": [
            {
              "var": "answer"
            },
            4.0
          ]
        },
        "1"
      ]
    },
    "answers": [],
    "results": {
      "0": {
        "destination": "ankundigung"
      },
      "1": {
        "destination": "angemessen"
      }
    }
  },
  "ankundigungsart": {
    "name": "Ank\u00fcndigungsart",
    "question": "<p>Wie wurdest du nach der fehlgeschlagenen Lastschrift benachrichtigt?</p>",
    "input_type": "list",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "in": [
            {
              "var": "answer"
            },
            [
              "E-Mail",
              "Keine Ank\u00fcndigung"
            ]
          ]
        },
        "0",
        {
          "in": [
            {
              "var": "answer"
            },
            [
              "Brief"
            ]
          ]
        },
        "1",
        {
          "in": [
            {
              "var": "answer"
            },
            [
              "SMS"
            ]
          ]
        },
        "2"
      ]
    },
    "answers": [
      "Brief",
      "SMS",
      "E-Mail",
      "Keine Ank\u00fcndigung"
    ],
    "results": {
      "0": {
        "destination": "max3"
      },
      "1": {
        "destination": "max4"
      },
      "2": {
        "destination": "max309"
      }
    }
  },
  "max4": {
    "name": "max4",
    "question": "In diesem Fall ist eine Geb\u00fchr von bis zu vier Euro leider angemessen.",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  },
  "max309": {
    "name": "max3.09",
    "question": "In diesem Fall ist nur eine Geb\u00fchr von 3,09 Euro zul\u00e4ssig. Soll ein Musterschreiben zur R\u00fcckforderung generiert werden?",
    "input_type": "button",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "==": [
            {
              "var": "answer"
            },
            "Ja"
          ]
        },
        "0",
        {
          "==": [
            {
              "var": "answer"
            },
            "Nein"
          ]
        },
        "1"
      ]
    },
    "answers": [
      "Ja",
      "Nein"
    ],
    "results": {
      "0": {
        "destination": "musterschreiben"
      },
      "1": {
        "destination": "ende"
      }
    }
  },
  "max3": {
    "name": "max3",
    "question": "In diesem Fall ist nur eine Geb\u00fchr von 3 Euro zul\u00e4ssig. Soll ein Musterschreiben zur R\u00fcckforderung generiert werden?",
    "input_type": "button",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "==": [
            {
              "var": "answer"
            },
            "Ja"
          ]
        },
        "0",
        {
          "==": [
            {
              "var": "answer"
            },
            "Nein"
          ]
        },
        "1"
      ]
    },
    "answers": [
      "Ja",
      "Nein"
    ],
    "results": {
      "0": {
        "destination": "musterschreiben"
      },
      "1": {
        "destination": "ende"
      }
    }
  },
  "musterschreiben": {
    "name": "Musterschreiben",
    "question": "- Musterschreiben -",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  },
  "ende": {
    "name": "Ende",
    "question": "-",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  }
}


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
