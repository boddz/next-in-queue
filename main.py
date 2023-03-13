#!/usr/bin/env python3

from src import client


def main() -> None:
    YOUR_APPLICATION_CLIENT_ID = "REDACTED"
    YOUR_APPLICATION_CLIENT_SECRET = "REDACTED"
    # The redirect can just be anything with valid link format, just make sure
    # the link that is here matches the one you entered on the app you made.
    YOUR_APPLICATION_REDIRECT_URI = "http://127.0.0.1:9090"

    # NOTE: end-users, just ignore below code & add your credentials above. 

    # Build a client with custom class `src.client.Client` & set needed perms.
    spotify_client = client.Client(
        YOUR_APPLICATION_CLIENT_ID,
        YOUR_APPLICATION_CLIENT_SECRET,
        YOUR_APPLICATION_REDIRECT_URI ,
        client.VALID_SCOPES_LIST[3]
    )

    print(f"Next in Queue: {spotify_client.get_next_in_queue}")


if __name__ == "__main__":
    main()
