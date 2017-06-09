#!/usr/bin/env python2
# coding: utf-8
# https://fragments.turtlemeat.com/pythonwebserver.php

import cgi
import os
import socket
from brotherprint import BrotherPrint
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from labelprinter import Labelprinter

if os.path.isfile('labelprinterServeConf_local.py'):
    import labelprinterServeConf_local as conf
else:
    import labelprinterServeConf as conf


class MyHandler(BaseHTTPRequestHandler):
    labelprinter = Labelprinter(conf=conf)

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            template = ''

            finalPath = self.path
            templateReplaceDict = {}
            print 'self.path', self.path
            if finalPath == '/':
                finalPath = conf.SERVER_DEFAULT_TEMPLATE

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
            else:
                template = open('www' + finalPath).read()

            for replaceKey, replaceValue in templateReplaceDict.iteritems():
                template = template.replace('{{' + replaceKey + '}}', replaceValue)

            self.wfile.write(template)

            return

        except Exception as ex:
            self.send_error(404, 'File Not Found: {} {}'.format(self.path, ex))

    def do_POST(self):
        self.send_response(301)
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            print ctype, pdict
            query = None

            if ctype == 'multipart/form-data':
                query = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                query = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)

            print query
            self.end_headers()
            text = query.get('text')

            finalTxt = ''
            for txt in text:
                finalTxt += txt

            if finalTxt.strip() == '':
                raise RuntimeError('NO TEXT, NO LABEL!')

            self.wfile.write("POST OK.\n")
            self.wfile.write("start printing: " + finalTxt + "\n")

            print finalTxt

            if query.get('printMode', [''])[0] == 'barcode':
                self.labelprinter.printBarcode(
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
                self.labelprinter.printText(
                    finalTxt,
                    charSize=query.get('fontSize', [42])[0],
                    font=query.get('font', ['lettergothic'])[0],
                    align=query.get('align', ['left'])[0],
                    bold=query.get('bold', ['off'])[0],
                    charStyle=query.get('charStyle', ['normal'])[0],
                    cut=query.get('cut', ['full'])[0],
                )
        except Exception as ex:
            print 'ERROR:', ex
            self.wfile.write("ERROR: " + str(ex))


def main():
    server = None
    try:
        server = HTTPServer(('', conf.SERVER_PORT), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        if server is not None:
            server.socket.close()

if __name__ == '__main__':
    main()
