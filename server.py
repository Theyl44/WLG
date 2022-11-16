import os
import shutil

from generator import Generator
import urllib.parse as parseURL
from http.server import HTTPServer, SimpleHTTPRequestHandler

# hostname = "0.0.0.0"
# port = 80
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
                print("[INFO] No file result.txt found")
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
        if self.path == "/?act=addTypo":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            typo = body.decode('utf-8').split("=")[1]
            generator.setTypo(typo)
            self.path = "/app.html"
            return SimpleHTTPRequestHandler.do_GET(self)

        elif self.path == "/?act=generateList":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            decodeBody = parseURL.unquote(body.decode('utf-8'))

            # collect typo
            typo = decodeBody.split("&")[0]
            generator.setTypo(typo.split("=")[1])

            # collect list of words
            wordListRequest = decodeBody.split("&")[1].split("=")[1]
            wordList = self.parseWordlist(wordListRequest)

            # write in file, the list of words
            temporaryListFile = "tmp.txt"
            generator.write_file(file_path=temporaryListFile, word_list=wordList)
            generator.steps(file=temporaryListFile)
            self.path = "/app.html"
            fileHtml = open("app.html", 'r', encoding='UTF-8')
            codeHtml = ""
            for line in fileHtml:
                codeHtml += line
                if line.__contains__('id="generate_list"'):
                    resultGen = generator.get_result()
                    for i in range(0, 50):
                        msg = "<tr><td>" + str((i + 1)) + "</td><td>" + resultGen.__getitem__(i) + "</td></tr>"
                        codeHtml += msg
            fileHtml.close()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(codeHtml, 'utf-8'))

        elif self.path == "/?act=applyTransformation":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            decodeBody = parseURL.unquote(body.decode('utf-8'))
            wordListRequest = decodeBody.split("&")[1].split("=")[1]

            wordList = self.parseWordlist(wordListRequest)

            transformWordList = generator.add_tranformation(word_list=wordList)

            self.path = "/app.html"
            fileHtml = open('app.html', 'r', encoding='UTF-8')
            codeHtml = ""
            for line in fileHtml:
                codeHtml += line
                if line.__contains__('id="temporary_list"'):
                    for i in range(0, len(transformWordList)):
                        msg = "<tr><td>" + str((i + 1)) + "</td><td>" + str(transformWordList[i]) + "</td></tr>"
                        codeHtml += msg
            fileHtml.close()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(codeHtml, 'utf-8'))

    def parseWordlist(self, wordListRequest):
        wordList = wordListRequest.split("\r")
        if wordList.__contains__("\n"):
            wordList.remove("\n")
        # remove \n for each element
        for i in range(0, len(wordList)):
            wordList[i] = wordList[i].replace("\n", "")
        return wordList

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
