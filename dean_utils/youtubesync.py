#!/usr/bin/env python3

import argparse
import json
import logging
import logging.handlers
import os
import re
import time

from dean_utils import ConfigReader
from youtube_dl import YoutubeDL


def main():
    parser = argparse.ArgumentParser(
        description="Download videos from playlist"
        )
    parser.add_argument('playlist', type=str, help='Youtube playlist url')
    parser.add_argument(
        '-c', '--cfg', type=str, nargs=1,
        dest='config_file', default=None,
        help='Path to config file (default: ~/.config/dean/dean.ini)'
        )
    args = vars(parser.parse_args())

    formatter = logging.Formatter(
        fmt='%(asctime)-22s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)

    logging.getLogger(__name__).setLevel(logging.INFO)
    logging.getLogger(__name__).addHandler(sh)

    ys = YoutubeSync(config_file=args['config_file'])
    ys.download(args['playlist'])


class YoutubeSync:
    """Youtube video object."""

    config_key = 'DL-YT-PLAYLIST'

    def __init__(self, config_file=None):
        """."""
        self.config = []
        self.dl_logger = []
        self.dl_rate = []
        self.downloaded = []
        self.download_log = []
        self.logger = []
        self.ydl = []

        self.dl_location = []
        self.dl_archive = []
        self.dl_log = []

        self.logger = logging.getLogger(__name__)

        self.config = ConfigReader()
        self.config.readconf(config_file)

        try:
            self.dl_location = self.config[self.config_key]['download_location']
            self.dl_archive = self.config[self.config_key]['download_archive']
            self.dl_log = self.config[self.config_key]['download_log']
        except:
            self.logger.error('Could not read config file')

        # TODO: Rename config file entries to youtubesync?
        ydl_opts = {
            'outtmpl': '[%(uploader)s] %(title)s.%(ext)s',
            'logger': self.logger,
            'call_home': False,
            'download_archive':
                self.config[self.config_key]['download_archive'],
            'ignoreerrors': True,
            'socket_timeout': 10,
            # 'simulate': True,
            'progress_hooks': [self.hook],
        }

        self.ydl = YoutubeDL(ydl_opts)
        self.ydl.add_default_info_extractors

    def download(self, youtube_playlist=None):
        """Download videos in specified youtube_playlist."""
        if youtube_playlist:
            os.makedirs(self.dl_location, exist_ok=True)
            os.makedirs(os.path.dirname(self.dl_archive), exist_ok=True)

            self.logger.info('Downloading playlist: {:s}'
                             .format(youtube_playlist)
                             )
            os.chdir(self.dl_location)
            self.ydl.download([youtube_playlist])
            self.log_downloaded()
        else:
            self.logger.error('No youtube playlist specified')

    def hook(self, d):
        if d['status'] == 'downloading':
            try:
                self.dl_rate.append(float(d['speed']))
            except (TypeError, KeyError):
                pass
        elif d['status'] == 'finished':
            # TODO: Is capturing f\d{3} enough to cover all cases?
            ext = re.compile('(^.*)\\.f\\d{3}$')
            fn = ext.match(d['filename'])
            if fn:
                filename = fn.group(1)
            else:
                filename = d['filename']

            if filename not in self.downloaded:
                self.logger.info('Finished downloading {:s}'.format(filename))
                self.downloaded.append(filename)

    def log_downloaded(self):
        json_log = []

        if self.downloaded:
            try:
                dl_speed = sum(self.dl_rate)/len(self.dl_rate)
            except:
                dl_speed = -1

            dl_info = {
                       'date': time.strftime('%Y-%m-%d %H:%M:%S'),
                       'dl_speed': dl_speed,
                       'nr_downloaded': len(self.downloaded),
                       'videos': self.downloaded
                       }

            try:
                with open(self.dl_log, 'r') as fp:
                    json_log = json.load(fp)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                pass

            json_log.append(dl_info)

            os.makedirs(os.path.dirname(self.dl_log), exist_ok=True)
            try:
                with open(self.dl_log, 'w+') as fp:
                    json.dump(json_log, fp)
                self.logger.debug('Writing info to download log: {:s}'
                                  .format(self.dl_log)
                                  )
            except Exception as e:
                self.logger.exception(e)

        self.downloaded = []


if __name__ == '__main__':
    main()
