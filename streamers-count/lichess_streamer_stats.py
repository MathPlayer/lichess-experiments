#!/usr/bin/env python3

""" Automate gathering of information about current streamers. """

# System imports.
import json
import pathlib
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
    client = berserk.Client()
    streamers = client.users.get_live_streamers()
    update_streamers_file(streamers)


if __name__ == "__main__":
    sys.exit(main())
