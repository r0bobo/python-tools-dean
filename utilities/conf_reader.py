#!/usr/bin/env python3

import re
from os.path import expanduser, join


class ConfigReader:
    """Read properties from .dean.conf.

    Default file location is: ~/.dean.conf.
    Conf. file with default values is created if missing.
    """

    config_data = []
    homedir = []

    def __init__(self, config_file=None):
        self.config_data = dict()
        self.homedir = expanduser("~")

        if not config_file:
            config_file = join(self.homedir, '.dean.conf')

        self.read_config_file(config_file)

    def read_config_file(self, config_file):
        """Read the config file. Create default if missing."""
        regex = re.compile('^\s*(\S+)\s*=\s*(\S+)\s*$')

        try:
            with open(config_file, 'r') as file:
                for line in file:
                    match = regex.match(line)
                    if match:
                        self.config_data[match.group(1)] = match.group(2)
        except FileNotFoundError:
            self.create_default_config(config_file)

    def get(self, property):
        """Return value of property."""
        return self.config_data[property]

    def create_default_config(self, config_file):
        """Create default config file."""
        print('%s missing. Creating default config.' % config_file)
        with open(config_file, 'w+') as file:
            file.write('# Settings for private scripts\n\n\n')
            file.write('# General\n')
            file.write('log_dir = %s\n\n\n' % join(self.homedir, '.dean_log'))
            file.write('# dl-yt-playlist\n')
            file.write('youtube_playlist = %s\n' % 'https://www.youtube.com/playlist?list=PL1qRR_Q0qopRh_CE3FvXSFOHohDAYH_GN')
            file.write('download_location = %s\n\n\n' % join(self.homedir, 'Downloads', 'Youtube_Videos'))
            file.write('# ssh-logger\n')
            file.write('auth_log = %s\n\n\n' % '/var/log/auth.log')
