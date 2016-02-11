#!/usr/bin/env python2
# coding: utf-8

import socket
from brotherprint import BrotherPrint

def getLined(txt):
	pass

f_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
f_socket.connect(('172.22.27.26', 9100))
printjob = BrotherPrint(f_socket)

printjob.command_mode()
printjob.initialize()
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
