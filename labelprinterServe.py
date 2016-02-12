#!/usr/bin/env python2
# coding: utf-8
# https://fragments.turtlemeat.com/pythonwebserver.php
import string
import cgi
import time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri


class MyHandler(BaseHTTPRequestHandler):

    def printText(
            self,
            txt,
            charSize='42',
            font='lettergothic',
            align='left',
            bold='off',
            charStyle='normal',
            cut='full'
    ):
        print "start printing:", txt
        import socket
        from brotherprint import BrotherPrint

        f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        f_socket.connect(('172.22.27.26', 9100))
        printjob = BrotherPrint(f_socket)

        printjob.command_mode()
        printjob.initialize()
        printjob.select_font(font)
        printjob.char_size(charSize)  # 28 chars
        printjob.alignment(align)
        # printjob.char_size('75')
        printjob.bold(bold)
        printjob.char_style(charStyle)
        printjob.cut_setting(cut)
        # printjob.select_charset("Germany")
        #printjob.select_char_code_table("western european")
        #txt = 28*"x"
        #txt = "öäü".decode('utf8').encode('iso-8859-1')

        printjob.send(txt.decode('utf8').encode('iso-8859-1'))
        printjob.print_page('full')

    def getCmbFromList(self, ls):
        cmb = ''
        for itm in ls:
            cmb += '<option value="' + str(itm) + '">' + str(itm) + '</option>'
        return cmb

    def do_GET(self):
        try:
            sizes = [
                '42',
                '24',
                '32',
                '48',
                '33',
                '38',
                '46',
                '50',
                '58',
                '67',
                '75',
                '83',
                '92',
                '100',
                '117',
                '133',
                '150',
                '167',
                '200',
                '233',
                '11',
                '44',
                '77',
                '111',
                '144'
            ]
            sizesCmb = self.getCmbFromList(sizes)

            '''
                    <Bit map fonts>
                    'brougham'
                    'lettergothicbold'
                    'brusselsbit'
                    'helsinkibit'
                    'sandiego'
                    <Outline fonts>
                    'lettergothic'
                    'brusselsoutline'
                    'helsinkioutline'
            '''

            fontsOutline = [
                'lettergothic',
                'brusselsoutline',
                'helsinkioutline'
            ]

            fontsBitMap = [
                'brougham',
                'lettergothicbold',
                'brusselsbit',
                'helsinkibit',
                'sandiego'
            ]

            fontsCmb = '<optgroup label="Outline Fonts">'
            fontsCmb += self.getCmbFromList(fontsOutline)
            fontsCmb += '</optgroup>'

            fontsCmb += '<optgroup label="Bitmap Fonts">'
            fontsCmb += self.getCmbFromList(fontsBitMap)
            fontsCmb += '</optgroup>'

            aligns = [
                'left',
                'center',
                'right',
                'justified'
            ]
            alignsCmb = self.getCmbFromList(aligns)

            charStyles = [
                'normal',
                'outline',
                'shadow',
                'outlineshadow'
            ]
            charStylesCmb = self.getCmbFromList(charStyles)

            cuts = [
                'full',
                'half',
                'chain',
                'special'
            ]
            cutsCmb = self.getCmbFromList(cuts)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            template = ''
            if self.path == '/':
                template = open('templates/base.html').read()
            elif self.path == '/magic':
                template = open('templates/magic.html').read()
            else:
                template = 'NOTHING'

            template = template.replace('{{sizesCmb}}', sizesCmb)
            template = template.replace('{{fontsCmb}}', fontsCmb)
            template = template.replace('{{alignsCmb}}', alignsCmb)
            template = template.replace('{{charStylesCmb}}', charStylesCmb)
            template = template.replace('{{cutsCmb}}', cutsCmb)

            self.wfile.write(template)

            return

        except Exception as ex:
            self.send_error(404, 'File Not Found: {} {}'.format(self.path, ex))

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            print ctype, pdict
            query = None
            if ctype == 'multipart/form-data':
                query = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                query = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            self.send_response(301)
            print query
            self.end_headers()
            text = query.get('text')
            print "filecontent", text
            self.wfile.write("<HTML>POST OK.<BR><BR>")
            # self.wfile.write(upfilecontent[0]);

            finalTxt = ''
            print text
            for txt in text:
                finalTxt += txt

            print finalTxt

            self.printText(
                finalTxt,
                charSize=query.get('fontSize', [42])[0],
                font=query.get('font', ['lettergothic'])[0],
                align=query.get('align', ['left'])[0],
                bold=query.get('bold', ['off'])[0],
                charStyle=query.get('charStyle', ['normal'])[0],
                cut=query.get('cut', ['full'])[0],
            )
        except Exception as ex:
            print ex
            self.wfile.write(ex)


def main():
    try:
        server = HTTPServer(('', 8000), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
