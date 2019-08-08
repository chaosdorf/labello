# coding: utf-8

# some compatibility with Python 3 (see #7)
from __future__ import print_function
from __future__ import unicode_literals

import socket
import imghdr
import logging
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
        self.printjob.select_char_code_table("western european")
    
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
        logging.debug("start printing: " + txt)
        
        self.printjob.select_font(font)
        self.printjob.char_size(charSize)  # 28 chars
        self.printjob.alignment(align)
        self.printjob.bold(bold)
        self.printjob.char_style(charStyle)
        self.printjob.cut_setting(cut)

        self.printjob.send(txt.encode('windows-1252', 'replace'))
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

        self.printjob.barcode(txt.encode('windows-1252', 'replace'), barcode, characters, height, width, parentheses, ratio, equalize)
        self.printjob.print_page('full')

    def printPicture(self, pictureBytes):
        pictureType = imghdr.what(None, h=pictureBytes)
        if pictureType is None:
            raise RuntimeError('NOT A VALID PICTURE!')
        elif pictureType not in ['jpeg', 'png', 'bmp']:
            raise RuntimeError('INVALID PICTURE TYPE: ' + pictureType)

        if pictureType == 'jpeg':
            pass
        elif pictureType == 'png':
            pass
