#!/usr/bin/env python2
# coding: utf-8

import socket
from brotherprint import BrotherPrint

class Labelprinter():
    def __init__(self, conf=None, printjob=None):
        if conf:
            f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            f_socket.settimeout(conf.PRINTER_TIMEOUT)
            f_socket.connect((conf.PRINTER_HOST, conf.PRINTER_PORT))
            printjob = BrotherPrint(f_socket)
        assert printjob
        self.printjob = printjob
        self.printjob.command_mode()
        self.printjob.initialize()
    
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
        
        self.printjob.select_font(font)
        self.printjob.char_size(charSize)  # 28 chars
        self.printjob.alignment(align)
        self.printjob.bold(bold)
        self.printjob.char_style(charStyle)
        self.printjob.cut_setting(cut)

        self.printjob.send(txt.decode('utf8').encode('iso-8859-1'))
        self.printjob.print_page(cut)
    
    def printBarcode(self, txt, barcode, characters='on', height=100, width='medium', parentheses='on', ratio='3:1', equalize='off'):
        '''
        characters='on', characters: Whether you want characters below the bar code. 'off' or 'on'
        height=100, height: Height, in dots.
        width='medium' width: width of barcode. Choose 'xsmall' 'small' 'medium' 'large'
        parentheses='on', parentheses: Parentheses deletion on or off. 'on' or 'off' Only matters with GS1-128
        ratio='3:1', ratio: ratio between thick and thin bars. Choose '3:1', '2.5:1', and '2:1'
        equalize='off' equalize: equalize bar lengths, choose 'off' or 'on'
        '''

        self.printjob.barcode(txt, barcode, characters, height, width, parentheses, ratio, equalize)
        self.printjob.print_page('full')
