import spotipy
import spotipy.util
from spotipy.oauth2 import SpotifyOauthError
import pylast
import utilities
import datetime
from random import shuffle


class Collaborator:
    def __init__(self, lastfm_username, spotify_username=None, spotify_api=None, spotify_scopes='user-library-read'):
        self.lastfmUsername = lastfm_username
        self.spotifyUsername = spotify_username
        self.lastfmNetwork = None
        self.lastfmUser = None
        self.lastfmUserLibrary = None
        self.spotify = spotify_api
        self.spotifyToken = None
        self.spotifyScopes = spotify_scopes
        self._prepare_collaborator()

    def _prepare_collaborator(self):
        config = utilities.load_config()
        lastfm_config = config['lastfmConfig']
        spotify_config = config['spotifyConfig']
        # we shouldn't need to be authenticated. We just need their library, nothing else
        self.lastfmNetwork = pylast.LastFMNetwork(api_key=lastfm_config['lastfmAPIKey'],
                                                  api_secret=lastfm_config['lastfmAPISecret'])
        self.lastfmUser = self.lastfmNetwork.get_user(self.lastfmUsername)
        self.lastfmUserLibrary = self.lastfmUser.get_library()

        if self.spotifyUsername is not None and self.spotify is None:
            try:
                # todo: work out if it's possible to automate this? I hate the spotify API authentication
                self.spotifyToken = spotipy.util.prompt_for_user_token(self.spotifyUsername, self.spotifyScopes,
                                                                       spotify_config['spotifyClientId'],
                                                                       spotify_config['spotifyClientSecret'],
                                                                       spotify_config['redirectURI'])
                self.spotify = spotipy.Spotify(auth=self.spotifyToken)
            except SpotifyOauthError:
                print("Failed to set up spotify user")

    def _valid_spotify_track(self, track):
        if self.spotify is None:
            # if we haven't got an authorised spotify api object we cannot validate the track
            # todo: determine if this should throw an exception
            return False, None
        # search for the track on spotify
        # todo: enable reauthorising here if necessary
        search_results = self.spotify.search(q=track.title + " artist:" + track.artist.name, type='track')
        # filter search results logically and then return a tuple of if it's valid and the id of the track on spotify
        sr_len = len(search_results['tracks']['items'])

        if sr_len == 1:
            return True, search_results['tracks']['items'][0]['id']
        for result in search_results['tracks']['items']:
            if len([x for x in result['artists'] if track.artist.name.lower() in x['name'].lower()]) > 0:
                return True, result['id']
        return False, None

    def get_last_week_tracks(self, max_no_tracks=30, minimum_track_play_count=3, minimum_artist_play_count=10,
                             max_artist_top_tracks=2):
        tracks = set()
        # get the top tracks for the week
        top_tracks = [t.item for t in self.lastfmUser.get_top_tracks(period=pylast.PERIOD_7DAYS, limit=150)
                      if int(t.weight) >= minimum_track_play_count]
        # get the top artists for the week
        top_artists = [a.item for a in self.lastfmUser.get_top_artists(period=pylast.PERIOD_7DAYS, limit=50)
                       if int(a.weight) >= minimum_artist_play_count]
        # grab some tracks from the top played artist
        top_artist_tracks = []
        for artist in top_artists:
            top_artist_tracks += [t.item for t in artist.get_top_tracks()[:max_artist_top_tracks]]

        # get tracks loved within the last week
        seven_days_ago = datetime.datetime.now().timestamp() - 7 * 24 * 60 * 60
        loved_tracks = [x.track for x in self.lastfmUser.get_loved_tracks() if float(x.timestamp) > seven_days_ago]

        # shuffled all tracks and return the as many tracks as possible
        shuffled_tracks = top_tracks + loved_tracks + top_artist_tracks
        shuffle(shuffled_tracks)
        used_artists = {}
        while len(tracks) < max_no_tracks and len(shuffled_tracks) > 0:
            track_to_add = shuffled_tracks.pop()
            # check the track is valid
            valid, spotify_id = self._valid_spotify_track(track_to_add)
            if valid and track_to_add.artist.name not in used_artists:
                used_artists[track_to_add.artist.name] = True
                # if the track is valid stick the spotify id on the object and add it to the tracks
                track_to_add.spotify_id = spotify_id
                tracks.add(track_to_add)
        return tracks

# uncomment for testing
# c = Collaborator() # fill in the usernames here
# tracks = c.get_last_week_tracks(100, 1, 4)
