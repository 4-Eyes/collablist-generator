from data import Collaborator
from random import shuffle
import sys
import argparse


def run(args):
    # create all collaborators
    primary_collaborator = Collaborator(args.collaborators[0], args.spotify[0])
    print("loading first collaborator's data...")
    songs = primary_collaborator.get_last_week_tracks(args.maxTracks, args.minTrackPlayCount, args.minArtistPlayCount,
                                                      args.maxArtistTopTracks, args.maxTopTracks, args.maxTopArtists)
    for i, collaborator in enumerate(args.collaborators[1:]):
        print("loading the {0}{1} collaborator's data...".format(i + 2, {2: "nd", 3: "rd"}.get(i+2, "th")))
        c = Collaborator(collaborator, spotify_api=primary_collaborator.spotify)
        songs = songs | c.get_last_week_tracks(100, 2, 4, 2)
    print("creating new playlist...")
    playlist_id = primary_collaborator.create_new_playlist(args.name[0])
    print("adding tracks to playlist...")
    shuffled_ids = list(set([song.spotify_id for song in songs]))
    shuffle(shuffled_ids)
    primary_collaborator.add_songs_to_playlist(playlist_id, shuffled_ids[:80])
    print("Finished!!!")
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a collaborative playlist from last.fm data')
    parser.add_argument('collaborators', metavar='C', nargs='+', help='a collaborator for the playlist, this should be their last.fm account user name')
    parser.add_argument('-s', '--spotify', metavar='s', help='the user name to use for the spotify processing', nargs=1, required=True)
    parser.add_argument('-n', '--name', metavar='n', help='the name of the playlist to be generated', nargs=1, required=True)
    parser.add_argument('-mt', '--maxTracks', metavar='mt', help='the max number of tracks to get from each collaborator for the last week. Defaults to 30', type=int, default=30)
    parser.add_argument('-mtpc', '--minTrackPlayCount', metavar='mtpc', help='the minimum number of times a track must have been played in the last week to be included in the top tracks. Defaults to 3', type=int, default=3)
    parser.add_argument('-mapc', '--minArtistPlayCount', metavar='mapc', help='the minimum number of times an artist must have been played to be included in the top artists for the week. Defaults to 10', type=int, default=10)
    parser.add_argument('-matt', '--maxArtistTopTracks', metavar='matt', help='the maximum number of top tracks to take from top artists when getting weekly data. Defaults to 2', type=int, default=2)
    parser.add_argument('-mtt', '--maxTopTracks', metavar='mtt', help='the maximum number of top tracks to pull from last.fm. Defaults to 150', type=int, default=150)
    parser.add_argument('-mta', '--maxTopArtists', metavar='mta', help='the maximum number of top artists to pull from last.fm. Defaults to 50', type=int, default=50)
    run(parser.parse_args(sys.argv[1:]))
