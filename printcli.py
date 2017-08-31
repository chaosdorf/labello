#!/usr/bin/env python2

import argparse
import os

from labelprinter import Labelprinter
import labelprinterServeConf as conf

def show_config(args, labelprinter):
    for var in dir(conf):
        if(var.isupper()):
            print("{} = {}".format(var, conf.__getattribute__(var)))

def text(args, labelprinter):
    bold = 'on' if args.bold else 'off'
    labelprinter.printText(args.text.decode('utf-8'),
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
parser_config = subparsers.add_parser("config", help="show the config")
parser_config.set_defaults(func=show_config)

args = parser.parse_args()

if args.func != show_config:
    labelprinter = Labelprinter(conf=conf)
else:
    labelprinter = None
args.func(args, labelprinter)
