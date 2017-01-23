#!/usr/bin/env python3

import logging
import dean_utils

# TODO: Create way to specify testing playlists for travis

def main():
    # Setup logger
    formatter = logging.Formatter(
        fmt='%(asctime)s, %(levelname)-9s %(message)s (%(name)s)',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    logging.getLogger('dean_utils').setLevel(logging.DEBUG)
    logging.getLogger('dean_utils').addHandler(sh)

    test_logger = logging.getLogger('test_dl_yt_playlist')
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(sh)

    # Test ConfigReader
    # ydl1 = dean_utils.YoutubeSync(
    #     '/home/travis/build/r0bobo/python_tools_dean/test/test1.ini'
    #     )
    # ydl1.download()
    ydl2 = dean_utils.YoutubeSync(
        '/home/travis/build/r0bobo/python_tools_dean/test/test2.ini'
        )
    ydl2.download()


if __name__ == '__main__':
    main()
