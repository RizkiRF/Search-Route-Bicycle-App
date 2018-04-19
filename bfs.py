import random as rand

class Bfs:
    def __init__(self, awal, tujuan, peta):
        self.titik_awal = awal
        self.titik_akhir = tujuan
        self.peta_ = peta
        self.hasil = 0

    def proses_searching(self):
        queue = [[self.titik_awal]]
        visited = set()
        i=1
        while queue:
            print i,' : ' , queue
            i+=1
            cabang_rand = []
            ambil_jalur = queue.pop(0)
            # simpan node yang dipilih ke variabel state, misal jalur = C,B maka simpan B ke variabel state
            ambil_node = ambil_jalur[-1]
            
            
            # cek state apakah sama dengan tujuan, jika ya maka return jalur
            if ambil_node == self.titik_akhir:
                h = ''.join(ambil_jalur)

                return h
            # jika state tidak sama dengan tujuan, maka cek apakah state tidak ada di visited
            elif ambil_node not in visited:
                for cabang in self.peta_.get(ambil_node,[]):
                    cabang_rand.append(cabang)
                rand.shuffle(cabang_rand)
                # jika state tidak ada di visited maka cek cabang
                for x in cabang_rand:  # cek semua cabang dari state
                    # masukkan isi dari variabel jalur ke variabel jalur_baru
                    jalur_baru = list(ambil_jalur)
                    # update/tambah isi jalur_baru dengan cabang
                    jalur_baru.append(x)
                    # update/tambah queue dengan jalur_baru
                    queue.append(jalur_baru)

                # tandai state yang sudah dikunjungi sebagai visited
                visited.add(ambil_node)

            #cek isi antrian
            isi = len(queue)
            if isi == 0:
                print("Tidak ditemukan")
