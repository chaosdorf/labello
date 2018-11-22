#!/usr/bin/env python3
# coding: utf-8
# https://fragments.turtlemeat.com/pythonwebserver.php

# some compatibility with Python 3 (see #7)
from __future__ import print_function
from __future__ import unicode_literals

import cgi
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
    import raven
    raven_client = raven.Client(conf.SENTRY_DSN)
else:
    raven_client = None

def strip_query(query):
    for key in query.keys():
        # replace lists with their first element
        if isinstance(query[key], list):
            query[key] = query[key][0]
        # decode bytes if possible
        if isinstance(query[key], bytes):
            query[key] = query[key].decode('utf-8')

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            template = ''


            parsedUrl = urlparse(self.path)
            query_components = parse_qs(parsedUrl.query)
            finalPath = parsedUrl.path
            templateReplaceDict = {}
            print('self.path', self.path)
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
            
            self.wfile.write(template)
            return

        except IOError as ex:
            self.send_error(404, 'File Not Found: {} {}'.format(self.path, ex))
        except Exception as ex:
            if raven_client:
                raven_client.captureException()
            print("ERROR: ", ex)
            import traceback
            traceback.print_exc()
            self.send_error(500, 'ERROR: {}'.format(ex))

    def do_POST(self):
        self.send_response(301)
        try:
            printMode = "default"

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            print(ctype, pdict)
            query = None

            if ctype == 'multipart/form-data':
                print(self.rfile)
                for key in pdict.keys():
                    pdict[key] = pdict[key].encode("utf-8")
                query = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.get('content-length'))
                if sys.version_info.major == 2:
                    data = self.rfile.read(length)
                else:
                    data = self.rfile.read(length).decode('utf-8')
                query = cgi.parse_qs(data, keep_blank_values=1)
            elif ctype == "application/json":
                length = int(self.headers.get('content-length'))
                query = json.loads(self.rfile.read(length).decode("utf-8"))

            if ctype != "application/json":
                strip_query(query)
            
            print(query)
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
                print('pictures!!!!!!')
                print(query.keys())
                submitPicture = query.get('submitPicture', [None])[0]
                labelprinter.printPicture(submitPicture)
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
            if raven_client:
                raven_client.captureException()
            print('ERROR:', ex)
            import traceback
            traceback.print_exc()
            self.wfile.write("ERROR: {}".format(ex).encode("utf-8"))


def main():
    server = None
    try:
        server = HTTPServer(('', conf.SERVER_PORT), MyHandler)
        print('started httpserver on port ' + str(conf.SERVER_PORT) + ' ...')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        if server is not None:
            server.socket.close()
    except:
        if raven_client:
            raven_client.captureException()
        raise

if __name__ == '__main__':
    main()
