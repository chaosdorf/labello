from libs import parser, printerFeatures


def getParseDict():
    parseDict = {}

    parseDict['barcodesCmb'] = parser.getCmbFromList(printerFeatures.barcodes)

    parseDict['barcodeWidthCmb'] = parser.getCmbFromList(printerFeatures.barcodeWidth)

    parseDict['barcodeRatioCmb'] = parser.getCmbFromList(printerFeatures.barcodeRatio)

    return parseDict