from data import Collaborator
from random import shuffle
import sys
import argparse


def run(args):
    # create all collaborators
    primary_collaborator = Collaborator(args.collaborators[0], args.spotify[0])
    print("loading first collaborator's data...")
    songs = primary_collaborator.get_last_week_tracks(100, 2, 4, 2)
    for i, collaborator in enumerate(args.collaborators[1:]):
        print("loading the {0}{1} collaborator's data...".format(i + 2, {2: "nd", 3: "rd"}.get(i+2, "th")))
        c = Collaborator(collaborator, spotify_api=primary_collaborator.spotify)
        songs = songs | c.get_last_week_tracks(100, 2, 4, 2)
    print("creating new playlist...")
    playlist_id = primary_collaborator.create_new_playlist('A Test Playlist')
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
    run(parser.parse_args(sys.argv[1:]))
