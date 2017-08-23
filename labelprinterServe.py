#!/usr/bin/env python2
# coding: utf-8
# https://fragments.turtlemeat.com/pythonwebserver.php

# some compatibility with Python 3 (see #7)
from __future__ import print_function
from __future__ import unicode_literals

import cgi
import os
import socket
from io import open # compatibility to Python 2
from brotherprint import BrotherPrint
try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError: # Python 3
    from http.server import BaseHTTPRequestHandler, HTTPServer

from labelprinter import Labelprinter
import labelprinterServeConf as conf

if conf.SENTRY_DSN:
    import raven
    raven_client = raven.Client(conf.SENTRY_DSN)
else:
    raven_client = None

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            template = ''

            finalPath = self.path
            templateReplaceDict = {}
            print('self.path', self.path)
            if finalPath == '/':
                finalPath = conf.SERVER_DEFAULT_TEMPLATE

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
            elif finalPath == '/app.js':
                import templates.magic
                templateReplaceDict = templates.magic.getParseDict()
                template = open('www/app.js').read()
            else: # most likely a binary file
                binary = True
                template = open('www' + finalPath, "rb").read()

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
            self.send_error(500, 'ERROR: {}'.format(ex))

    def do_POST(self):
        self.send_response(301)
        try:
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
                query = cgi.parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=1)

            print(query)
            self.end_headers()
            text = query.get('text')

            finalTxt = ''
            for txt in text:
                if isinstance(txt, bytes):
                    txt = txt.decode("utf-8")
                finalTxt += txt

            if finalTxt.strip() == '':
                raise RuntimeError('NO TEXT, NO LABEL!')

            self.wfile.write(b"POST OK.\n")
            self.wfile.write("start printing: {}\n".format(finalTxt).encode("utf-8"))

            print(finalTxt)
            
            labelprinter = Labelprinter(conf=conf)

            if query.get('printMode', [''])[0] == 'barcode':
                labelprinter.printBarcode(
                    finalTxt,
                    barcode=query.get('barcodeType', ['code39'])[0],
                    characters=query.get('barcodeCharacters', ['on'])[0],
                    height=int(query.get('barcodeHeight', [100])[0]),
                    width=query.get('barcodeWidth', ['medium'])[0],
                    parentheses=query.get('barcodeParentheses', ['on'])[0],
                    ratio=query.get('barcodeRatio', ['3:1'])[0],
                    equalize=query.get('barcodeEqualize', ['off'])[0]
                )
            else:
                labelprinter.printText(
                    finalTxt,
                    charSize=query.get('fontSize', [42])[0],
                    font=query.get('font', ['lettergothic'])[0],
                    align=query.get('align', ['left'])[0],
                    bold=query.get('bold', ['off'])[0],
                    charStyle=query.get('charStyle', ['normal'])[0],
                    cut=query.get('cut', ['full'])[0],
                )
        except Exception as ex:
            if raven_client:
                raven_client.captureException()
            print('ERROR:', ex)
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
