#!/usr/bin/env python2

import argparse
import os

from labelprinter import Labelprinter

if os.path.isfile('labelprinterServeConf_local.py'):
    import labelprinterServeConf_local as conf
else:
    import labelprinterServeConf as conf

def text(args, labelprinter):
    bold = 'on' if args.bold else 'off'
    labelprinter.printText(args.text,
                charSize=args.char_size,
                font=args.font,
                align=args.align,
                bold=bold,
                charStyle=args.char_style,
                cut=args.cut
                )

parser = argparse.ArgumentParser(description="A command line interface to Labello.")
subparsers = parser.add_subparsers(help="commands")
parser_text = subparsers.add_parser("text", help="print a text")
parser_text.add_argument("text", type=str, help="the text to print")
parser_text.add_argument("--char_size", type=str, default='42')
parser_text.add_argument("--font", type=str, default='lettergothic')
parser_text.add_argument("--align", type=str, default='left')
parser_text.add_argument("--bold", action='store_true')
parser_text.add_argument("--char_style", type=str, default='normal')
parser_text.add_argument("--cut", type=str, default='full')
parser_text.set_defaults(func=text)

args = parser.parse_args()

labelprinter = Labelprinter(conf=conf)
args.func(args, labelprinter)
