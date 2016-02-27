from libs import parser, printerFeatures


def getParseDict():
    parseDict = {}

    parseDict['sizesCmb'] = '<optgroup label="Outline Sizes">'
    parseDict['sizesCmb'] += parser.getCmbFromList(printerFeatures.sizesOutline)
    parseDict['sizesCmb'] += '</optgroup>'

    parseDict['sizesCmb'] += '<optgroup label="Bitmap Sizes">'
    parseDict['sizesCmb'] += parser.getCmbFromList(printerFeatures.sizesBitmap)
    parseDict['sizesCmb'] += '</optgroup>'

    parseDict['fontsCmb'] = '<optgroup label="Outline Fonts">'
    parseDict['fontsCmb'] += parser.getCmbFromList(printerFeatures.fontsOutline)
    parseDict['fontsCmb'] += '</optgroup>'

    parseDict['fontsCmb'] += '<optgroup label="Bitmap Fonts">'
    parseDict['fontsCmb'] += parser.getCmbFromList(printerFeatures.fontsBitMap)
    parseDict['fontsCmb'] += '</optgroup>'

    parseDict['alignsCmb'] = parser.getCmbFromList(printerFeatures.aligns)

    parseDict['charStylesCmb'] = parser.getCmbFromList(printerFeatures.charStyles)

    parseDict['cutsCmb'] = parser.getCmbFromList(printerFeatures.cuts)

    return parseDict