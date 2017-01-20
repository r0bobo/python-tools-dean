#!/usr/bin/env python3

import os
import python_tools_dean
import shutil


def main():
    config = python_tools_dean.ConfigReader()
    config.readconf()
    shutil.move(os.path.expanduser('~/.config/dean/dean.ini'), os.path.expanduser('~/test.ini'))
    config.readconf(os.path.expanduser('~/test.ini'))

    print(config['DL-YT-PLAYLIST']['youtube_playlist'])
    print(config['DL-YT-PLAYLIST']['download_location'])
    print(config['DL-YT-PLAYLIST']['download_log'])


if __name__ == '__main__':
    main()
