import conans

class ConanFileInst(conans.ConanFile):
    def build(self):
        pass

    def test(self):
        self.run("asn1c -P {d}/rfc3280-PKIX1Explicit88.asn1".format(d=self.source_folder))
