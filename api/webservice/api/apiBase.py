# -*- coding: utf-8 -*-
from abc import abstractmethod


class apiBase(object):

    @abstractmethod
    def _getWebPage(self, query: dict) -> str:
        """Get request page."""

    @abstractmethod
    def _phasePage(self, page: str) -> str:
        """Get phase data."""

    def request(self, query: dict) -> str:
        page = self._getWebPage(query)
        result = self._phasePage(page)
        return result
