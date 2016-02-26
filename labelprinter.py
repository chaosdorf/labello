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
    txt = "öäü".decode('utf8').encode('iso-8859-1')

    printjob.send(txt)
    printjob.print_page('full')

def testBarcode(printjob):
    barcodes = ['code39', 'itf', 'ean8/upca', 'upce', 'codabar', 'code128', 'gs1-128', 'rss']

    # nope: 'code39', itf, ean8/upca, upce, codabar,  gs1-128
    #'itf',
    barcodes = ['code39', 'code128', 'gs1-128']
    index = 0
    for code in barcodes:
        printjob.barcode(str(index), code, 'on', height=100, width='medium')
        index += 1
    #printjob.barcode(str(123), 'rss', rss_symbol='rsslimited')

f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f_socket.connect(('172.22.27.26', 9100))
printjob = BrotherPrint(f_socket)

printjob.command_mode()
printjob.initialize()

testBarcode(printjob)


printjob.print_page('full')