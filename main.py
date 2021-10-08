import os
import logging
import movielinks
import time
from telegram.ext import *
from telegram import *

API_KEY = os.environ.get('API_KEY')
bot = Bot(token=API_KEY)
MLINK = 'https://linkpdisk.com/share-video?videoid='
admin_chat_id1 = 1223296516
admin_chat_id2 = 820893728


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting bot...')

def start_command(update, context):
    text = f'''
    Hello {update.message.chat.username}, Ask movie name without spelling mistakes,
    I can help you to watch that movie.
    Before searching movie name refer the google for movie names and give me name as it is.
    1.Search
    2.Click
    3.Enjoy

    Developed by @NklRockers
    '''
    chat_id = update.message.chat.id

    bot.send_message(chat_id=chat_id, text=text)


def movie(msg, username, chat_id, msg_id):

    movie_name_user_input = msg
    movie_name_user_input = movie_name_user_input.split()
    movie_keys = movielinks.movies_ids.keys()
    try:
        priority_size = 30
        result = {}
        final_result = {}
        for keys in movie_keys:
            movie_name = keys
            keys = keys.split()
            for key in keys:
                for movie_name_user_entered in movie_name_user_input:
                    if movie_name_user_entered == key:
                        priority_size += 30
                    else:
                        pass
            result[movie_name] = priority_size
            priority_size = 30

        priority_range = list(result.values())
        # priority_movie_name = list(result.keys())
        highest_range = max(priority_range)
        if highest_range > 30:
            for key, value in result.items():
                if value not in final_result:
                    final_result[value] = [key]
                else:
                    final_result[value].append(key)

            for name in final_result[highest_range]:
                admin_reply = ''
                for link in movielinks.movies_ids[name]:
                    bot.send_message(chat_id=chat_id, text=MLINK + link, reply_to_message_id=msg_id)
                    if admin_reply != name:
                        
        else:
            keyboard1 = [
                [InlineKeyboardButton('Click Here To Check Spelling', url='https://www.google.com/search?q='+msg+' movie')]
            ]
            keyboard2 = [
                [InlineKeyboardButton('Developed By Anil', url='https://telegram.me/DarlingAnil')]
            ]
            reply_markup1 = InlineKeyboardMarkup(keyboard1)
            reply_markup2 = InlineKeyboardMarkup(keyboard2)
            
            
    except:
       
        

def movie_request(update, context):
    username = update.message.chat.username
    username = str(username)
    msg = update.effective_message.text
    msg = msg.replace('movies', '')
    msg = msg.replace('movie', '')
    msg = msg.replace('links', '')
    msg = msg.replace('link', '')
    msg = msg.replace('files', '')
    msg = msg.replace('file', '')
    # msg = msg.replace(' ', '')
    msg = msg.lower()
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    if msg == '':
        bot.send_message(chat_id=chat_id,text='Please ask the movie name without spelling mistake.', reply_to_message_id = msg_id)
    elif msg == 'hi' or msg == 'hii' or msg == 'hiii' or msg == 'thanks' or msg == 'thank':
        bot.send_message(chat_id=chat_id, text='Please don\'t send like this only ask movie names', reply_to_message_id = msg_id)
    else:
        movie(msg, username, chat_id, msg_id)

def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    Updater = Updater(API_KEY, use_context=True)

    dp = Updater.dispatcher
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(MessageHandler(Filters.text, movie_request))

    dp.add_error_handler(error)
    Updater.start_polling(5)
    Updater.idle()
