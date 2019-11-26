import request
import json

# TODO url need


class Request:
    def __init__(self, follow, timeout=1):
        self._follow = follow
        self._timeout = timeout

    def follow(self):
        return self._follow(self._timeout)


class TestResponse:
    def __init__(self, status_code, response_data):
        self.status_code = status_code
        self._json = response_data

    def json(self):
        return self._json

