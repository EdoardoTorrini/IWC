import codecs


class StringElaborator:

    def __init__(self, sString):
        self.sString = sString

    def getPlainText(self):

        nFind = self.sString.find("Content-Transfer-Encoding: ")
        sTmp, sRet = "", ""
        if nFind > -1:
            nLength = nFind + len("Content-Transfer-Encoding: ")
            sTmp = self.sString[nLength:]
            aTmp = sTmp.split("\n\n")

            match aTmp[0]:
                case "base64":
                    import base64
                    sRet = codecs.decode(base64.b64decode(codecs.encode(aTmp[1])))
                case "quoted-printable":
                    import quopri
                    sRet = quopri.decodestring(aTmp[1])
                case _:
                    print("porco dio")

        else:
            aRet = self.sString.split("\n\n")
            sRet = aRet[1]

        return sRet

