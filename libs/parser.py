def getCmbFromList(ls):
    cmb = ''
    for itm in ls:
        cmb += '<option value="' + str(itm) + '">' + str(itm) + '</option>'
    return cmb

def getPolymerFromList(ls):
    poly = ''
    for itm in ls:
        poly += '<paper-item>' + str(itm) + '</paper-item>'
    return poly
