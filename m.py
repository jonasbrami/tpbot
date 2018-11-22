from telegram.ext import Updater
from subprocess import check_output
import subprocess
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import unidecode
import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

today = datetime.now().date()
yesterday=(datetime.now()-timedelta(1)).date()

def session_get_to_soup_wrapper(url,session):
    r = session.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    while True:
            try:
                if soup.find("").__len__():
                    break
                r = session.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')
            except AttributeError:
                r = session.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')

   #     print(soup.find("a"))

    return soup

def page_to_tg(update,soup):
    print('page_to_tg')
    comment_url = 'http://uj3wazyk5u4hnvtk.onion/static/img/icon_comment.gif'
    res= "-------- TORRENT LIST --------\n\n\n"
    count=0
    for torrent in soup.select("table > tr"):


            try:
                temp_metadata = unidecode.unidecode(torrent.find(class_="detDesc").get_text())
            except AttributeError:
                continue

            turl = 'http://uj3wazyk5u4hnvtk.onion' + torrent.find(class_="detLink").get('href')
            #print(turl)
            tname=torrent.find(class_="detLink").get_text()
            try:
                magnet=torrent.find(title="Download this torrent using magnet").get('href')
            except Exception as e:
                magnet='NOT AVAILABLE'
            try:
                uname = unidecode.unidecode(torrent.select("font > a")[0].get_text())
            except IndexError:
                uname = 'Anonymous'

            uploaded=temp_metadata.partition(',')[0][9:]
            uploaded_param=uploaded.partition(' ')
            if(uploaded_param[0]=='Today' or uploaded_param[2][0:4]=='mins'):
                uploaded=today
            elif uploaded_param[0]=='Y-day':
                uploaded = yesterday
            elif uploaded_param[2].__len__()==4:
                uploaded=uploaded_param[2]+'-'+uploaded_param[0]
            else:
                uploaded='2018'+'-'+uploaded_param[0]



            seeders=torrent.select("td:nth-of-type(3)")[0].get_text()
            leechers=torrent.select("td:nth-of-type(4)")[0].get_text()

            try:
                comments=torrent.find(src=comment_url).get('alt')[17:].partition(' ')[0]
            except AttributeError:
                comments=0


            tsize = temp_metadata.partition(',')[2].partition(',')[0][6:]
            tsize=tsize.__str__()

            if torrent.find_all(alt='Trusted').__len__()==1:
                ranku = 'Trusted'
            elif torrent.find_all(alt='VIP').__len__()==1:
                ranku='VIP'
            else:
                ranku='NO RANK'
            print(tname+uname+tsize+ranku+uploaded)
            count = count + 1
            if count % 5 == 0:
                update.message.reply_text(res)
                res="'\n"

            res+='Name: '+ tname + '\n'+ 'Uploader: '+ uname+' Rank: '+ranku +'\n'+ 'size: '+tsize+ '\n'+'Uploaded: '+uploaded+'\n'+'Seeders: '+seeders+' Leechers: '+leechers+'\n'+ magnet + '\n\n\n'
    update.message.reply_text(res)


CATEGORY, MOVIE, MOVIE_D, TV_SHOW,TV_SHOW_D, MUSIC,MUSIC_D = range(7)


def tpb(bot,update):
    reply_keyboard = [['Movie', 'TV_Show', 'Music']]
    update.message.text
    update.message.reply_text(
        'Welcome to MGB, please chose a category',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CATEGORY

def goToMovie(bot,update):
    update.message.reply_text('enter the title')
    return MOVIE

def goToTVShow(bot,update):
    update.message.reply_text('enter the title')
    return TV_SHOW

def goToMusic(bot,update):
    update.message.reply_text('enter the title')
    return MUSIC

def getMovies(bot,update):
    print(update.message.text)
    page_url="http://uj3wazyk5u4hnvtk.onion/search/"+update.message.text+"/0/99/201"
    session = requests.session()
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    soup=session_get_to_soup_wrapper(page_url,session)
    page_to_tg(update,soup)
    update.message.reply_text('Enter a valid magnet')
    return MOVIE_D

def getTVShows(bot,update):
    print(update.message.text)
    page_url="http://uj3wazyk5u4hnvtk.onion/search/"+update.message.text+"/0/99/205"
    session = requests.session()
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    soup=session_get_to_soup_wrapper(page_url,session)
    page_to_tg(update,soup)
    update.message.reply_text('Enter a valid magnet')
    return TV_SHOW_D

def getMusics(bot,update):
    print(update.message.text)
    page_url="http://uj3wazyk5u4hnvtk.onion/search/"+update.message.text+"/0/99/101"
    session = requests.session()
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    soup=session_get_to_soup_wrapper(page_url,session)
    page_to_tg(update,soup)
    update.message.reply_text('Enter a valid magnet')
    return MUSIC_D

def download_movie_from_magnet(bot,update):
    update.message.reply_text('DL started')
    cmd="transmission-remote localhost:1234 --auth=user:passwords -w '/home/username/download/movies' -a "+ update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=check_output(cmd, stderr=subprocess.STDOUT, shell=True))
    return ConversationHandler.END

def download_TVShow_from_magnet(bot,update):
    update.message.reply_text('DL started')
    cmd="transmission-remote localhost:1234 --auth=user:password -w '/home/username/download/series' -a "+ update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=check_output(cmd, stderr=subprocess.STDOUT, shell=True))
    return ConversationHandler.END

def download_Music_from_magnet(bot,update):
    update.message.reply_text('DL started')
    cmd="transmission-remote localhost:1234 --auth=user:password -w '/home/username/download/Music' -a "+ update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=check_output(cmd, stderr=subprocess.STDOUT, shell=True))
    return ConversationHandler.END

def cancel(bot,udpate):
    return ConversationHandler.END

updater = Updater(token='728641004:AAGIZlG8_XlBPI8kY67rw6B-LqovIwiHa7I')

dispatcher = updater.dispatcher

tpb_handler = ConversationHandler(

        entry_points=[CommandHandler('tpb', tpb)],

        states={
            CATEGORY:  [RegexHandler('^(Movie)$', goToMovie),
                        RegexHandler('^(TV_Show)$', goToTVShow),
                        RegexHandler('^(Music)$', goToMusic)],

            MOVIE: [MessageHandler(Filters.text, getMovies)],

            MOVIE_D: [RegexHandler('^(magnet:?)', download_movie_from_magnet)],

            TV_SHOW: [MessageHandler(Filters.text, getTVShows)],

            TV_SHOW_D: [RegexHandler('^(magnet:?)', download_TVShow_from_magnet)],

            MUSIC: [MessageHandler(Filters.text, getMusics)],

            MUSIC_D: [RegexHandler('^(magnet:?)', download_Music_from_magnet)]

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

dispatcher.add_handler(tpb_handler)

updater.start_polling()




