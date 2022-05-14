import requests

from edam.reader.resolvers.resolver import Resolver


class HttpResolver(Resolver):

    @property
    def content_as_list(self):
        return self._content_as_list

    @content_as_list.setter
    def content_as_list(self, file_uri):
        response = requests.get(file_uri)
        self._content_as_list = response.text.split('\r\n')
