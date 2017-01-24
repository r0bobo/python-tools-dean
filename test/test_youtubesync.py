#!/usr/bin/env python3

import dean_utils
import logging

# TODO: Create way to specify testing playlists for travis

def main():
    # Setup logger
    formatter = logging.Formatter(
        fmt='%(asctime)s, %(levelname)-9s %(message)s (%(name)s)',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)

    logging.getLogger('dean_utils').setLevel(logging.DEBUG)
    logging.getLogger('dean_utils').addHandler(sh)

    test_logger = logging.getLogger('test_dl_yt_playlist')
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(sh)

    # Test ConfigReader
    ydl = dean_utils.YoutubeSync()
    ydl.download('https://www.youtube.com/playlist?list=PL1qRR_Q0qopRDY2kqz2FtCCJijs7GxAQf')
    ydl.download('https://www.youtube.com/playlist?list=PL1qRR_Q0qopRTcoibkO5Ar7wh0iiTewys')


if __name__ == '__main__':
    main()
