#!/usr/bin/env python3

#    Paperwork - Using OCR to grep dead trees the easy way
#    Copyright (C) 2012-2014  Jerome Flesch
#    Copyright (C) 2012  Sebastien Maccagnoni-Munch
#
#    Paperwork is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Paperwork is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Paperwork.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging

logger = logging.getLogger(__name__)

#
# Request handler
#


class WebHandler(SimpleHTTPRequestHandler):
    def _send_response(self, mimetype, binary=False):
        try:
            self.send_response(200)
            self.send_header("Content-Type", mimetype)
            self.end_headers()
            print(binary)
            if bool(binary):
                f = open(os.curdir + self.path.split("?")[0], "rb")
                self.wfile.write(f.read())
                f.close()
            else:
                f = open(os.curdir + self.path.split("?")[0])
                self.wfile.write(bytes(f.read(), "utf-8"))
                f.close()
        except IOError:
            self.send_error(404, "File Not Found:" + os.curdir + self.path)

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-Type", "text/html")
        s.end_headers()

    def do_GET(s):
        if s.path == "/":
            s.path = "/pages/index.html"

        if s.path.split('?')[0].endswith(".html"):
            s._send_response("text/html")
        if s.path.endswith(".css"):
            s._send_response("text/css")
        if s.path.endswith(".js"):
            s._send_response("application/javascript")
        if s.path.endswith(".png"):
            s._send_response("image/png", True)
        if s.path.endswith(".properties"):
            s._send_response("text/plain")
        if s.path.split('?')[0].endswith(".pdf"):
            s._send_response("application/pdf", True)
        if s.path.endswith(".ico"):
            s._send_response("image/x-icon", True)

# for debugging
if __name__ == '__main__':
    formatter = logging.Formatter(
        '%(levelname)-6s %(name)-30s %(message)s')
    handler = logging.StreamHandler()
    logger = logging.getLogger()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel({
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }[os.getenv("PAPERWORK_VERBOSE", "INFO")])

    logger.info("WebServer starting...")

    ServerClass = HTTPServer
    httpd = ServerClass(('', 8001), WebHandler)
    try:
        httpd.serve_forever()
        logger.info("WebServer running!")
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info("WebServer stopped!")
