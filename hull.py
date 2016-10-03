import requests


class Hull:
    def __init__(self,
                 platform_id,
                 org_url,
                 platform_secret=None,
                 sentry=None):
        self.baseurl = "%s/api/v1" % (org_url,)
        self.platform_id = platform_id
        self.platform_secret = platform_secret
        self.sentry = sentry

    def _auth_headers(self):
        auth_headers = {
            "Hull-App-Id": self.platform_id
        }
        if self.platform_secret is not None:
            auth_headers["Hull-Access-Token"] = self.platform_secret

        return auth_headers

    def _req(self, method, url, data=None):
        if not url.startswith("/"):
            url = "/" + url

        req_funcs = {
            "get": requests.get,
            "post": requests.post,
            "put": requests.put,
            "delete": requests.delete
        }
        payloads = {
            "get": {},
            "post": {}
        }
        if data is not None:
            payloads = {
                "get": {
                    "params": data
                },
                "post": {
                    "json": data
                },
                "put": {
                    "json": data
                }
            }

        return req_funcs[method.lower()](self.baseurl + url,
                                         headers=self._auth_headers(),
                                         **payloads[method.lower()])

    def _parse_json(self, response):
        parsed_data = response.text
        try:
            parsed_data = response.json()
        except ValueError:
            print response
            pass

        return parsed_data

    def get(self, endpoint, data=None):
        response = self._req("get", endpoint, data)
        return self._parse_json(response)

    def get_all(self, endpoint, data=None):
        if data is None:
            data = {}

        unduplicated_data = []
        ids = []

        page = 1
        is_there_new_data = True

        while is_there_new_data:
            partial_data = []
            try:
                data.update({"per_page": 100, "page": page})
                request = self._req("get", endpoint, data)
                partial_data = request.json()
            except ValueError:
                raise self.JSONParseError()
            except requests.exceptions.RequestException:
                raise self.RequestException()

            duplicate_count = 0
            duplicated_ids = []
            for obj in partial_data:
                if obj["id"] in ids:
                    duplicate_count += 1
                    duplicated_ids += obj["id"]
                else:
                    ids.append(obj["id"])
                    unduplicated_data.append(obj)
            is_there_new_data = len(partial_data) != duplicate_count
            page += 1

            # reports when there is partially duplicated data
            if is_there_new_data and duplicate_count != 0:
                self.sentry.captureMessage(
                    "Duplicated data on different page",
                    tags={
                        "level": "info"
                    }, extra=({
                        "duplicated_ids": reduce(
                            lambda a, b: "%s;%s" % (a, b),
                            duplicated_ids),
                        "retrieved_ids": reduce(
                            lambda a, b: "%s;%s" % (a, b),
                            map(lambda hobj: hobj["id"], partial_data))
                    }))

        return unduplicated_data

    def put(self, endpoint, data=None):
        response = self._req("put", endpoint, data)
        return self._parse_json(response)

    def post(self, endpoint, data=None):
        response = self._req("post", endpoint, data)
        return self._parse_json(response)

    def delete(self, endpoint):
        response = self._req("delete", endpoint)
        return self._parse_json(response)

    class JSONParseError(ValueError):
        pass

    class RequestException(requests.exceptions.RequestException):
        pass
