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
                case "quoted-printable" | "7bit":
                    import quopri
                    sRet = quopri.decodestring(aTmp[1])
                case _:
                    print("porco dio")

        else:
            aRet = self.sString.split("\n\n")
            aRemoveElem = []

            for elem in aRet:

                if elem.find("--") > -1:
                    aRemoveElem.append(elem)

                elif elem.find("Content-Type") > -1:
                    aRemoveElem.append(elem)

            for elem in aRemoveElem:
                aRet.remove(elem)

            sRet = "".join(aRet)

        return sRet

