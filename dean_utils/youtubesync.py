#!/usr/bin/env python3

import json
import logging
import os
import re

from copy import deepcopy
from dean_utils import ConfigReader
from youtube_dl import YoutubeDL


def main():
    # TODO: Use argparse to take input arguments
    pass


class YoutubeSync:
    """Youtube video object."""

    config = []
    video_list = []
    ydl = []
    logger = []
    download_log = []
    downloaded = []
    dl_rate = []

    def __init__(self, config_file=None):
        """."""
        self.logger = logging.getLogger(__name__)

        self.config = ConfigReader()
        self.config.readconf(config_file)

        # self.logger.info('youtube_playlist: {:s}'.format(config['DL-YT-PLAYLIST']['youtube_playlist']))
        # self.logger.info('download_log: {:s}'.format(config['DL-YT-PLAYLIST']['download_log']))
        # self.logger.info('download_location: {:s}'.format(config['DL-YT-PLAYLIST']['download_location']))
        # self.logger.info('download_archive: {:s}'.format(config['DL-YT-PLAYLIST']['download_archive']))

        ydl_opts = {
            'outtmpl': '[%(uploader)s] %(title)s',
            'logger': self.logger,
            'call_home': False,
            'download_archive': self.config['DL-YT-PLAYLIST']['download_archive'],
            'simulate': True,
            'progress_hooks': [self.hook],
        }

        self.ydl = YoutubeDL(ydl_opts)
        self.ydl.add_default_info_extractors

    def download(self):
        self.ydl.download([self.config['DL-YT-PLAYLIST']['youtube_playlist']])
        self.log_downloaded()

    def hook(self, d):
        pattern = re.compile('^(.*)\\.\\w*$')

        if d['status'] == 'downloading':
            self.dl_rate.append(float(d['speed']))
        elif d['status'] == 'finished':
            match = pattern.match(d['filename'])
            if match.group(1) not in self.downloaded:
                self.downloaded.append(match.group(1))

    def log_downloaded(self):
        if self.downloaded:
            print(self.downloaded)
            print(sum(self.dl_rate)/len(self.dl_rate)/1024**2)


        # print(mean(dl_rate))

        # if filename:
        #     try:
        #         with open(filename) as fp:
        #             self.video_list = json.load(fp)
        #     except FileNotFoundError:
        #         self.video_list = dict()filepath
        # else:
        #     self.video_list = dict()

#     def add(self, id, title):
#         """."""
#         if id not in self.video_list:
#             self.video_list[id] = dict()
#             self.video_list[id]['title'] = title
#             self.video_list[id]['downloaded'] = False
#         else:
#             print('[index] %s already added. Skipping.' % title)
#
#     def download(self, dl_dir):
#         """."""
#         dl_vids = []
#
#         os.chdir(dl_dir)
#
#         for video_id in self.video_list:
#             if not self.video_list[video_id]['downloaded']:
#                 dl_vids.append('https://www.youtube.com/watch?v=%s' % video_id)
#
#         try:
#             self.ydl.download(dl_vids)
#         except ContentTooShortError:
#             pass
#
#     def sync_playlist(self, playlist_url):
#         """."""
#         playlist = self.ydl.extract_info(playlist_url, download=False)
#
#         for var in playlist['entries']:
#             self.add(var['webpage_url_basename'], var['title'])
#
#         # Remove videos from local database that are not in youtube playlist
#         video_list = deepcopy(self.video_list)
#         for id_loc in self.video_list.keys():
#             if id_loc not in [ids_new['webpage_url_basename'] for ids_new in playlist['entries']]:
#                 print('[cleaning] %s removed from youtube playlist.' % self.video_list[id_loc]['title'])
#                 video_list.pop(id_loc, None)
#         self.video_list = video_list
#
#     def set_downloaded(self, id_list):
#         """."""
#         for id in id_list:
#             self.video_list[id]['downloaded'] = True
#             print('[downloaded] %s set to downloaded.' % self.video_list[id]['title'])
#
#     def write_json(self, filename):
#         """."""
#         with open(filename, 'w+') as file:
#             json.dump(self.video_list, file, sort_keys=True, indent=4)
#
#
# def download_hook(d):
#     """."""
#     global downloaded
#
#     pattern = re.compile('.+\-[\w-]{11}')
#
#     if d['status'] == 'finished':
#         # TODO: Find more robust way to find url_basename?
#         for seg in reversed(d['filename'].split('.')):
#             if pattern.match(seg):
#                 print('[debug] %s' % seg[-11:])
#                 downloaded.append(seg[-11:])
#                 break


if __name__ == '__main__':
    main()
