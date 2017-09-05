import spotipy
import pylast
import utilities
import datetime


class Collaborator:
    def __init__(self, lastfm_username, spotify_username=None):
        self.lastfmUsername = lastfm_username
        self.spotifyUsername = spotify_username
        self.lastfmNetwork = None
        self.lastfmUser = None
        self.lastfmUserLibrary = None
        self.spotifyUser = None
        self._prepare_collaborator()

    def _prepare_collaborator(self):
        config = utilities.load_config()
        lastfmConfig = config['lastfmConfig']
        # we shouldn't need to be authenticated. We just need their library, nothing else
        self.lastfmNetwork = pylast.LastFMNetwork(api_key=lastfmConfig['lastfmAPIKey'],
                                                  api_secret=lastfmConfig['lastfmAPISecret'])
        self.lastfmUser = self.lastfmNetwork.get_user(self.lastfmUsername)
        self.lastfmUserLibrary = self.lastfmUser.get_library()

        # todo: setup up getting spotify user/library

    def get_last_week_recommendations(self, max_no_tracks=30):
        tracks_to_use = []
        top_tracks = self.lastfmUser.get_top_tracks(period=pylast.PERIOD_7DAYS)
        top_artists = self.lastfmUser.get_top_artists(period=pylast.PERIOD_7DAYS)
        seven_days_ago = datetime.datetime.now().timestamp() - 7 * 24 * 60 * 60;
        loved_tracks = [x for x in self.lastfmUser.get_loved_tracks() if float(x.timestamp) > seven_days_ago]
        return tracks_to_use

