import spotipy
import pylast


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

        # we shouldn't need to be authenticated. We just need their library, nothing else
        self.lastfmNetwork = pylast.LastFMNetwork()
        self.lastfmUser = self.lastfmNetwork.get_user(self.lastfmUsername)
        self.lastfmUserLibrary = self.lastfmUser.get_library()

        # todo: setup up getting spotify user/library

    def get_last_week_recommendations(self):
