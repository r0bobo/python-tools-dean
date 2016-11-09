#!/usr/bin/env python3

import conf_reader
import datetime


def main():
    log = Log()
    log.log_successful('ssh_logger')


class Log:
    """."""

    config_reader = []
    log_path = []

    def __init__(self, log_path=None):
        """."""
        self.config_reader = conf_reader.ConfigReader()
        self.log_path = self.config_reader.get('activity_log')

    def log_successful(self, script_name):
        message = 'Successfully finshed: %s' % script_name
        print(message)

if __name__ == '__main__':
    main()
