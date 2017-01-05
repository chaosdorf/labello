#!/usr/bin/env python2
# coding: utf-8

import socket
from brotherprint import BrotherPrint

def getLined(txt):
    pass


def testLabel(printjob):
    printjob.select_font('lettergothic')
    printjob.char_size('42')
    printjob.char_size('75')
    printjob.bold('on')
    #printjob.select_charset("Germany")
    #printjob.select_char_code_table("western european")
    #txt = 28*"x"
    txt = "auf deinem grab".decode('utf8').encode('iso-8859-1')

    printjob.send(txt)
    #printjob.print_page('full')

def testRaster(printjob):
    printjob.invalidate()
    printjob.initialize()
    printjob.raster_mode()
    #printjob.print_line()
    #printjob.print_line()
    #printjob.print_line()

def testBarcode(printjob):
    barcodes = ['code39', 'itf', 'ean8/upca', 'upce', 'codabar', 'code128', 'gs1-128', 'rss']

    # nope: 'code39', itf, ean8/upca, upce, codabar,  gs1-128
    #'itf',
    #printjob.qr_code("test123", cell_size=10)
    #printjob.barcode(str(123), 'rss', rss_symbol='rsslimited')

f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f_socket.connect(('172.22.26.67', 9100))
printjob = BrotherPrint(f_socket)

printjob.command_mode()
printjob.initialize()
#testRaster(printjob)
#testBarcode(printjob)

testLabel(printjob)


printjob.print_page('full')
