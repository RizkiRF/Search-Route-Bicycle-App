#import modul random
import random as rand

class Dfs:
    def __init__(self, awal, tujuan, peta):
        self.titik_awal = awal
        self.titik_akhir = tujuan
        self.peta_ = peta
        self.hasil = 0

    def proses_searching(self):
        stack = [[self.titik_awal]]
        visited = set()
        while stack:
            #hitung panjang tumpukan dan masukkan ke variabel panjang_tumpukan
            banyak_tumpukan = len(stack)-1
            cabang_rand = []
            # masukkan tumpukan palinif state == tujuan:g atas ke variabel jalur
            ambil_jalur = stack.pop(banyak_tumpukan)

            # simpan node yang dipilih ke variabel state, misal jalur = C,B maka simpan B ke variabel state
            ambil_node = ambil_jalur[-1]

            # cek state apakah sama dengan tujuan, jika ya maka return jalur
            if ambil_node == self.titik_akhir:
                h = ''.join(ambil_jalur)
                print h
                #selesai
                return h
                
            # jika state tidak sama dengan tujuan, maka cek apakah state tidak ada di visited
            elif ambil_node not in visited:
                # jika state tidak ada di visited maka cek cabang
                for cabang in self.peta_.get(ambil_node,[]):
                    cabang_rand.append(cabang) #Memasukan ke list cabang_rand
                
                rand.shuffle(cabang_rand)

                for x in cabang_rand:  # cek semua cabang dari state
                    # masukkan isi dari variabel jalur ke variabel jalur_baru
                    jalur_baru = list(ambil_jalur)
                    # update/tambah isi jalur_baru dengan cabang
                    jalur_baru.append(x)
                    # update/tambah queue dengan jalur_baru
                    stack.append(jalur_baru)

                # tandai state yang sudah dikunjungi sebagai visited
                visited.add(ambil_node)

            #cek isi tumpukan
            isi = len(stack)
            if isi == 0:
                print("Tidak ditemukan")
