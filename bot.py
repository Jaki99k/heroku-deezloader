import deezloader
import os
import urllib.request
import glob
import telepot
import telegram
from client import Client
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

client = Client()
dw = deezloader.Login("jaki99kofficial@gmail.com", "camillo01")
global typeDown
typeDown = []

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)

	global mex
	global search

	keyboard = [[[]]]
	search = bot.getUpdates()[0]['message']['text']
	#print(search)

	start = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text="🔍 Cerca", callback_data="search"),]])

	if content_type == 'text':
		if len(typeDown) > 0:
			if typeDown[0] == 'album' and search[0] != '🎵': 
				infos = client.list_title_results_album(search)
				#print(infos)
				cont = 0
				for x in range(len(infos)-1):
					keyboard[0].append([KeyboardButton(text='🎵'+str(infos[cont]))])
					cont += 1
				bot.sendMessage(chat_id, "Scegli uno dei risultati elencati qui sotto : ", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard[0]))

			if typeDown[0] == 'track' and search[0] != '🎵':
				infos = client.list_title_results_track(search)
				cont = 0
				for x in range(len(infos)-1):
					keyboard[0].append([KeyboardButton(text='🎵'+str(infos[cont]))])
					cont += 1
				bot.sendMessage(chat_id, "Scegli uno dei risultati elencati qui sotto : ", reply_markup=ReplyKeyboardMarkup(keyboard=keyboard[0]))


		if search[0] == '🎵' and typeDown[0] == 'album': 
			print("Starting Download ...")
			track = search[1:]
			link = client.get_album_link(track)
			dw.download_albumdee(link, output="./", check=False)
			print("Download of Album " + track + " finished!")
			album_infos = client.show_album_infos(track)
			photo = urllib.request.urlopen(str(album_infos[2]))
			bot.sendPhoto(chat_id, ("cover.jpg", photo), caption="👨‍🎤 <b>Artist : </b>" + str(album_infos[1]) +'\n\n' + '🎶 <b>Album name : </b>' + str(album_infos[0]), parse_mode='HTML')
			nameTracksAlbum = glob.glob(track + '/*.mp3')
			i = 0
			for x in nameTracksAlbum:
				print("Sending to target ", nameTracksAlbum[i])
				bot.sendDocument(chat_id, document=open(nameTracksAlbum[i], 'rb'))
				i += 1
			#os.system("rm -r " + search[1:]) Problema in caso titolo con spazi! *!* DA RISOLVERE *!*
		elif search[0] == '🎵' and typeDown[0] == 'track':
			print("Starting Download ...")
			track = search[1:]
			link = client.get_track_link(track)
			dw.download_trackdee(link, output="./", check=False)
			print("Download of track " + track + " finished!")
			track_infos = client.show_track_infos(track)
			photo = urllib.request.urlopen(str(track_infos[2]))
			bot.sendPhoto(chat_id, ("cover.jpg", photo), caption="👨‍🎤 <b>Artist : </b>" + str(track_infos[1]) + '\n\n' + '🎶 <b>Album name : </b>' + str(track_infos[0]), parse_mode='HTML')
			nameTrack = glob.glob(str(track_infos[1]) + '/*.mp3')
			i = 0
			print("Sending to target ", nameTrack[0])
			bot.sendDocument(chat_id, document=open(nameTrack[0], 'rb'))

		if msg['text'] == '/start':
			mex = bot.sendMessage(chat_id, "Benvenuto, clicca il pulsante ricerca per iniziare!", reply_markup=start, parse_mode='HTML')

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    typeOfSearch = InlineKeyboardMarkup(inline_keyboard=[
    	[InlineKeyboardButton(text="🎶 Ricerca Album", callback_data="searchalbum"),
    	InlineKeyboardButton(text="💿 Ricerca Traccia", callback_data="searchtrack")],
    	[InlineKeyboardButton(text="👨‍🎤 Ricerca Artista", callback_data="searchartist")]])

    backMenu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Torna al menu", callback_data="backmenu")]])

    if query_data == 'search':
    	choice = bot.editMessageText(telepot.message_identifier(mex), text="Scegli con che criterio cercare la musica", reply_markup=typeOfSearch)
    if query_data == 'searchalbum':
    	choice = bot.editMessageText(telepot.message_identifier(mex), text="Ok, cerchero per <b>🎶 Album!</b>\n✒ Inserisi il nome da ricercare", reply_markup=backMenu, parse_mode='HTML')
    	typeDown.append('album')
    if query_data == 'searchtrack':
    	choice = bot.editMessageText(telepot.message_identifier(mex), text="Ok, cherchero per <b>💿 Traccia!</b>\n✒ Inserisci il nome da ricercare", reply_markup=backMenu, parse_mode='HTML')
    	typeDown.append('track')

TOKEN = "632800680:AAGv3jX7eAxF69KUXUx2uMksfW7VUFBoVQE"
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})

import time
while 1:
    time.sleep(10)

