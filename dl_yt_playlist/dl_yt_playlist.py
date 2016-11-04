#!/usr/bin/env python3

import os
import json
import re
from copy import deepcopy
from youtube_dl import YoutubeDL
from python_tools_dean.utilities import conf_reader

def main():
    global downloaded
    downloaded = []
    config = conf_reader.ConfigReader()

    # playlist_url = 'https://www.youtube.com/playlist?list=PL1qRR_Q0qopRh_CE3FvXSFOHohDAYH_GN'
    playlist_url = config.get('youtube_playlist')

    home = os.path.expanduser('~/ExternalHDD')
    download_dir = config.get('download_location') 

    json_file = os.path.join(config.get('log_dir'), 'dl-yt-playlist.json')

    if os.path.exists(download_dir):
        videos = YoutubeSync(json_file)

        videos.sync_playlist(playlist_url)
        videos.download(download_dir)
        videos.set_downloaded(downloaded)
        videos.write_json(json_file)
    else:
        print('[error] Download dir \'%s\' does not exist.' % download_dir)


class YoutubeSync:
    """Youtube video object."""

    video_list = []
    ydl = []

    def __init__(self, filename=None):
        """."""
        ydl_opts = {
            'progress_hooks': [download_hook],
        }

        self.ydl = YoutubeDL(ydl_opts)
        self.ydl.add_default_info_extractors

        if filename:
            try:
                with open(filename) as fp:
                    self.video_list = json.load(fp)
            except FileNotFoundError:
                self.video_list = dict()
        else:
            self.video_list = dict()

    def add(self, id, title):
        """."""
        if id not in self.video_list:
            self.video_list[id] = dict()
            self.video_list[id]['title'] = title
            self.video_list[id]['downloaded'] = False
        else:
            print('[index] %s already added. Skipping.' % title)

    def download(self, dl_dir):
        """."""
        dl_vids = []

        os.chdir(dl_dir)

        for video_id in self.video_list:
            if not self.video_list[video_id]['downloaded']:
                dl_vids.append('https://www.youtube.com/watch?v=%s' % video_id)

        try:
            self.ydl.download(dl_vids)
        except ContentTooShortError:
            pass

    def sync_playlist(self, playlist_url):
        """."""
        playlist = self.ydl.extract_info(playlist_url, download=False)

        for var in playlist['entries']:
            self.add(var['webpage_url_basename'], var['title'])

        # Remove videos from local database that are not in youtube playlist
        video_list = deepcopy(self.video_list)
        for id_loc in self.video_list.keys():
            if id_loc not in [ids_new['webpage_url_basename'] for ids_new in playlist['entries']]:
                print('[cleaning] %s removed from youtube playlist.' % self.video_list[id_loc]['title'])
                video_list.pop(id_loc, None)
        self.video_list = video_list

    def set_downloaded(self, id_list):
        """."""
        for id in id_list:
            self.video_list[id]['downloaded'] = True
            print('[downloaded] %s set to downloaded.' % self.video_list[id]['title'])

    def write_json(self, filename):
        """."""
        with open(filename, 'w+') as file:
            json.dump(self.video_list, file, sort_keys=True, indent=4)


def download_hook(d):
    """."""
    global downloaded

    pattern = re.compile('.+\-[\w-]{11}')

    if d['status'] == 'finished':
        # TODO: Find more robust way to find url_basename?
        for seg in reversed(d['filename'].split('.')):
            if pattern.match(seg):
                print('[debug] %s' % seg[-11:])
                downloaded.append(seg[-11:])
                break


if __name__ == '__main__':
    main()
