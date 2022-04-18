from edam.reader.resolvers.resolver import Resolver


class FileResolver(Resolver):

    @property
    def content_as_list(self):
        return self._content_as_list

    @content_as_list.setter
    def content_as_list(self, file_uri):
        with open(file_uri, 'r') as file:
            self._content_as_list = list(
                map(lambda line: line.strip('\n\r'), file.readlines()))
