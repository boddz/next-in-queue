"""
Boddz @ <https://github.com/boddz/next-in-queue>

A local module to help assist with getting the next Spotify track in a user's
currently playing queue. Contains class and helper methods/ properties for
doing so.

To be released under 'The Unlicense'.

Please refer to the project source tree for more information on this.
"""


from __future__ import annotations

import traceback
from sys import version_info

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


if __name__ == "__main__":
    ...
