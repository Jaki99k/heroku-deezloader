import requests
import urllib.request

#INIZIO SVILUPPO API DEEZER DA ME ;)
#GIORNO INIZIO 17/10/18 ORE 18:25

host = 'https://api.deezer.com/'

class Client:

    def __init__(self):
        print("*!* DeezLoader Python API *!*\n")

    def search(self, arg): #get indica cosa l'utente vuole ottenere
        return requests.get(host + 'search?q=' + arg).json()

    def show_album_infos(self, arg):
        infos = []
        info = self.search(arg)
        info = info['data'][0]
        infos.append(info['album']['title'])
        infos.append(info['artist']['name'])
        infos.append(info['album']['cover_big'])
        return infos

    def show_track_infos(self, arg):
        infos = []
        info = self.search(arg)
        info = info['data'][0]
        infos.append(info['title'])
        infos.append(info['artist']['name'])
        infos.append(info['album']['cover_big'])
        return infos

    def __list_key_results(self, arg): #Par contiene il tipo di ricerca (track, album, artist)
        it = 0
        keys = []
        info = self.search(arg)['data']
        for x in info:
            if str(info[it]['album']['id']) not in keys:
                keys.append(str(info[it]['album']['id']))
            it += 1
        return keys

    def list_title_results_album(self, arg):
        it = 0
        titles = []
        info = self.search(arg)['data']
        for x in info:
            if str(info[it]['album']['title']) not in titles:
                titles.append(str(info[it]['album']['title']))
            it += 1
        return titles

    def get_album_object(self, arg):
        return requests.get(host + 'album/' + str(self.search(arg)['data'][0]['album']['id'])).json()

    def list_title_results_track(self, arg):
        it = 0
        titles = []
        info = self.search(arg)['data']
        for x in info:
            if str(info[it]['title']) not in titles:
                titles.append(str(info[it]['title']))
            it += 1
        return titles

    def get_track_object(self, arg):
        return requests.get(host + 'track/' + str(self.search(arg)['data'][0]['id'])).json()

    def get_track_link(self, arg):
        return self.get_track_object(arg)['link']

    def get_album_link(self, arg): #arg indica il nome dell'album
        return self.get_album_object(arg)['link']

    def get_album_title(self, arg):
        return self.get_album_object(arg)['title']

    def get_track_from_album_to_list(self, arg):
        tracks = []
        conta = 0
        for x in range(int(self.get_album_object(arg)['nb_tracks'])):
            tracks.append(self.get_album_object(arg)['tracks']['data'][conta]['title'])
            conta += 1

        return tracks

    def get_track_from_album(self, arg):
        conta = 0
        for x in range(int(self.get_album_object(arg)['nb_tracks'])):
            print(self.get_album_object(arg)['tracks']['data'][conta]['title'])
            conta += 1


    #Funzione per download delle cover con relativa scelta della dimensione delle stesse
    def get_album_cover(self, arg, size): #aggiungere poi path per salvare
        if size == 'small':
            name = 'cover_' + arg.lower() + '_' + size.lower() + '.jpg'
            return urllib.request.urlretrieve(str(self.get_album_object(arg)['cover_small']), name)
        elif size == 'medium':
            name = 'cover_' + arg.lower() + '_' + size.lower() + '.jpg'
            return urllib.request.urlretrieve(str(self.get_album_object(arg)['cover_medium']), name)
        elif size == 'big':
            name = 'cover_' + arg.lower() + '_' + size.lower() + '.jpg'
            return urllib.request.urlretrieve(str(self.get_album_object(arg)['cover_big']), name)
        elif size == 'xl':
            name = 'cover_' + arg.lower() + '_' + size.lower() + '.jpg'
            return urllib.request.urlretrieve(str(self.get_album_object(arg)['cover_xl']), name)
        else:
            print("Expected small, medium, big or xl in size")

    def get_album_tracks(self, arg):
        return self.get_album_object(arg)['tracks']
