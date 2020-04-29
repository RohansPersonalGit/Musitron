import requests
import csv
import json
import os

spotify_base_api = "https://api.spotify.com/v1/"
audio_features_path = "audio-features/"
search_path = "search?q={song_name}%20year:{song_year}&type={song_type}&limit=2"
search_param_delim = "%20"
search_param_year = "year"

class audio_object:
    def __init__(self, duration_ms, key, mode, time_signature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valency, tempo):
        self.duration_ms = duration_ms
        self.key = key
        self.mode = mode
        self.time_signature = time_signature
        self.acousticness = acousticness
        self.dannceability = danceability
        self.energy = energy
        self.instr = instrumentalness
        self.liveness = liveness
        self.loudness = loudness
        self.speechiness = speechiness
        self.valency = valency
        self.temp = tempo


class SpotifyClient:
    def __init__(self, token):
        self.failed_requests = []
        self.good_requests = []
        self.token_header = {"Authorization": token}
        self.good_audio_features = []
        self.failed_audio_features = []

    def get_song_features(self, id):
        search_response = requests.request('GET', spotify_base_api + audio_features_path + id,
                                           headers=self.token_header)
        if search_response.status_code is 200:
            resp_json = search_response.json()
            obj = audio_object(resp_json['duration_ms'], resp_json['key'], resp_json['mode'], resp_json['time_signature'], resp_json['acousticness'], resp_json['danceability'], resp_json['energy'], resp_json['instrumentalness'], resp_json['liveness'], resp_json['loudness'], resp_json['speechiness'], resp_json['valence'], resp_json['tempo']).__dict__
            print(obj)
            self.good_audio_features.append(obj)
        else:
            self.failed_audio_features.append(id)

    def search_song_by_year(self, song_name, song_type, song_year):
        search_response = requests.request('GET', spotify_base_api + search_path.format(song_name=song_name,
                                                                                        song_type=song_type,
                                                                                        song_year=song_year),
                                           headers=self.token_header)
        print(search_response.json())
        if search_response.status_code is 200:
            try:
                resp_json = search_response.json()['tracks']['items'][0]
                trimmed_json = {'name': resp_json['name'],'id': resp_json['id']}
            except IndexError as e:
                print(e)
                self.failed_requests.append({'name':song_name, 'year': song_year})
                return
            self.good_requests.append(trimmed_json)
        else:
            self.failed_requests.append({'name':song_name, 'year': song_year})




def quick_and_dirty_data_clean():
    new_Response_list = []
    faild_response_list = []
    with open('spotify_search_response_good.json', 'r') as f:
        data = f.read()
        response_jsons = json.loads(data)
        for each in response_jsons:
            try:
                each = each['tracks']['items'][0]
            except IndexError as e:
                print(e)
                faild_response_list.append(each)
                continue
            trimed_track = {'id': each['id'], 'name':each['name']}
            new_Response_list.append(trimed_track)
    with open('good_search_resposne/trimed_tracks_good_response.json', 'w') as f:
        json.dump(new_Response_list,f)
    with open('trimed_tracks_gbad_response.json', 'w') as f:
        json.dump(faild_response_list,f)

def parse_songs():
    client = SpotifyClient('Bearer BQAL2fnRQZUdU83b44XzWfiYCzHe6WGRfyNvz5lTkv9MiwB04gMsGASl8W6ZP74U-aHaCOKu2RDU8pJUtfY')
    song_listt = []
    with open('./songlibraryfailed.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            client.search_song_by_year(row[0], 'track', row[7])
        with open('good_search_resposne/spotify_search_response_good2.json', 'w') as f:
            json.dump(client.good_requests, f)
        with open('./failed_requests2.json', 'w') as f:
            json.dump(client.failed_requests, f)

def parse_failed_requests():
    #insert songs here
    client = SpotifyClient('Bearer ')
    with open('./failed_requests.json', 'r') as f:
        data = f.read()
        failed_responses = json.loads(data)
        for each in failed_responses:
            client.search_song_by_year()

def quick_and_diry_song_audio_feature_getter():
    client = SpotifyClient('Bearer BQAL2fnRQZUdU83b44XzWfiYCzHe6WGRfyNvz5lTkv9MiwB04gMsGASl8W6ZP74U-aHaCOKu2RDU8pJUtfY')
    for each in os.listdir('./good_search_resposne'):
        print(each)
        with open('./good_search_resposne/' + each,'r') as f:
            data = f.read()
            songs = json.loads(data)
            for each in songs:
                client.get_song_features(each['id'])
    with open('./audioanalysismysongs.json', 'w') as f:
        json.dump(client.good_audio_features, f)
    with open('./badaudioanalysismysongs.json', 'w') as f:
        json.dump(client.failed_audio_features, f)

def main():
    quick_and_diry_song_audio_feature_getter()


if __name__ == "__main__":
    main()
