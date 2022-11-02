import os
import shutil

from generator import Generator
import urllib.parse as parseURL
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import time
from io import BytesIO

hostname = "localhost"
port = 8080
generator = Generator()


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

        elif self.path == "/js/chat-mode_server.js":
            with open("js/chat-mode_server.js", 'rb') as file:
                self.send_response(200)
                self.send_header("Content-type", "text/javascript")
                self.send_header("Content-Disposition", 'inline; '
                                                        'filename="{}"'.format(
                                                            os.path.basename("js/chat-mode_server.js")))
                fs = os.fstat(file.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.end_headers()
                shutil.copyfileobj(file, self.wfile)

        else:
            self.path = "/app.html"
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print("path : ", self.path)
        if self.path == "/?act=addTypo":
            print("headers : ", self.headers)
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            print(body)
            typo = body.decode('utf-8').split("=")[1]
            print(typo)
            generator.setTypo(typo)
            self.path = "/app.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/?act=generateList":
            print("headers : ", self.headers)
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            print(body)
            decodeBody = parseURL.unquote(body.decode('utf-8'))
            typo = decodeBody.split("&")[0]
            generator.setTypo(typo.split("=")[1])
            wordListRequest = decodeBody.split("&")[1].split("=")[1]
            wordList = wordListRequest.split("\r")
            if wordList.__contains__("\n"):
                wordList.remove("\n")
            print(wordList)
            temporaryList = "tmp.txt"
            generator.write_file(file_path=temporaryList, word_list=wordList)
            generator.steps()
            self.path = "/app.html"
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_PUT(self):
        filename = os.path.basename(self.path)

        if os.path.exists(filename):
            self.send_response(409, 'Conflict')
            self.end_headers()
            reply_body = '{0} already exists\n'.format(filename)
            self.wfile.write(bytes(reply_body, 'utf-8'))
            return


web_server = HTTPServer((hostname, port), Handler)
print("Server start on http://{0}:{1}\n".format(hostname, port))

try:
    web_server.serve_forever()
except KeyboardInterrupt:
    pass

web_server.server_close()
print("Server stopped")