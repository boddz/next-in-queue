#!/usr/bin/env python3

"""
Crawl and get recommended genres/artists and dump their songs into a playlist.
"""

from src import client


def main() -> None:
    # NOTE: where redacted, add your own information: client ID + secret.
    YOUR_APPLICATION_CLIENT_ID = "REDACTED"
    YOUR_APPLICATION_CLIENT_SECRET = "REDACTED"
    YOUR_APPLICATION_REDIRECT_URI = "http://127.0.0.1:9090"

    spotify_client = client.Client(
        YOUR_APPLICATION_CLIENT_ID,
        YOUR_APPLICATION_CLIENT_SECRET,
        YOUR_APPLICATION_REDIRECT_URI,
        client.VALID_SCOPES_LIST[7:10],
    )

    # NOTE: you need to add your own playlist ID on your account here.
    # Adds 100 similar tracks from an original track ID that was entered.
    spotify_client.add_list_of_track_ids_to_playlist(
        # ID's for playlist, albums, artist & tracks can be found in URI
        # at the top of you browser.
        "2rRFvUBPDKuARVvvsI7Jjk",  # Your playlist ID to add tracks to.
        ["78Y9lEFTSCHpnPPLfQ8UXp"],  # The list of track IDs to seed (1 - 5).
        45  # The number of times to repeat this process. Can be `None`.
        )


if __name__ == "__main__":
    main()
