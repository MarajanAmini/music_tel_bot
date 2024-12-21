import requests
from telegram import Update
from telegram.ext import Application,CommandHandler,CallbackContext


class Track:
    def __init__(self,name,artist,album,track_url):
        self.name = name 
        self.artist = artist
        self.album = album
        self.track_url = track_url

    def __str__(self):
        return f"name:{self.name}\nartist:{self.artist}\nalbum:{self.album}\n{self.track_url}"

class TrackFetcher:
    def __init__(self,url):
        self.url = url
        self.tracks = [] 

    def request_api(self):
        response = requests.get(self.url) 
        if response.status_code == 200:
            return response.json()
        return []      

    @staticmethod
    def read_data(track):
        name = track.get("trackName","No name")
        artist = track.get("artistName"," unknown artist")
        album = track.get ("collectionName","unKnown collection")
        url = track.get("previewUrl","No url!")
        return name,artist,album,url


    def create_track_object (self):
        response = self.request_api()
        if not response:
            print("No result found!")
            return
        for track in response["results"]:
            name,artist,album,url = self.read_data(track)
            track1 = Track(name,artist,album,url)
            self.tracks.append(track1)

async def start(update:Update,context :CallbackContext):
    await update.message.reply_text("welcome to robot ")

async def all(update:Update,context:CallbackContext):
    search_word = input("inter a name af track:")
    url = f"https://itunes.apple.com/search?term={search_word}&media=music"
    abj1 = TrackFetcher(url)
    abj1.create_track_object()
    for track in abj1.tracks[:10]:
        await update.message.reply_text(str(track))

async def one_track(update:Update,context:CallbackContext):
    search_word = input("inter a name af track:")
    url = f"https://itunes.apple.com/search?term={search_word}&media=music"
    abj1 = TrackFetcher(url)
    abj1.create_track_object()
    await update.message.reply_text(str(abj1.tracks[0]))


if __name__ == "__main__":
    TOKEN = ""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start",start))
    application.add_handler(CommandHandler("all",all))
    application.add_handler(CommandHandler("one",one_track))

    application.run_polling()


