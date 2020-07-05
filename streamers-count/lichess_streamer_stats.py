#!/usr/bin/env python3

""" Automate gathering of information about current streamers. """

# System imports.
import json
import pathlib
import requests
import sys
import time

# Package imports.
import berserk

# Path to this script.
THIS_SCRIPT = pathlib.Path(__file__).parent.resolve()

STREAMERS_FILE = THIS_SCRIPT / "streamers.json"


def update_streamers_file(new_info):
    """ Update the streamers file. """
    data = {}
    if STREAMERS_FILE.exists():
        with STREAMERS_FILE.open(encoding='utf-8') as f:
            data = json.load(f)

    data[time.time()] = new_info
    with STREAMERS_FILE.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def main():
    """ Entrypoint for calling this script. """
    # Get live streamers.
    client = berserk.Client()
    streamers = client.users.get_live_streamers()

    # Update with {'front-page': true/false}.
    # Abuses the fact that the main page lists the streamers ids as part of the relative URLs).
    r = requests.get('https://lichess.org/')
    front_page_ids = [x[0:x.find('"')] for x in str(r.content).split('/streamer/')[1:]]
    streamers = [dict(x, **{'front-page': x['id'] in front_page_ids}) for x in streamers]

    update_streamers_file(streamers)


if __name__ == "__main__":
    sys.exit(main())
