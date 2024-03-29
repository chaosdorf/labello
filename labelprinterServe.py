#!/usr/bin/env python3
# coding: utf-8
# https://fragments.turtlemeat.com/pythonwebserver.php

# some compatibility with Python 3 (see #7)
from __future__ import print_function
from __future__ import unicode_literals

import cgi
import logging
import os
import socket
import json
import sys
from io import open # compatibility to Python 2
from brotherprint import BrotherPrint
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from urlparse import urlparse, parse_qs
except ImportError: # Python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import urlparse, parse_qs

from labelprinter import Labelprinter
import labelprinterServeConf as conf

if conf.SENTRY_DSN:
    import sentry_sdk
    sentry_sdk.init(conf.SENTRY_DSN)

def strip_query(query):
    for key in query.keys():
        # replace lists with their first element
        if isinstance(query[key], list):
            query[key] = query[key][0]
        # decode bytes if possible
        if isinstance(query[key], bytes):
            query[key] = query[key].decode('utf-8')


def log_print(*args):
    return ' '.join(str(a) for a in args)


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            template = ''

            parsedUrl = urlparse(self.path)
            query_components = parse_qs(parsedUrl.query)
            finalPath = parsedUrl.path
            templateReplaceDict = {}
            logging.debug(log_print('self.path', self.path))
            if finalPath == '/':
                finalPath = conf.SERVER_DEFAULT_TEMPLATE

            #print('path', parsedUrl.path)
            #print(query_components)

            binary = False
            if finalPath == '/base':
                import templates.base
                templateReplaceDict = templates.base.getParseDict()
                template = open('templates/base.html').read()
            elif finalPath == '/barcode':
                import templates.barcode
                templateReplaceDict = templates.barcode.getParseDict()
                template = open('templates/barcode.html').read()
            elif finalPath == '/magic':
                import templates.magic
                templateReplaceDict = templates.magic.getParseDict()
                template = open('templates/magic.html').read()
            elif finalPath == '/choose':
                template = open('templates/choose.html').read()
            elif finalPath == '/pictures':
                import templates.pictures
                templateReplaceDict = templates.pictures.getParseDict()
                template = open('templates/pictures.html').read()
            elif finalPath == '/app.js':
                import templates.magic
                templateReplaceDict = templates.magic.getParseDict()
                template = open('www/app.js').read()
            else: # most likely a binary file
                binary = True
                template = open('www' + finalPath, "rb").read()

            if query_components.get('text'):
                templateReplaceDict['text'] = query_components['text'][0]
            else:
                templateReplaceDict['text'] = ''

            if not binary:
                for replaceKey, replaceValue in templateReplaceDict.items():
                    template = template.replace('{{' + replaceKey + '}}', replaceValue)
                template = template.encode("utf-8")
            
            self.send_ok(template)
            return

        except IOError as ex:
            self.send_error(404, 'File Not Found: {} {}'.format(self.path, ex))
        except Exception as ex:
            if "sentry_sdk" in globals():
                sentry_sdk.capture_exception(ex)

            logging.error(log_print("ERROR:", ex))
            import traceback
            traceback.print_exc()
            self.send_error(500, 'ERROR: {}'.format(ex))

    def send_ok(self, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        self.send_response(301)
        try:
            printMode = "default"

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            logging.debug(log_print(ctype, pdict))
            query = None
            clength = int(self.headers.get('content-length'))

            if ctype == 'multipart/form-data':
                logging.debug(log_print(self.rfile))
                for key in pdict.keys():
                    pdict[key] = pdict[key].encode("utf-8")
                pdict["CONTENT-LENGTH"] = clength
                query = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                if sys.version_info.major == 2:
                    data = self.rfile.read(clength)
                else:
                    data = self.rfile.read(clength).decode('utf-8')
                query = parse_qs(data, keep_blank_values=1)
            elif ctype == "application/json":
                query = json.loads(self.rfile.read(clength).decode("utf-8"))

            if ctype != "application/json":
                strip_query(query)
            
            logging.debug(log_print(query))
            self.end_headers()
            
            if query['text'].strip() == '':
                raise RuntimeError('NO TEXT, NO LABEL!')

            self.wfile.write(b"POST OK.\n")
            self.wfile.write("start printing: {}\n".format(query['text']).encode("utf-8"))

            labelprinter = Labelprinter(conf=conf)

            if query.get('printMode', '') == 'barcode':
                labelprinter.printBarcode(
                    query['text'],
                    barcode=query.get('barcodeType', 'code39'),
                    characters=query.get('barcodeCharacters', 'on'),
                    height=int(query.get('barcodeHeight', 100)),
                    width=query.get('barcodeWidth', 'medium'),
                    parentheses=query.get('barcodeParentheses', 'on'),
                    ratio=query.get('barcodeRatio', '3:1'),
                    equalize=query.get('barcodeEqualize', 'off')
                )

            elif printMode == 'pictures':
                logging.debug(log_print('pictures!!!!!!'))
                logging.debug(log_print(query.keys()))

                submit_picture = query.get('submitPicture', [None])[0]
                labelprinter.printPicture(submit_picture)
            else:
                labelprinter.printText(
                    query['text'],
                    charSize=query.get('fontSize', 42),
                    font=query.get('font', 'lettergothic'),
                    align=query.get('align', 'left'),
                    bold=query.get('bold', 'off'),
                    charStyle=query.get('charStyle', 'normal'),
                    cut=query.get('cut', 'full'),
                )

        except Exception as ex:
            if "sentry_sdk" in globals():
                sentry_sdk.capture_exception(ex)

            logging.error(log_print('ERROR:', ex))
            import traceback
            traceback.print_exc()
            self.send_error(500, "ERROR: {}".format(ex))


def main():
    server = None
    # ask the system what the configured bind address means
    bindings = socket.getaddrinfo(
        conf.SERVER_ADDRESS, conf.SERVER_PORT, 0, socket.SOCK_STREAM
    )
    assert len(bindings) == 1  # The result should be unambiguous.
    # The next line shouldn't be needed for 3.8 and newer,
    # see https://bugs.python.org/issue24209.
    HTTPServer.address_family = bindings[0][0]
    try:
        server = HTTPServer(bindings[0][4], MyHandler)
        logging.info(log_print('started httpserver on', bindings[0][4], ' ...'))
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info(log_print('^C received, shutting down server'))
        if server is not None:
            server.socket.close()


if __name__ == '__main__':
    logging.info(log_print('Log level is set to:', logging.getLogger().getEffectiveLevel()))
    main()
