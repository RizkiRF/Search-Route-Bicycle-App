import MySQLdb


class dataBase:

    def __init__(self, url, username, password, db):
        # Buka Konkesi ke database
        self.db = MySQLdb.connect(url, username, password, db)

        # Prepare cursor untuk menjalankan printah SQL
        self.cursor = self.db.cursor()

    # SQL Query Insert
    def insertDataBesar(self, idKen):
        # SQL Query
        sql = "INSERT INTO besar (kendaraan, waktu, tanggal) VALUES (%d,now(),now())" % (
            idKen)
        try:
            # Jalankan perintah SQL
            self.cursor.execute(sql)
            # Commit perubahan
            self.db.commit()
        except:
            #Rollback ketika ada kesalahan
            self.db.rollback()

    # SQL Query Insert
    def insertDataKecil(self, idKen):
        # SQL Query
        sql = "INSERT INTO kecil (kendaraan, waktu, tanggal) VALUES (%d,now(),now())" % (
            idKen)
        try:
            # Jalankan perintah SQL
            self.cursor.execute(sql)
            # Commit perubahan
            self.db.commit()
        except:
            #Rollback ketika ada kesalahan
            self.db.rollback()

    # SQL Query Insert
    def readDataBesar(self, time1, time2, date):
        # SQL Query
        try:
            if date == "CURDATE()" :
                sql = "SELECT kendaraan FROM besar where waktu >= '%s' and waktu <= '%s' and tanggal = %s ORDER BY id DESC LIMIT 1" % (
                    time1, time2, date)
            else :
                sql = "SELECT kendaraan FROM besar where waktu >= '%s' and waktu <= '%s' and tanggal = '%s' ORDER BY id DESC LIMIT 1" % (
                    time1, time2, date)
            res = self.cursor.execute(sql)
            if res == 0:
                hasil = "0"
            else:
                res2 = self.cursor.fetchall()
                for row in res2:
                    hasil = row[0]

            return hasil
        except:
            #Rollback ketika ada kesalahan
            print "ERROR"
            self.db.rollback()

    
    # SQL Query Insert
    def readDataKecil(self, time1, time2,date):
        # SQL Query
        try:
            if date == "CURDATE()":
                sql = "SELECT kendaraan FROM kecil where waktu >= '%s' and waktu <= '%s' and tanggal = %s ORDER BY id DESC LIMIT 1" % (
                    time1, time2, date)
            else:
                sql = "SELECT kendaraan FROM kecil where waktu >= '%s' and waktu <= '%s' and tanggal = '%s' ORDER BY id DESC LIMIT 1" % (
                    time1, time2, date)
            res = self.cursor.execute(sql)

            if res == 0:
                hasil = "0"
            else:
                res2 = self.cursor.fetchall()
                for row in res2:
                    hasil = row[0]

            return hasil
        except:
            #Rollback ketika ada kesalahan
            self.db.rollback()

    def databaseClose(self):
        # Disconect dari server
        self.db.close()
