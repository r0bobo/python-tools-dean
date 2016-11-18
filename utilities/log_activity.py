#!/usr/bin/env python3

import conf_reader
import datetime


def main():
    log = Log()
    log.successful('ssh_logger')
    log.failed('dl_yt_playlist')


class Log:
    """."""

    config_reader = []
    log_file = []

    def __init__(self, log_file=None):
        """."""
        self.config_reader = conf_reader.ConfigReader()

        if log_file:
            self.log_file = log_file
        else:
            self.log_file = self.config_reader.get('activity_log')

    def write_log(self, script_name, successful):
        if successful:
            status = 'successfully finished'
        else:
            status = 'failed'

        message = '%s    %s: %s\n' % (datetime.datetime.now().strftime('%Y %b %d %H:%M:%S'), script_name, status)

        with open(self.log_file, 'a+') as f:
            f.write(message)

    def successful(self, script_name):
        self.write_log(script_name, True)

    def failed(self, script_name):
        self.write_log(script_name, False)


if __name__ == '__main__':
    main()
