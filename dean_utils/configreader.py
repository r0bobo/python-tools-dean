#!/usr/bin/env python3

import logging
import os
import collections
import configparser


class ConfigReader(configparser.ConfigParser):
    """Read properties from .dean.ini.

    Default file location is: ~/.config/dean/dean.ini.
    dean.ini file with default values is created if missing.
    """

    logger = []

    def __init__(self):
        super().__init__(allow_no_value=True)
        self.logger = logging.getLogger(__name__)

    def readconf(self, filename=None):
        """."""
        homedir = os.path.expanduser('~')

        default_config = collections.OrderedDict()
        default_config['GENERAL'] = {
            '# general settings': None
            }
        default_config['DL-YT-PLAYLIST'] = {
            'youtube_playlist': 'https://www.youtube.com/playlist?list=PL1qRR_Q0qopRTcoibkO5Ar7wh0iiTewys',
            # 'youtube_playlist': 'https://www.youtube.com/playlist?list=PL1qRR_Q0qopRh_CE3FvXSFOHohDAYH_GN',
            'download_location': '{:s}'.format(
                os.path.join(homedir, 'Downloads', 'Youtube_Videos')),
            'download_log': '{:s}'.format(
                os.path.join(homedir, '.local', 'share',
                             'dean', 'youtube_dl.log')
                             ),
            'download_archive': '{:s}'.format(
                os.path.join(homedir, '.local', 'share',
                             'dean', '.download_archive')
                             ),
            }
        default_config['SSH-LOGGER'] = {
            'auth_log': '/var/log/auth.log'
            }

        if not filename:
            config_file = os.path.join(
                homedir, '.config', 'dean', 'dean.ini'
                )
            self.logger.debug(
                'No config file path specificed, using default: {:s}'
                .format(config_file)
                )
        else:
            config_file = os.path.expanduser(filename)

        try:
            with open(config_file, 'r') as fp:
                super().read_file(fp)
            self.logger.debug('Finished reading {:s}'.format(config_file))
        except FileNotFoundError:
            self.logger.debug('Config file missing {:s}'.format(config_file))
            super().read_dict(default_config)
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, 'w+') as fp:
                super().write(fp)
                self.logger.info('Writing default config file to {:s}'.format(config_file))
