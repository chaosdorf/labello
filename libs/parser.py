def getCmbFromList(ls):
    cmb = ''
    for itm in ls:
        cmb += '<option value="' + str(itm) + '">' + str(itm) + '</option>'
    return cmb

def getArrayFromList(ls):
    cmb = '['
    for itm in ls:
        cmb += "'" + str(itm) + "',"
    cmb = cmb[:-1]
    cmb += ']'
    return cmb

def getPolymerFromList(ls):
    poly = ''
    for itm in ls:
        poly += '<paper-item>' + str(itm) + '</paper-item>'
    return poly
