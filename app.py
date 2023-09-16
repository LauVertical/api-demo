#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import traceback
import argparse

from flask import Flask, request, jsonify, make_response
from webservice.apiList import apiList


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tornado Web Server')
    parser.add_argument('--port', type=int, default=6699, required=False, help='Port number to listen on')
    return parser.parse_args()


if __name__ == "__main__":

    app = Flask(__name__)


    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response


    @app.route('/query', methods=['POST', 'OPTIONS'])
    def query():
        if request.method == 'OPTIONS':
            res = make_response()
            res.status_code = 204
            return res
        else:
            try:
                data = request.json
                if not data:
                    return jsonify({
                        'status': 400,
                        'message': 'Cannot request from null query'
                    })
                api_name = data.get("api_name")
                if not api_name:
                    return jsonify({
                        'status': 500,
                        'message': traceback.format_exc()
                    })

                api = apiList.get(api_name)
                if not api:
                    return jsonify({
                        'status': 500,
                        'message': f'API {api_name} not found'
                    })

                req = {}
                if "query" in data:
                    req["query"] = data["query"]
                if "queryKW" in data:
                    req["queryKW"] = data["queryKW"]

                content = api.request(req)

                return content

            except Exception:
                return jsonify({
                    'status': 500,
                    'message': traceback.format_exc()
                })


    @app.route('/apilist', methods=['GET', 'OPTIONS'])
    def api_list():
        if request.method == 'OPTIONS':
            res = make_response()
            res.status_code = 204
            return res
        else:
            try:
                data = {"apilist": []}

                for key in apiList.keys():
                    data["apilist"].append(key)

                response_str = json.dumps(data, ensure_ascii=False)

                return response_str

            except Exception:
                response = {
                    'status': 500,
                    'message': traceback.format_exc()
                }

                return jsonify(response)


    args = parse_arguments()

    app.run(port=args.port)
