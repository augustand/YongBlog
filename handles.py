# -*- coding:utf-8 -*-

from tornado import web


class MainHandler(web.RequestHandler):
    def get(self):
        _d = open("docs/index.md").read()
        self.render("index.html", name=_d)


class DocsHandler(web.RequestHandler):
    def get(self, _path):

        if _path.endswith(".map"):
            return

        if _path.endswith(".md"):

            _content = open(_path).read()
            _content = _content.replace('`', '\`')

            p_path = "/".join(_path.split("/")[:-1])
            self.render(
                "article.html",
                articleUrl='/' + _path,
                gnavText=open(p_path + "/index.md").read(),
                articleText=_content
            )
        else:
            _d = open(_path + "/index.md").read()
            self.render(
                "article_urls.html",
                name=_d
            )

    def post(self, _path):

        if getattr(self.request, "body"):
            data = self.request.body

            with open(_path, 'w') as f:
                f.write(data)

        self.write("ok")
