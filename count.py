# Library
import numpy as np
import cv2
import Person
from db import dataBase
import time


class count:

    def __init__(self):
        #Inisialisasi Database
        self.data = dataBase("localhost", "root", "", "tf")

        #Definisi awal perhitungan
        self.cnt_up_kecil = 0
        self.cnt_up_besar = 0
        self.cnt_down = 0
        self.jam_sk = 0
        self.jam_sb = 10
        self.menit_sk = 0
        self.menit_sb = 50

        self.w = 380
        self.h = 540
        self.frameArea = self.h*self.w
        self.areaTH =35

        #Koordinat Posisi Line, dihitung dari pojok kiri atas
        self.line_up = 230
        self.line_down = 100

        self.up_limit = 50
        self.down_limit = 260

        self.line_down_color = (255, 0, 0)
        self.line_up_color = (0, 0, 255)
        self.pt1 = [0, self.line_down]  # Titik awal garis down
        self.pt2 = [self.w+150, self.line_down]  # Titik akhir garis down
        self.pts_L1 = np.array([self.pt1, self.pt2], np.int32)  # Mulai mengaris
        self.pts_L1 = self.pts_L1.reshape((-1, 1, 2))  # Ukuran garis

        self.pt3 = [0, self.line_up]  # Titik awal garis up
        self.pt4 = [self.w+150, self.line_up]  # Titik akhir garis up
        self.pts_L2 = np.array([self.pt3, self.pt4], np.int32)
        self.pts_L2 = self.pts_L2.reshape((-1, 1, 2))

        self.pt5 = [0, self.up_limit]
        self.pt6 = [self.w+150, self.up_limit]
        self.pts_L3 = np.array([self.pt5, self.pt6], np.int32)
        self.pts_L3 = self.pts_L3.reshape((-1, 1, 2))

        self.pt7 = [0, self.down_limit]
        self.pt8 = [self.w+150, self.down_limit]
        self.pts_L4 = np.array([self.pt7, self.pt8], np.int32)
        self.pts_L4 = self.pts_L4.reshape((-1, 1, 2))

        #Substraksi
        self.fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

        #Kernel Morfologi (Dilasi dan Erosi) | Dilasi : Closing, Erosi : Opening
        self.kernelOp = np.ones((5, 5), np.uint8)
        #kernelOp2 = np.ones((5,5),np.uint8)
        self.kernelCl = np.ones((10, 10), np.uint8)

        #Variables
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.persons = []
        self.max_p_age = 5
        self.pid = 1

    def frameOriginal(self,cap):
        retval, im = cap.read()
        im = cv2.resize(im, (540, 380))
        
        return im

    def frameTrehold(self,cap): 
        retval, im = cap.read()
        im = cv2.resize(im, (540, 380))
        for i in self.persons:
            i.age_one()  # 1 Objek 1 Frame
        #########################
        #   PRE-PROSESING       #
        #########################

        #Gunakan substraksi yang telah di siapkan
        fgmask = self.fgbg.apply(im)

        #Setelah di substraksi, dilakukan treshold agar hasilnya lebih bagus
        #imBin = Ke atas
        #imBin2 = Kebawah

        ret, imBin = cv2.threshold(fgmask, 220, 255, cv2.THRESH_BINARY)

        #Morfologi untuk memperjelas bentuk
        #Opening (erode->dilate)
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, self.kernelOp)

        #Closing (dilate -> erode)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernelCl)

        return mask


    def findContours(self,mask,frame):
        _, contours0, hierarchy = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for cnt in contours0:
            area = cv2.contourArea(cnt)
            if area > self.areaTH:
                #################
                #   TRACKING    #
                #################

                M = cv2.moments(cnt)
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                x, y, w, h = cv2.boundingRect(cnt)
                new = True
                if cy in range(self.up_limit, self.down_limit):
                    for i in self.persons:
                        if abs(cx-i.getX()) <= w and abs(cy-i.getY()) <= h:
                            new = False
                            i.updateCoords(cx, cy)
                            if i.going_UP(self.line_down, self.line_up) == True: # Saat objek bergerak ke atas
                                self.jam_sk = time.strftime("%H")
                                self.menit_sk = time.strftime("%M")
                                if int(self.jam_sk) > int(self.jam_sb) and int(self.menit_sk) < int(self.menit_sb):
                                        self.cnt_up_kecil = 0
                                        self.cnt_up_besar = 0

                                if(area >= self.areaTH and area <= self.areaTH+220) :
                                    self.jam_sb = time.strftime("%H")
                                    self.menit_sb = time.strftime("%M")
                                    self.cnt_up_kecil += 1
                                    self.data.insertDataKecil(self.cnt_up_kecil) #Insert data ke database
                                else :
                                    self.jam_sb = time.strftime("%H")
                                    self.menit_sb = time.strftime("%M")
                                    self.cnt_up_besar += 1
                                    self.data.insertDataBesar(self.cnt_up_besar) #Insert data ke database
                                
                            elif i.going_DOWN(self.line_down, self.line_up) == True: #Saat objek bergerak ke bawah
                                self.cnt_down += 1
                                #self.data.insertData(self.cnt_down) #Insert data ke database
                            break
                        if i.getState() == '1':
                            if i.getDir() == 'down' and i.getY() > self.down_limit:
                                i.setDone()
                            elif i.getDir() == 'up' and i.getY() < self.up_limit:
                                i.setDone()
                        if i.timedOut():
                            index = self.persons.index(i)
                            self.persons.pop(index)
                            del i
                    if new == True:
                        p = Person.MyPerson(self.pid, cx, cy, self.max_p_age)
                        self.persons.append(p)
                        self.pid += 1

                # Gambar titik merah pada objek
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                # Gambar kotak hijau pada objek
                img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # Gambar Garis bentuk objek
                #cv2.drawContours(frame, cnt, -1, (0, 255, 0),3) 

        for i in self.persons:
            #Pada bagian ini dikomentar karena, bagian ini melakukan tracking pergerakan objek
            ##        if len(i.getTracks()) >= 2:
            ##            pts = np.array(i.getTracks(), np.int32)
            ##            pts = pts.reshape((-1,1,2))
            ##            frame = cv2.polylines(frame,[pts],False,i.getRGB())
            ##        if i.getId() == 9:
            ##            print str(i.getX()), ',', str(i.getY())
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()),self.font, 0.3, i.getRGB(), 1, cv2.LINE_AA)

        #################
        #   GAMBAR      #
        #################
        str_up = 'Besar: ' + str(self.cnt_up_besar)
        str_down = 'Kecil: ' + str(self.cnt_up_kecil)
        frame = cv2.polylines(frame, [self.pts_L1], False, self.line_down_color, thickness=2)
        frame = cv2.polylines(frame, [self.pts_L2], False, self.line_up_color, thickness=2)
        frame = cv2.polylines(frame, [self.pts_L3], False, (255, 255, 255), thickness=1)
        frame = cv2.polylines(frame, [self.pts_L4], False, (255, 255, 255), thickness=1)
        cv2.putText(frame, str_up, (10, 40), self.font, 0.5,(255, 255, 255), 2, cv2.LINE_AA)  # Stroke
        cv2.putText(frame, str_up, (10, 40), self.font, 0.5,(0, 0, 255), 1, cv2.LINE_AA)  # Warna Font
        cv2.putText(frame, str_down, (10, 90), self.font, 0.5,(255, 255, 255), 3, cv2.LINE_AA)  # Stroke
        cv2.putText(frame, str_down, (10, 90), self.font, 0.5,(255, 0, 0), 2, cv2.LINE_AA)  # Warna Font


        #Konverter Image
        # Dilakukan konverter karena dari proses image agar dapat diload di web
        # harus di konversikan ke binary yang kemudian di load di web binary menjadi sebuah gambar
        imgencode = cv2.imencode('.png', frame)[1]
        stringData = imgencode.tostring()
        return stringData
