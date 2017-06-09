#!/usr/bin/env python2
# coding: utf-8


import socket
from brotherprint import BrotherPrint
from labelprinter import Labelprinter


def getLined(txt):
    pass

def testLabel(printjob):
    TEST_FONT = 'lettergothic'
    TEST_CHAR_SIZE = '75'
    TEST_BOLD = 'on'
    TEST_TEXT = "auf deinem Grab"
    labelprinter = Labelprinter(conf=None, printjob=printjob)
    labelprinter.printText(TEST_TEXT, charSize=TEST_CHAR_SIZE, font=TEST_FONT, bold=TEST_BOLD)


def testRaster(printjob):
    printjob.invalidate()
    printjob.initialize()
    printjob.raster_mode()
    #printjob.print_line()
    #printjob.print_line()
    #printjob.print_line()

def testBarcode(printjob):
    barcodes = ['code39', 'itf', 'ean8/upca', 'upce', 'codabar', 'code128', 'gs1-128', 'rss']
    labelprinter = Labelprinter(conf=None, printjob=printjob)
    labelprinter.printBarcode("TEST", barcodes[2])

    # nope: 'code39', itf, ean8/upca, upce, codabar,  gs1-128
    #'itf',
    #printjob.qr_code("test123", cell_size=10)
    #printjob.barcode(str(123), 'rss', rss_symbol='rsslimited')

f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f_socket.connect(('172.22.26.67', 9100))
printjob = BrotherPrint(f_socket)

testLabel(printjob)
# testBarcode(printjob) # FIXME
