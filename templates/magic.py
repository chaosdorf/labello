from libs import parser, printerFeatures


def getParseDict():
    parseDict = {}

    parseDict['sizesCmb'] = parser.getCmbFromList(printerFeatures.sizesBitmap)
    parseDict['sizesCmb'] += parser.getCmbFromList(printerFeatures.sizesOutline)

    parseDict['sizesPoly'] = parser.getPolymerFromList(printerFeatures.sizesBitmap)

    parseDict['fontsCmb'] = '<optgroup label="Outline Fonts">'
    parseDict['fontsCmb'] += parser.getCmbFromList(printerFeatures.fontsOutline)
    parseDict['fontsCmb'] += '</optgroup>'

    parseDict['fontsCmb'] += '<optgroup label="Bitmap Fonts">'
    parseDict['fontsCmb'] += parser.getCmbFromList(printerFeatures.fontsBitMap)
    parseDict['fontsCmb'] += '</optgroup>'

    parseDict['fontsPoly'] = '<polymer-item disabled>Outline Fonts</polymer-item>'
    parseDict['fontsPoly'] += parser.getPolymerFromList(printerFeatures.fontsOutline)

    parseDict['fontsPoly'] += '<polymer-item disabled>Bitmap Fonts</polymer-item>'
    parseDict['fontsPoly'] += parser.getPolymerFromList(printerFeatures.fontsBitMap)

    parseDict['alignsCmb'] = parser.getCmbFromList(printerFeatures.aligns)
    parseDict['alignsPoly'] = parser.getPolymerFromList(printerFeatures.aligns)

    parseDict['charStylesCmb'] = parser.getCmbFromList(printerFeatures.charStyles)
    parseDict['charStylePoly'] = parser.getPolymerFromList(printerFeatures.charStyles)

    parseDict['cutsCmb'] = parser.getCmbFromList(printerFeatures.cuts)
    parseDict['cutsPoly'] = parser.getPolymerFromList(printerFeatures.cuts)

    return parseDict
