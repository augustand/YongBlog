# -*- coding:utf-8 -*-

import os
import re

import gevent
import time


def get_article_title(file_path):
    with open(file_path) as file:
        for _f in file:
            m = re.match(r"#{1}?\s+\[(?P<title0>.*)\]|(#{1}\s+)(?P<title1>.*)", _f)
            if not m:
                continue

            __d = m.groupdict()
            if __d.get("title0"):
                return __d.get("title0")
            else:
                return __d.get("title1")
        else:
            return file_path.rsplit("/", 1).pop().split('.', 1)[0]


def getIndex(_path):
    tpl = '* [**{}**](/{})\n'

    p, d, f = os.walk(_path).next()
    yield tpl.format("previous", p.rsplit("/", 1)[0])
    for _name in d:
        yield tpl.format(_name, p + "/" + _name)

    for _name in f:
        if _name != 'index.md' and _name.endswith("md"):
            yield tpl.format(get_article_title(p + "/" + _name), p + "/" + _name)


def genIndex(_path, _content):
    with open(_path, "w") as f:
        if type(_content) is str:
            f.write(_content)
        elif type(_content) in [list, type((i for i in []))]:
            f.writelines(_content)


def genDoc(_path):
    p, d, f = os.walk(_path).next()
    gevent.spawn(genIndex, p + "/index.md", getIndex(p)).join()
    # genIndex(p + "/index.md", getIndex(p))
    for _d in d:
        genDoc(p + "/" + _d)


if __name__ == '__main__':
    docs = []

    genDoc("docs")
    # print get_article_title("docs/TEST.md")
    # print get_article_title("docs/DOING.md")

    # name = "docs/TEST.md"
    # print os.path.getmtime(name)  # 获取文件的修改时间
    # print os.path.getctime(name)  # 获取文件的创建时间
    # timeArray = time.localtime(os.path.getmtime(name))
    # print time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
