"""
Boddz @ <https://github.com/boddz/next-in-queue>

A local module to help assist with getting the next Spotify track in a user's
currently playing queue. Contains class and helper methods/ properties for
doing so.

To be released under an MIT license.

Please refer to the project source tree for more information on this.
"""


from __future__ import annotations

import traceback
from sys import version_info
from random import randint
from time import sleep

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


assert version_info >= (3, 9), "Please use Python 3.9 or higher!"


VALID_SCOPES_LIST = [
    # Pick and choose which perms you need here for development.
    "ugc-image-upload",
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "app-remote-control",
    "streaming",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public",
    "user-follow-modify",
    "user-follow-read",
    "user-read-playback-position",
    "user-top-read",
    "user-read-recently-played",
    "user-library-modify",
    "user-library-read",
    "user-read-email",
    "user-read-private"
]


class Client:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str,
                 perm_scopes: str | list = []) -> None:
        self.__client_id = client_id
        self.__client_secret = client_secret
        self.__redirect_uri = redirect_uri
        self.__perm_scopes = perm_scopes
        self.__cred_mgr = SpotifyClientCredentials(client_id, client_secret)
        _oauth = SpotifyOAuth(client_id, client_secret, redirect_uri,
                                    scope=perm_scopes)
        _resp = _oauth.get_cached_token() if _oauth.get_cached_token()       \
               is not None else _oauth.get_access_token(as_dict=False)
        self.__token = _resp if type(_resp) == str else _resp["access_token"]
        self.__spotipy_obj = spotipy.Spotify(
            auth = self.__token,
            client_credentials_manager=self.__cred_mgr
        )

    @property
    def client_id(self) -> str:
        return self.__client_id

    @property
    def client_secret(self) -> str:
        return self.__client_secret

    @property
    def redirect_uri(self) -> str:
        return self.__redirect_uri

    @property
    def token(self) -> str:
        return self.__token

    @property
    def spotify_obj(self) -> Spotipy:
        return self.__spotipy_obj

    @property
    def _currently_playing_json(self) -> json | dict:
        return self.spotify_obj.current_user_playing_track()

    @property
    def _current_track_json(self) -> json | dict:
        return self._currently_playing_json["item"]

    @property
    def current_track_name(self) -> str:
        return self._current_track_json["name"]

    @property
    def current_playlist_id(self) -> str:
        """
        Parse the playlist ID from the playlist URI using above json data
        for what the user is currently playing.
        """
        return self._currently_playing_json["context"]["uri"][17:]

    @property
    def _current_playlist_json(self) -> json | dict:
        """
        Get the full json response containing playlist data using the
        previously parsed playlist ID.
        """
        return self.spotify_obj.playlist_tracks(self.current_playlist_id)

    @property
    def _current_queue_json(self) -> json | dict:
        """
        Get the full json response containing the current queues data.
        """
        return self.spotify_obj.queue()

    @property
    def get_next_in_queue(self) -> str:
        """
        Simply get the name of the next track that is in the current queue.

        This work around for getting next in queue is reliable and works
        in combination with shuffle play :).

        Will print the traceback for exception if one is encountered and then
        return string saying nothing is next in queue.

        FYI Future Me
        -------------
        The queue shuffles, not the playlist its self, so the
        'next-in-playlist' 'hack' will still work fine, well if it is not
        sorted in a way other than default.
        """
        try: return self._current_queue_json["queue"][0]["name"]
        except:
            traceback.print_exc()
            return "\nNothing is next, no current queue perhaps."

    @property
    def _recommended_genre_seeds_list(self) -> list:
        return self.spotify_obj.recommendation_genre_seeds()["genres"]

    def _get_recommended_track_ids(self, track_id: str) -> list:
        rs = self.spotify_obj.recommendations(seed_tracks=track_id, limit=100)
        return [i["id"] for i in rs["tracks"]]

    @staticmethod
    def _pick_random_track_id_from_list(track_ids: list) -> str:
        """
        Grab a track ID in the specified track ID's list. 1 - 100 range.

        I will not bother with exception handle here as it is kind of rare you
        would need this.
        """
        return track_ids[randint(0, 100)]

    def add_list_of_track_ids_to_playlist(self, playlist_id: str,
                                           track_ids: list,
                                           repeat: int=None,
                                           sleep_interval: int=5) -> None:
        """
        Add 100 tracks to a specified playlist either 1x or *x. This shouldn't
        add that many duplicate tracks, but it is up to what Spotify
        recommends, I tried to add some randomness to help with this and
        to spice up the track a tad bit more.

        Requires 1 - 5 track IDs to be entered in list form for this to work.

        I would leave `sleep_interval` as 5 as this will not spam the Spotify
        API then and risk you getting rate limited.
        """
        _user = self.spotify_obj.me()
        _initial_ids = self._get_recommended_track_ids(track_ids)
        if repeat is None:
            self.spotify_obj.user_playlist_add_tracks(_user, playlist_id,
                                                      _initial_ids)
        else:
            assert type(repeat) == int and not None, "Please use an int here."
            for i in range(repeat):
                print(f"Sweep: {i + 1} >> tracks added: {(i + 1) * 100}")
                if i == 0: _ids = self._get_recommended_track_ids(track_ids)
                else: _ids = self._get_recommended_track_ids(
                    [self._pick_random_track_id_from_list(_initial_ids)]
                )
                self.spotify_obj.user_playlist_add_tracks(_user, playlist_id,
                                                          _ids)
                sleep(sleep_interval)


if __name__ == "__main__":
    ...
