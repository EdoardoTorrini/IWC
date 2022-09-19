import codecs


class StringElaborator:

    def __init__(self, sString):
        self.sString = sString
        self.dData = {}

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

            self.dData["plain"] = sRet

        else:
            nFindStart, sQuery = self.sString.find("--"), ""
            if nFindStart > -1:
                sTmp = self.sString[nFindStart:]
                sQuery = sTmp[:sTmp.find("\n")]

                if sQuery is not None:
                    aElemFormat = self.sString.split(sQuery)
                    aElemFormat.remove(aElemFormat[0])
                    for elem in aElemFormat:
                        if elem.find("Content-Type") > -1:
                            sTmp = elem.strip()

                            sKey = ""
                            for str in sTmp.split("\"\n"):
                                sKey = self.StringElaborator(str, sKey)
            else:
                sKey = ""
                for elem in self.sString.split("\n"):
                    if len(elem) > 0:
                        sKey = self.StringElaborator(elem, sKey)

        return self.dData

    def StringElaborator(self, sTmp, sKey):
        nFindStart = sTmp.find("Content-Type: ")
        if nFindStart > -1:
            sTmp = sTmp[nFindStart + len("Content-Type: "):]
            sKey = sTmp[:sTmp.find(";")].split("/")[1]
            self.dData[sKey] = ""
            return sKey
        else:
            self.dData[sKey] = sTmp.strip()
            return ""

