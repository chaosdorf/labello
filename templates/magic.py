from libs import parser, printerFeatures


def getParseDict():
    parseDict = {}

    parseDict['sizesBitmap'] = parser.getArrayFromList(printerFeatures.sizesBitmap)
    parseDict['sizesOutline'] = parser.getArrayFromList(printerFeatures.sizesOutline)

    parseDict['fontsOutline'] = parser.getArrayFromList(printerFeatures.fontsOutline)
    parseDict['fontsBitMap'] = parser.getArrayFromList(printerFeatures.fontsBitMap)

    parseDict['aligns'] = parser.getArrayFromList(printerFeatures.aligns)

    parseDict['charStyles'] = parser.getArrayFromList(printerFeatures.charStyles)

    parseDict['cuts'] = parser.getArrayFromList(printerFeatures.cuts)

    return parseDict
