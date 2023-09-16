# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup

from webservice.api.apiBase import apiBase
from webservice.requestUtil import *


class baiduWikiApi(apiBase):

    def _getWebPage(self, query) -> str:
        url = "https://baike.baidu.com/item/" + query["queryKW"] + "?fromModule=lemma_search-box"
        req = requestObjcet(url=url, header={}, data={}, method=METHOD.GET)
        return requestPage(req)["msg"]

    def _phasePage(self, page) -> str:
        soup = BeautifulSoup(page, 'html.parser')
        content_divs = soup.find_all('div', {'class': ['lemma-summary J-summary', 'para MARK_MODULE']})
        for div in content_divs:
            sup_tags = div.find_all('sup', {'class': ['sup--normal']})
            for sup in sup_tags:
                sup.decompose()
        extracted_data = []
        for div in content_divs:
            inner_text = re.sub(r'[\n]+', '\n', div.get_text().strip())
            extracted_data.append(inner_text)
        extracted_data = [item for item in extracted_data if item != '']
        return "\n".join(extracted_data)

