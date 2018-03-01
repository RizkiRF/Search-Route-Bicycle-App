from db import dataBase
class getData :

    def __init__(self):
        self.kendaraanBesar = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]
        self.kendaraanKecil = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]

    def getDataKendaraanBesar(self,tanggal):
        db = dataBase("localhost", "root", "", "tf")
        j = 0
        for i in range(6, 18):
            parm1 = "0" + `i` +":00:00"
            parm2 = "0" + `i` +":59:59"
            self.kendaraanBesar[j] = db.readDataBesar(parm1, parm2, tanggal)
            j += 1
        return self.kendaraanBesar


    def getDataKendaraanKecil(self,tanggal):
        db = dataBase("localhost", "root", "", "tf")
        j = 0
        for i in range(6, 18):
            parm1 = "0" + `i` +":00:00"
            parm2 = "0" + `i` +":59:59"
            self.kendaraanKecil[j] = db.readDataKecil(parm1, parm2, tanggal)
            j += 1
        return self.kendaraanKecil
