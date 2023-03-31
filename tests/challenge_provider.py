from sewer.auth import ProviderBase, ChalItemType, ChalListType, ErrataListType
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

class TestChallengeProvider(ProviderBase):
    def __init__(self, **kwargs) -> None:
        if "chal_types" not in kwargs:
            kwargs["chal_types"] = ["http-01"]
        super().__init__(**kwargs)
    
    def setup(self, challenges: ChalListType) -> ErrataListType:
        raise NotImplementedError("setup method not implemented by %s" % self.__class__)

    def unpropagated(self, _challenges: ChalListType) -> ErrataListType:
        # Propagation is immediate
        return []

    def clear(self, challenges: ChalListType) -> ErrataListType:
        raise NotImplementedError("clear method not implemented by %s" % self.__class__) 



FILES = {}

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
        content_length = int(self.headers['Content-Length'])
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
    httpd = HTTPServer(('localhost', port), ChallengeServer)
    httpd.serve_forever()

if __name__ == '__main__':
    print("Start to listen on http://localhost:4500/")
    run_server(4500)