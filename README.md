# Spotify Next in Queue Script

A script/ local module to get the song that is next in a user's current queue.

Created for a friend to use for a twitch bot or something.

To be released under 'The Unlicense', use this however you want, I mainly did
this for a bit of fun.


## Prerequisites

(Written and tested on Python 3.11, anything above 3.9 should do though)

I would recommend setting up a virtual environment to avoid dependency
contamination, although this is optional:

```bash
# Linux w/ bash shell: 
python3 -m venv venv && source venv/bin/activate

# Windows 10 w/ powershell:
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
./venv/Scripts/activate.ps1
```

Install requirements using pip:

```bash
pip install -r requirements.txt

# Or like this:
python3 -m pip install -r requirements.txt
```


## Use

Next in Queue & Crawl Recommeded Tracks

### Next in Queue

First, and this is very important to actually be granted access to Spotify's
API; create an application at the
[Spotify dev dashboard](https://developer.spotify.com/dashboard/applications)
once done, edit it and set it's redirect URL to `http://127.0.0.1:9090` and
then save the changes. Once you have done that, copy the client ID & client
secret into the redacted slots in the main.py file.
<b>These steps are crucial</b>.

If done correct, a brief popup will open in your default browser to grab the
required token code to access your account info that is needed
(in this case, it just needs your currently playing information) and the rest
should just work, your next in queue will be pretty printed.

Once that is done simply do the following:

```bash
python3 main.py  # Once all prerequisites are met.
```

### Crawl Recommended Tracks

There is a sub-script in this project called `crawl.py`. It will take an
initial track ID and the user's playlist ID on their account that they want
to append tracks to and add tracks two it randomized, suggested by Spotify
that are similar to the original track (track ID).

Just update your details like the next in track script and run it the same.


## Closing Note

The local module `src.client` contains stuff for you to get next in queue
information if you just want the raw data.

Enjoy! ~
