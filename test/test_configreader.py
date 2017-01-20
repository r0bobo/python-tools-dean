#!/usr/bin/env python3

import logging
import os
import dean_utils
import shutil
import sys


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

    test_logger = logging.getLogger('test_configreader')
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(sh)

    # Test ConfigReader
    try:
        config = dean_utils.ConfigReader()
        config.readconf()
        config['DL-YT-PLAYLIST']['youtube_playlist']
        config['DL-YT-PLAYLIST']['download_location']
        config['DL-YT-PLAYLIST']['download_log']
        test_logger.info('Successfully created default config file')
    except Exception as e:
        test_logger.exception('Failed creating default config file')

    config_path = os.path.expanduser('~/test.ini')
    shutil.move(os.path.expanduser('~/.config/dean/dean.ini'), config_path)

    try:
        config.readconf(config_path)
        config['DL-YT-PLAYLIST']['youtube_playlist']
        config['DL-YT-PLAYLIST']['download_location']
        config['DL-YT-PLAYLIST']['download_log']
        test_logger.info('Successfully read config file: {:s}'
            .format(config_path))
    except Exception as e:
        test_logger.exception('Failed reading config file {:s}'
            .format(config_path))


if __name__ == '__main__':
    main()
