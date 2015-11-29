#!/usr/bin/python
# -*- coding:utf-8 -*-
import Config

__author__ = 'Sean'

import re
import json
from datetime import datetime
from datetime import timedelta


class Record(object):
    def __init__(self):
        self.datetime = ""
        self.content = []


class IP(object):
    def __init__(self, port, address):
        self.port = port
        self.address = address


def get_page(path, page, count):
    log_file = open(path, 'r').readlines()[::-1]  # 倒序遍历文件
    logs = list()
    i = 0
    for line in log_file:
        if len(logs) - 1 < i:
            logs.append(Record())
        if re.match(r'^\[[\w\s:-]*\]$', line):
            logs[i].datetime = datetime.strptime(line[1:-2], '%Y-%m-%d %H:%M:%S') + timedelta(hours=8)
            i += 1
            if i == page * count:
                return logs[(page - 1) * count:page * count]
        else:
            logs[i].content.insert(0, IP(port2name(line.split(' ')[0]), line.split(' ')[1]))
    return logs

comment = None


def port2name(port):
    global comment
    if comment is None:
        config_file = open(Config.read_config('config.properties', 'config', 'shadowsocks_config'), 'r')
        config = json.loads(config_file.read())
        comment = config["_comment"]
    if str(port) in comment:
        return comment[str(port)]
    else:
        return port
