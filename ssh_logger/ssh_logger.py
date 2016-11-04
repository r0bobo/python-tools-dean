#!/usr/bin/env python3

import subprocess
import json
import os
import re
from datetime import datetime
from python_tools_dean.utilities import conf_reader

def main():
    """."""
    config = conf_reader.ConfigReader()
    json_file = os.path.join(config.get('log_dir'), 'ssh-log.json')
    auth_log = config.get('auth_log')

    ssh = LogSSH(auth_log, json_file)
    ssh.load_logdata()
    ssh.get_geodata()
    ssh.write_log(json_file)


class LogSSH:
    """."""

    fil = []
    log = dict()

    def __init__(self, auth_file, json_log=None):
        """."""
        self.fil = auth_file

        if json_log:
            try:
                with open(json_log) as file:
                    self.log = json.load(file)
            except FileNotFoundError:
                self.log = dict()
        else:
            self.log = dict()

    def load_logdata(self):
        """."""
        sshd_invalid = re.compile('^(\D{3}) (\d{2}) ([\d\:]{8}).*sshd.*Invalid user (\S*) from ([\w.:]+)')

        with open(self.fil, 'r') as fp:
            for line in fp:
                match = sshd_invalid.match(line)
                if match:
                    # Set date and time for event
                    time = match.group(3).split(':')
                    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(match.group(1))+1  # HACK Didnt want to use strptime due to possible locale errors
                    year = int(datetime.now().year)
                    day = int(match.group(2))

                    ip = match.group(5)
                    datestr = '%d%d%d-%s%s%s' % (year, month, day, time[0], time[1], time[2])
                    user = match.group(4)

                    if ip not in self.log:
                        self.log[ip] = dict()
                    if 'failed_logins' not in self.log[ip]:
                        self.log[ip]['failed_logins'] = dict()

                    self.log[ip]['failed_logins'][user] = datestr

    def get_geodata(self):
        """."""
        for ip in self.log:
            if 'hostname' not in self.log[ip]:
                output = subprocess.check_output(['curl', 'ipinfo.io/%s' % ip])
                geodata = json.loads(output.decode('UTF-8'))

                self.log[ip]['hostname'] = geodata['hostname']
                self.log[ip]['city'] = geodata['city']
                self.log[ip]['region'] = geodata['region']
                self.log[ip]['country'] = geodata['country']
                self.log[ip]['loc'] = geodata['loc']
                self.log[ip]['org'] = geodata['org']

    def write_log(self, json_log):
        """."""
        with open(json_log, 'w+') as file:
            json.dump(self.log, file, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
