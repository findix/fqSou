#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'Sean'

import re
from datetime import datetime
from datetime import timedelta


class Log(object):
    def __init__(self):
        pass

    datetime = ""
    content = ""


def get_logs(path):
    log_file = open(path, "r").readlines()
    logs = list()
    temp_log = Log()
    for line in log_file:
        if re.match(r"^\[[\w\s:-]*\]$", line):
            if temp_log.datetime is not "":
                logs.append(temp_log)
                temp_log = Log()
            temp_log.datetime = datetime.strptime(line[1:-2], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
        else:
            temp_log.content += line
    logs.append(temp_log)
    return logs
