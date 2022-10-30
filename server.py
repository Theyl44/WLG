import os
import shutil

from generator import Generator
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import time
from io import BytesIO

hostname = "localhost"
port = 8080


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):

        if self.path == "/result.txt":
            """
                use when trying to collect the result of the operation
            """
            if not os.path.exists("result.txt"):
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                return

            with open("result.txt", 'rb') as file:
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.send_header("Content-Disposition", 'attachment; '
                                                        'filename="{}"'.format(os.path.basename("result.txt")))
                fs = os.fstat(file.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(file, self.wfile)

        elif self.path == "/js/chatClient.js":
            # self.send_response(200)
            # self.send_header("Content-Type", "application/javascript")
            # self.end_headers()
            self.path = "/js/chatClient.js"
            return SimpleHTTPRequestHandler.do_GET(self)

        else:
            self.path = "/app.html"
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

    def do_PUT(self):
        filename = os.path.basename(self.path)

        if os.path.exists(filename):
            self.send_response(409, 'Conflict')
            self.end_headers()
            reply_body = '{0} already exists\n'.format(filename)
            self.wfile.write(bytes(reply_body, 'utf-8'))
            return


web_server = HTTPServer((hostname, port), Handler)
print("Server start on {0}:{1}\n".format(hostname, port))

try:
    web_server.serve_forever()
except KeyboardInterrupt:
    pass

web_server.server_close()
print("Server stopped")
