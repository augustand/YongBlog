# -*- coding:utf-8 -*-
import os
import re

from tornado import web


class MainHandler(web.RequestHandler):
    def get(self):
        _d = open("docs/index.md").read()
        self.render("index.html", name=_d, previous="/")


class DocsHandler(web.RequestHandler):
    def get(self, _path):

        if _path.endswith(".map"):
            return

        p_path = os.path.split(_path)[0]  # "/".join(_path.split("/")[:-1])
        if _path.endswith(".md"):

            _content = open(_path).read()
            _content = _content.replace('`', '\`')
            _content = _content.replace('$', '\$')

            self.render(
                "article.html",
                articleUrl='/' + _path,
                gnavText=open(p_path + "/index.md").read(),
                articleText=_content,
                previous=p_path

            )
        else:
            _d = open(_path + "/index.md").read()
            self.render(
                "article_urls.html",
                name=_d,
                previous=p_path
            )

    def post(self, _path):

        if getattr(self.request, "body"):
            data = self.request.body

            old_catalog = _path.rsplit("/", 2)[-2]
            old_title = _path.rsplit("/", 1)[-1].rsplit(".", 1)[0]

            header = data.split('\n\n\n')[0]
            print header
            # _title = re.match(r".*^title\s?:\s+(?P<title>.*)", header)
            # if _title:
            #     new_title = _title.groupdict().get("title")
            #     print new_title
            _catalog = re.match(r"catalog\s?:\s+(?P<catalog>.*)\s", header)
            print _catalog
            if _catalog:
                new_catalog = _catalog.groupdict().get("catalog")
                print new_catalog


            with open(_path, 'w') as f:
                f.write(data)

        self.write("ok")
