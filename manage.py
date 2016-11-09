# -*- coding:utf-8 -*-
import os
import traceback

from tornado import web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import TemplateModule

from handles import MainHandler, DocsHandler


class Application(web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/(.*)", DocsHandler),
            # (r"/task/(?P<tid>.*)", TaskHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={
                'include': TemplateModule,
            },
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":

    app = Application()
    # wsgi_app = wsgi.WSGIAdapter(app)

    loop = IOLoop.instance()

    print "http://{}:{}".format("localhost", 5210)

    HTTPServer(app).listen(5210)
    try:
        loop.start()
    except KeyboardInterrupt:
        print(" Shutting down on SIGINT!")
        loop.stop()
        traceback.format_exc()
    finally:
        pass


# loop.close()
# IOLoop.current().start()
# IOLoop.current().start()
