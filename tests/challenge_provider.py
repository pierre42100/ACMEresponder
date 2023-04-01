"""
A dummy lightweight server for test challenges hosting
"""

from sewer.auth import ProviderBase, ChalItemType, ChalListType, ErrataListType
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

from io import BytesIO


class HTTPChallengeProviderTest(ProviderBase):
    """
    Dummy HTTP challenge provider
    """

    def __init__(self, **kwargs) -> None:
        if "chal_types" not in kwargs:
            kwargs["chal_types"] = ["http-01"]
        super().__init__(**kwargs)

    def setup(self, challenges: ChalListType) -> ErrataListType:
        for c in challenges:
            requests.put(
                url=f"http://localhost:{PROVIDER_PORT}/.well-known/acme-challenge/{c['token']}",
                data=c["key_auth"],
            )
        return []

    def unpropagated(self, _challenges: ChalListType) -> ErrataListType:
        # Propagation is immediate
        return []

    def clear(self, challenges: ChalListType) -> ErrataListType:
        for c in challenges:
            requests.delete(
                url=f"http://localhost:{PROVIDER_PORT}/.well-known/acme-challenge/{c['token']}",
            )
        return []


FILES = {}

PROVIDER_PORT = 4567


class ChallengeServer(BaseHTTPRequestHandler):
    def do_GET(self):
        global FILES
        # Check if the file exists
        if self.path in FILES:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(FILES[self.path])
            return

        self.send_response(404)
        self.end_headers()

    def do_PUT(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        global FILES
        FILES[self.path] = body

    def do_DELETE(self):
        self.send_response(200)
        self.end_headers()
        global FILES
        if self.path in FILES:
            FILES.pop(self.path)


def run_server(port: int):
    """
    Run challenge server
    """
    httpd = HTTPServer(("localhost", port), ChallengeServer)
    httpd.serve_forever()


def challenges_server_test():
    """
    Run challenges server in testsuite
    """
    run_server(PROVIDER_PORT)


if __name__ == "__main__":
    print(f"Start to listen on http://localhost:{PROVIDER_PORT}/")
    run_server(PROVIDER_PORT)
