#!/usr/bin/env python2
# coding: utf-8
#https://fragments.turtlemeat.com/pythonwebserver.php
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri

def printText(txt, charSize = '42', font = 'lettergothic'):
    print "start printing:", txt
    import socket
    from brotherprint import BrotherPrint

    f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f_socket.connect(('172.22.27.26', 9100))
    printjob = BrotherPrint(f_socket)

    printjob.command_mode()
    printjob.initialize()
    printjob.select_font(font)
    printjob.char_size(charSize) # 28 chars
    #printjob.char_size('75')
    printjob.bold('on')
    #printjob.select_charset("Germany")
    #printjob.select_char_code_table("western european")
    #txt = 28*"x"
    #txt = "öäü".decode('utf8').encode('iso-8859-1')

    printjob.send(txt.decode('utf8').encode('iso-8859-1'))
    printjob.print_page('full')

class MyHandler(BaseHTTPRequestHandler):

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

            sizesCmb = ''
            for size in sizes:
                sizesCmb += '<option value="'+ size +'">'+ size +'</option>'
            
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
            #<optgroup label="Italienische Gerichte">
			#	<option value="piz"> Pizza </option>
			#	<option value="tor"> Tortelloni </option>
			#	<option value="bif"> Bifsteca </option>
			#</optgroup>
            fontsCmb = '<optgroup label="Outline Fonts">'
            for font in fontsOutline:
                fontsCmb += '<option value="'+ font +'">'+ font +'</option>'
                
            fontsCmb += '</optgroup>'
            fontsCmb += '<optgroup label="Bitmap Fonts">'
            for font in fontsBitMap:
                fontsCmb += '<option value="'+ font +'">'+ font +'</option>'
            fontsCmb += '</optgroup>'
                
            self.send_response(200)
            self.send_header('Content-type',	'text/html')
            self.end_headers()
            self.wfile.write('''<html>
                    <head>
                        <meta charset="utf-8"/>
                        <title>laibelprinter</title>
                        <!-- Latest compiled and minified CSS -->
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">

                        <!-- Optional theme -->
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r" crossorigin="anonymous">

                        <!-- Latest compiled and minified JavaScript -->
                        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS" crossorigin="anonymous"></script>
                        <style type="text/css">
                            body {
                                font-family: monospace;
                            }
                        </style>
                    </head>
                    <body>
                        <form method="POST" enctype="multipart/form-data" class="form-group">
                            <textarea name="text" cols="28" rows="15"></textarea>
                            <div class="form-group">
                                <label for="fontSize">Font Size</label><select name="fontSize">'''+ sizesCmb +'''</select>
                            </div>
                            <div class="form-group">
                                <label for="fontSize">Font</label><select name="font">'''+ fontsCmb +'''</select>
                            </div>
                            <div class="form-group">
                                <input type="submit" value="PRINT" class="btn btn-primary">
                            </div>
                        </form>
                    </body>
                </html>
            ''')
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
     

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            print ctype, pdict
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                query=cgi.parse(self.rfile, pdict)
            self.send_response(301)
            print query
            self.end_headers()
            text = query.get('text')
            print "filecontent", text
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            #self.wfile.write(upfilecontent[0]);
            
            finalTxt = ''
            for txt in text:
                finalTxt += txt
             
            print query.get('text')[0]
            printText(finalTxt, query.get('fontSize')[0], query.get('font')[0])
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

