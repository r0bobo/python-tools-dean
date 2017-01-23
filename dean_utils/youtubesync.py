#!/usr/bin/env python3

import logging
import logging.handlers
import os
import re
import time

from dean_utils import ConfigReader
from youtube_dl import YoutubeDL


def main():
    # TODO: Use argparse to take input arguments
    pass


class YoutubeSync:
    """Youtube video object."""

    config = []
    dl_logger = []
    dl_rate = []
    downloaded = []
    download_log = []
    logger = []
    ydl = []

    def __init__(self, config_file=None):
        """."""
        self.logger = logging.getLogger(__name__)

        self.dl_logger = logging.getLogger('youtube_dl')
        self.dl_logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            fmt='%(asctime)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
            )

        self.config = ConfigReader()
        self.config.readconf(config_file)

        # Create folders if missing
        os.makedirs(os.path.dirname(
            self.config['DL-YT-PLAYLIST']['download_log']), exist_ok=True
            )
        os.makedirs(os.path.dirname(
            self.config['DL-YT-PLAYLIST']['download_archive']), exist_ok=True
            )

        rfh = logging.handlers.RotatingFileHandler(
            self.config['DL-YT-PLAYLIST']['download_log']
            )
        rfh.setFormatter(formatter)
        rfh.setLevel(logging.INFO)

        self.dl_logger.addHandler(rfh)

        # TODO: Rename config file entries to youtubesync?
        ydl_opts = {
            'outtmpl': '[%(uploader)s] %(title)s',
            'logger': self.logger,
            'call_home': False,
            'download_archive':
                self.config['DL-YT-PLAYLIST']['download_archive'],
            'ignoreerrors': True,
            'socket_timeout': '10',
            # 'simulate': True,
            'progress_hooks': [self.hook],
        }

        self.ydl = YoutubeDL(ydl_opts)
        self.ydl.add_default_info_extractors

    def download(self):
        os.makedirs(
            self.config['DL-YT-PLAYLIST']['download_location'], exist_ok=True
                    )
        os.chdir(self.config['DL-YT-PLAYLIST']['download_location'])
        self.ydl.download([self.config['DL-YT-PLAYLIST']['youtube_playlist']])
        # self.log_downloaded()

    def hook(self, d):
        pattern = re.compile('^(.*)\\.\\w*$')
        
        self.logger.info(d)

        if d['status'] == 'downloading':
            try:
                self.dl_rate.append(float(d['speed']))
            except Exception as e:
                self.logger.exception(e)
        elif d['status'] == 'finished':
            match = pattern.match(d['filename'])
            if match.group(1) not in self.downloaded:
                self.downloaded.append(match.group(1))

    def log_downloaded(self):
        # TODO: Log to both normal text file and ascii-file

        new = {'date': time.strftime('%Y-%m-%d %H:%M:%S')}

        try:
            new['dl_speed'] = sum(self.dl_rate)/len(self.dl_rate)
        except:
            new['dl_speed'] = -1

        try:
            new['nr_downloaded'] = len(self.downloaded)
        except:
            new['nr_downloaded'] = -1

        try:
            new['videos'] = self.downloaded
        except:
            new['videos'] = 'none'

        if self.downloaded:
            msg = ('Downloaded {:d} videos. Average dl speed: {:.2f}MB/s'
                   .format(len(self.downloaded),
                           sum(self.dl_rate)/len(self.dl_rate)/1024**2,
                           )
                   )
            for s in self.downloaded:
                msg += '\n        {:s}'.format(s)

            print(msg)
            self.dl_logger.info(msg)


if __name__ == '__main__':
    main()
