from tsuruclient.base import Manager, TsuruAPIError

import unittest
import httpretty


class ManagerTestCase(unittest.TestCase):

    m = Manager("http://target", "123")

    def setUp(self):
        httpretty.enable()

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_raise_httperror(self):
        url = "http://target/missing"
        httpretty.register_uri(
            httpretty.POST,
            url,
            status=400,
            body="invalid request"
        )
        s = ("400 Client Error: Bad Request for url: "
             "http://target/missing: invalid request")
        raised = False
        try:
            self.m.request("post", "/missing")
        except TsuruAPIError as ex:
            raised = True
            self.assertEqual(s, str(ex).strip())
        self.assertEqual(True, raised)

    def test_versioned(self):
        url = "http://target/1.2/api"
        httpretty.register_uri(
            httpretty.POST,
            url,
            status=200
        )
        self.m.request("post", "/api", version=1.2)
        self.assertEqual("/1.2/api", httpretty.last_request().path)

    def test_authorization_header(self):
        url = "http://target/api"
        httpretty.register_uri(
            httpretty.POST,
            url,
            status=200
        )
        self.m.request("post", "/api")
        self.assertEqual("bearer 123",
                         httpretty.last_request().headers["authorization"])

    def test_handle_stream(self):
        url = "http://target/api"
        httpretty.register_uri(
            httpretty.POST,
            url,
            body='{"a":1}\n"abc"\n{"a":3}',
            status=200,
            content_type='application/x-json-stream',
        )
        gen = self.m.request("post", "/api")
        self.assertListEqual([{"a": 1}, "abc", {"a": 3}], list(gen))

    def test_customized_handle_func(self):
        def handle(r):
            return r.status_code
        url = "http://target/api"
        httpretty.register_uri(
            httpretty.POST,
            url,
            status=400,
        )
        response = self.m.request("post", "/api", handle_response=handle)
        self.assertEqual(400, response)
