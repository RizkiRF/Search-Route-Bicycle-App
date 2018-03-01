import cv2
import sys
import numpy
from flask import Flask, render_template, flash, redirect, url_for, request, session, logging, Response, jsonify
from getData import getData
from count import count

app = Flask(__name__)
cont = count()
getDataKen = getData()

@app.route('/')
def index():
    return render_template('index.html')

def get_frame():
    # this makes a web cam object
    camera = cv2.VideoCapture('rtsp://www.lalinsemarang.info:1935/live/tugumuda.stream')
    i = 1
    while True:
        orgi = cont.frameOriginal(camera)
        treshold = cont.frameTrehold(camera)
        stringData = cont.findContours(treshold, orgi)
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        i += 1
    del(camera)


@app.route('/calc')
def calc():
     return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/laporan', methods = ['GET','POST'])
def lapor():
    totalKendaraan = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13,14]
    # Result
    if request.method == "POST" :
        j=0
        kendaraanBesar = getDataKen.getDataKendaraanBesar(request.form['tanggal'])
        kendaraanKecil = getDataKen.getDataKendaraanKecil(request.form['tanggal'])
        for i in range(6,18):
            totalKendaraan[j] = int(kendaraanBesar[j]) + int(kendaraanKecil[j])
            j+=1
        return render_template('laporan.html', kendaraanBesars=kendaraanBesar, kendaraanKecils=kendaraanKecil, totalKendaraans=totalKendaraan)
    if request.method == "GET":
        j = 0
        kendaraanBesar = getDataKen.getDataKendaraanBesar("CURDATE()")
        kendaraanKecil = getDataKen.getDataKendaraanKecil("CURDATE()")
        for i in range(6,18):
            totalKendaraan[j] = int(kendaraanBesar[j]) + int(kendaraanKecil[j])
            j+=1
        return render_template('laporan.html', kendaraanBesars=kendaraanBesar, kendaraanKecils=kendaraanKecil, totalKendaraans=totalKendaraan)
    return render_template('laporan.html')


@app.route('/data')
def data():
    res = getDataKen.kendaraanBesar
    res2 = getDataKen.kendaraanKecil
    return jsonify({'besar': res, 'kecil': res2})


@app.route('/tentang')
def about():
    return render_template('tentang.html')


# Debug = True -> Agar auto relod server
if __name__ == '__main__':
    app.run( debug=True, threaded=True)
