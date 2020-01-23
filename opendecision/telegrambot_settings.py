import os
if os.environ.get('DJANGO_PRODUCTION') is not None:
    token = os.environ['TELEGRAM_TOKEN']
else:
    token = '731203182:AAE573Gi-6PcAD7feyJzo3oIuJTeEWJ4mPc'

DJANGO_TELEGRAMBOT = {

    'MODE' : 'WEBHOOK', #(Optional [str]) # The default value is WEBHOOK,
                        # otherwise you may use 'POLLING'
                        # NB: if use polling you must provide to run
                        # a management command that starts a worker

    'WEBHOOK_SITE' : 'https://open-decision.herokuapp.com',


    'STRICT_INIT': True, # If set to True, the server will fail to start if some of the
                         # apps contain telegrambot.py files that cannot be successfully
                         # imported.

    'BOTS' : [
        {
        'TOKEN' : token

        },
    ],

}
