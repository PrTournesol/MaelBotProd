# -*- coding: utf-8 -*-
import time
import logging
import telepot
import ade
import room
import log
from telepot.loop import MessageLoop
import sys
import jokes
from tokens import *

if len(sys.argv)==2 and sys.argv[1]=="test":
    test = True
else:
    test = False

MAEL_ID = 412934982
THOMAS = 269118097
IR2020_CONV = -1001102632442

WHITELIST = [THOMAS]



chatrooms = []

def getHelpMessage():
        helpMessage = "Je ne saurais pas répondre à votre demande, voici les commandes ausquelles je répond :"\
                    +"\n        /salles_dispo - et je te dis les salles dispo dans l'heure qui vient"\
                    +"\n        /salles_a_dispo - et je te dis les salles du bâtiment A dispo dans l'heure qui vient"\
                    +"\n        /salles_b_dispo - idem avec le bâtiment B"\
                    +"\n        /salles_c_dispo - idem avec le bâtiment C"\
                    +"\n        /salles_cnotlinux_dispo - idem avec le bâtiment C sans les salles linux"\
                    +"\n        /salles_linux_dispo - idem avec les salles Linux du bâtiment C"\
                    +"\n        /on_est_ou - je te donne le lieu du cours en cours ou suivant si tu n'as pas encore cours"\
                    +"\n        /on_a_qui - idem avec le nom du prof"\
                    +"\n        /on_a_quoi - idem avec le nom du cours"\
                    +"\n        /blague - raconte une blague"\
                    +"\n        /add_blague votre blague - ajoute une blague"\
                    +"\n        /remove_blague votre blague - enlève une blague"\
                    +"\n        /help - affiche cet aide"\
                    +"\n        PS : tu peux remplacer les _ par des espaces en rajoutant ? à la fin"
        return helpMessage

    
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    logger.info(msg)
    joke = jokes.jokes(getHelpMessage)
    if chat_id not in chatrooms:
        chatrooms.append(chat_id)
    if content_type == 'text':
        t = str.upper(msg['text'])
        fromUser = msg['from']['id']
        if "QUELLE SALLE ?" in t or "ON EST OU ?" in t or "ON EST OÙ ?" in t\
            or "ON_EST_OU" in t:
            logger.info('On est ou ? / quelle salle ?')
            a = ade.adeGetter()
            message = a.CurrentRoom()
            bot.sendMessage(chat_id, message)
        if "ON A QUI ?" in t or "ON_A_QUI" in t:
            logger.info('On a qui ?')
            a = ade.adeGetter()
            message = a.CurrentTeacher()
            bot.sendMessage(chat_id, message)
        if "ON A QUOI ?" in t or "Y'A QUOI ?" in t or "ON_A_QUOI" in t :
            logger.info('On a quoi ?')
            a = ade.adeGetter()
            message = a.CurrentClass()
            bot.sendMessage(chat_id, message)
        if "SALLES" in t and "?" in t or "/SALLES" in t:
            logger.info('Running Salle dispo(Room.py)')
            rooms = room.roomGetter(bot, chat_id, getHelpMessage)
            message = str(rooms.getAnswer(t))
            logger.info('Room.py has termined with message : ' + message)
            bot.sendMessage(chat_id, message)
        if "/HELP" in t :
            logger.info('Helping message asked')
            bot.sendMessage(chat_id, getHelpMessage())
        if "/BLAGUE" in t or "BLAGUE" in t:
            logger.info('Joke command')
            bot.sendMessage(chat_id, joke.getAnswer(msg['text']))
            #bot.sendMessage(chat_id, "censuré")    
        if "!SAY" in t and fromUser in WHITELIST:
            logger.info('Say command detected with ' + msg['text'][5:])
            bot.sendMessage(IR2020_CONV, msg['text'][5:])

log.setup_logging()
logger = logging.getLogger(__name__)
logger.info('Starting Bot')
TOKEN = SUPERMAEL_TOKEN
if test:
    TOKEN = TESTING_TOKEN
    logger.info('TESTING MODE---------------------------------------------------------------')
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
logger.info('Listening ......................................................................')

# Keep the program running.
while True:
    time.sleep(10)
