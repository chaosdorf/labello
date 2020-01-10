#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import socket
from brotherprint import BrotherPrint
from labelprinter import Labelprinter
import labelprinterServeConf as conf

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
    printjob.print_line()
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

def testQRcode(printjob):
    labelprinter = Labelprinter(conf=None, printjob=printjob)
    # data, cell_size=4, symbol_type=2, partitioned=0, partition=0, parity=0, error_correction=4, data_input=0):

    #printjob.qr_code(**{'data':'noot noot', 'cell_size':10, 'symbol_type':2})
    printjob.qr_code('noot noot', 10)
    printjob.line_feed()
    printjob.select_font('lettergothic')
    printjob.char_size('11')

    printjob.send("noot noot")
    printjob.char_style('normal')
    printjob.print_page('full')

f_socket = socket.create_connection((conf.PRINTER_HOST, conf.PRINTER_PORT))
printjob = BrotherPrint(f_socket)



#testRaster(printjob)
#testLabel(printjob)
testQRcode(printjob)
#testBarcode(printjob) # FIXME
