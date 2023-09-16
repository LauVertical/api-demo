#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import tornado
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tornado Web Server')
    parser.add_argument('--port', type=int, default=6699, required=False, help='Port number to listen on')
    return parser.parse_args()


if __name__ == "__main__":

    from webservice.requestHander import RequestHandler
    from webservice.apiListHander import ApiListHandler

    args = parse_arguments()

    handlers = [
        (r'/query', RequestHandler),
        (r'/apilist', ApiListHandler),
    ]

    app = tornado.web.Application(handlers=handlers)
    # http_server = tornado.httpserver.HTTPServer(app)
    app.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
