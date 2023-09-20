#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from enum import Enum


class METHOD(Enum):
    POST = "POST"
    GET = "GET"


class requestObject(object):

    def __init__(self, header: dict, data: dict,
                 url: str, method: METHOD):
        self.header = header
        self.data = data
        self.method = method
        self.url = url


def requestPage(req: requestObject) -> dict:
    try:
        if req.method == METHOD.GET:
            response = requests.get(url=req.url, headers=req.header)
        else:
            response = requests.post(url=req.url, data=req.data, headers=req.header)

        response.raise_for_status()  # 如果出现错误，会抛出一个异常
        return {
            "status": 200,
            "msg": response
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": 500,
            "msg": e.response
        }
