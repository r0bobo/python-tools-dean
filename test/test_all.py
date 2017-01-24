#!/usr/bin/env python3

import configparser
import json
import logging
import os
import dean_utils
import shutil
import unittest


class TestConfigReader(unittest.TestCase):

    test_dir = os.path.expanduser('~/test_configreader')

    def setUp(self):
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(os.path.expanduser('~'))
        shutil.rmtree(self.test_dir)

    def test_creating_default_config_file(self):
        config = dean_utils.ConfigReader()
        config.readconf(os.path.join(self.test_dir, 'test', 'test_config.ini'))
        self.assertEqual(config['GENERAL']['debug'], 'test')


class TestYoutubeSync(unittest.TestCase):

    test_dir = os.path.expanduser('~/test_youtubesync')
    test_cfg = os.path.join(test_dir, 'config.ini')

    dl_dir = os.path.join(test_dir, 'downloads')
    dl_log = os.path.join(test_dir, 'youtube_dl.json')
    dl_arc = os.path.join(test_dir, 'download_archive')

    pl1 = 2
    pl12 = 4

    def setUp(self):
        os.makedirs(self.test_dir, exist_ok=True)
        os.chdir(self.test_dir)

        config = configparser.ConfigParser()
        config['DL-YT-PLAYLIST'] = {
            'download_location': self.dl_dir,
            'download_log': self.dl_log,
            'download_archive': self.dl_arc,
            }
        with open(self.test_cfg, 'w+') as fp:
            config.write(fp)

    def tearDown(self):
        os.chdir(os.path.expanduser('~'))
        shutil.rmtree(self.test_dir)

    def test_youtubesync_download_pl1(self):
        ydl = dean_utils.YoutubeSync(config_file=self.test_cfg)
        ydl.download('https://www.youtube.com/playlist?list=PL1qRR_Q0qopRDY2kqz2FtCCJijs7GxAQf')
        self.assertEqual(len(os.listdir(self.dl_dir)), self.pl1)

    def test_youtubesync_download_pl1_and_pl2(self):
        ydl = dean_utils.YoutubeSync(config_file=self.test_cfg)
        ydl.download('https://www.youtube.com/playlist?list=PL1qRR_Q0qopRDY2kqz2FtCCJijs7GxAQf')
        ydl.download('https://www.youtube.com/playlist?list=PL1qRR_Q0qopRTcoibkO5Ar7wh0iiTewys')
        self.assertEqual(len(os.listdir(self.dl_dir)), self.pl12)

    def test_youtubesync_json_log(self):
        json_log = []
        dl_files = ['testfile1.f140', 'testfile1.f501', 'test.file2']
        log_files = ['testfile1', 'test.file2']

        ydl = dean_utils.YoutubeSync(config_file=self.test_cfg)

        for dlfile in dl_files:
            ydl.hook({'status': 'finished', 'filename': dlfile})
        ydl.log_downloaded()

        with open(self.dl_log, 'r') as fp:
            json_log = json.load(fp)

        self.assertEqual(json_log[0]['videos'], log_files)


if __name__ == '__main__':
    formatter = logging.Formatter(
        fmt='%(asctime)s, %(levelname)-9s %(message)s (%(name)s)',
        datefmt='%Y-%m-%d %H:%M:%S'
        )

    fh = logging.FileHandler(
            os.path.join(os.path.expanduser('~'), 'dean_utils_test.log'), 'w'
            )

    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logging.getLogger('dean_utils').setLevel(logging.DEBUG)
    logging.getLogger('dean_utils').addHandler(fh)

    unittest.main(verbosity=2)
