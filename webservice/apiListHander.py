#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import json
import traceback
from webservice.apiList import apiList

root_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + ".") + '/'


class ApiListHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        self.set_header("Content-Type", "application/json")

        try:
            data = {"apilist": []}
            for key in apiList.keys():
                data["apilist"].append(key)
            response_str = json.dumps(data, ensure_ascii=False)
            return self.write(response_str)
        except Exception:
            response = {
                'status': 500,
                'message': traceback.format_exc()
            }
            return self.write(json.dumps(response, ensure_ascii=False))


if __name__ == "__main__":
    from tornado.options import define, options

    define("port", default=8888, help="run on the given port", type=int)
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", ApiListHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
