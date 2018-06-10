#!/usr/bin/env python3.5

import re
import os
from subprocess import Popen, PIPE
from shutil import rmtree

class TestRsync:

    def __init__(self):
        self.percent_complete = 0
        self.transfer_rate = 0
        self.stdout_block = ''
        self.stderr_block = ''
        self.progress_callback = None
        self.rsync_cmd = ''
        self.p = ''
        self.line = ''

    def sync(self):
        self.rsync_cmd = ['rsync'] + ['-a', '--no-inc-recursive', '--info=progress2', 'a', 'b']
        self.p = Popen(self.rsync_cmd, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True)

        while True:
            self.line = self.p.stdout.readline()
            print(self.line)
            TestRsync._parse_progress(self)

            if self.p.poll() is not None:
                break

    def _parse_progress(self):
        re_matches = re.findall(r'\d+(?=%)', self.line)

        if re_matches:
            self.percent_complete = re_matches[0];
            print(self.percent_complete, end="-", flush=True)

    def get_progress(self):
        return self.percent_complete


def main():
    t = TestRsync()
    t.sync()
    #if os.path.exists("b/a"):
    #    rmtree("/home/jmarin/PycharmProjects/Rsync/b/a")


if __name__ == "__main__":
    main()

