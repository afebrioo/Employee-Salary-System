from tabulate import tabulate as tb

list_DirSDM = {}
list_Direktur = {}

class Admin:
    def __init__(self):
        self.id = None
        self.is_logged_in = False 
        self.username = None
        self.__password = None
    
    def login(self, username, password):
        if username == "admin" and password == "123":
            self.is_logged_in = True
            self.username = username
            self.__password = password
            return "\nSelamat datang di Menu Admin."
        else:
            return "Invalid username or password."
    
    def edit(self):
        if self.is_logged_in:
            print("======== Menu Admin ========\n")
            x = int(input("Masukkan Menu yang ingin di edit\n1.Direktur SDM\n2.Direktur\n"))
            if x == 1:
                list_DirSDM["Nama"] = input("Masukkan nama Direktur SDM : ")
                list_DirSDM["Password"] = input("Masukkan password Direktur SDM : ")
                file = open('c:/college/PBO/List Direktur SDM.txt', 'w')
                file.write(f"Nama Direktur SDM : \n{list_DirSDM['Nama']}\n")
                file.write(f"Password : {list_DirSDM['Password']}\n")
                print("Data Direktur SDM Berhasil di input.")
            elif x == 2:
                list_Direktur["Nama"] = input("Masukkan nama Direktur : ")
                list_Direktur["Password"] = input("Masukkan password Direktur : ")
                file = open('c:/college/PBO/List Direktur.txt', 'w')
                file.write(f"Nama Direktur : {list_Direktur['Nama']}\n")
                file.write(f"Password : {list_Direktur['Password']}\n")
                print("Data Direktur Berhasil di input.")
        else:
            return "Invalid"

        
class DirekturSDM:
    def __init__(self):
        self.is_logged_in = False
        self.pegawai_dict = {}
        self.divisi_dict = {}

    def login(self, username, password):
        file = open('c:/college/PBO/List Direktur SDM.txt', 'r')
        content = file.read()

        if username in content and password in content:
            self.is_logged_in = True
            return "\nSelamat datang di Menu Direktur SDM."
        else:
            return "Invalid username or password."

    def tambah_pegawai(self, nip, nama, jabatan, divisi):
        pegawai = {
            'nama': nama,
            'jabatan': jabatan,
            'divisi': divisi,
            'gaji_pokok': 0,
            'gaji_per_jam': 0
        }
        self.pegawai_dict[nip] = pegawai

        if divisi not in self.divisi_dict:
            self.divisi_dict[divisi] = {'standar_gaji': 0, 'jumlah_pegawai': 0}

    def edit_pegawai(self, nip, nama=None, jabatan=None, divisi=None):
        if nip in self.pegawai_dict:
            pegawai = self.pegawai_dict[nip]
            if nama is not None:
                pegawai['nama'] = nama
            if jabatan is not None:
                pegawai['jabatan'] = jabatan
            if divisi is not None:
                pegawai['divisi'] = divisi
        else:
            print(f"Pegawai dengan NIP {nip} tidak ditemukan.")

    def tambah_gaji(self, nip, gaji_pokok, gaji_per_jam):
        if nip in self.pegawai_dict:
            pegawai = self.pegawai_dict[nip]
            pegawai['gaji_pokok'] = gaji_pokok
            pegawai['gaji_per_jam'] = gaji_per_jam
        else:
            print(f"Pegawai dengan NIP {nip} tidak ditemukan.")

    def edit_gaji(self, nip, gaji_pokok=None, gaji_per_jam=None):
        if nip in self.pegawai_dict:
            pegawai = self.pegawai_dict[nip]
            if gaji_pokok is not None:
                pegawai['gaji_pokok'] = gaji_pokok
            if gaji_per_jam is not None:
                pegawai['gaji_per_jam'] = gaji_per_jam
        else:
            print(f"Pegawai dengan NIP {nip} tidak ditemukan.")

    def tampilkan_semua_pegawai(self, urut='nip'):
        sorted_pegawai = sorted(self.pegawai_dict.items(), key=lambda x: x[1].get(urut, 0))
        headers = ["NIP", "Nama", "Jabatan", "Divisi", "Gaji Pokok", "Gaji per Jam"]
        data = [[nip, pegawai['nama'], pegawai['jabatan'], pegawai['divisi'], pegawai['gaji_pokok'], pegawai.get('gaji_per_jam', 0)] for nip, pegawai in sorted_pegawai]
        print(tb(data, headers=headers, stralign="right"))


    def tampilkan_gaji_bulan(self, bulan, urut='nip'):
        sorted_pegawai = sorted(self.pegawai_dict.values(), key=lambda x: x['gaji_pokok'] + x.get('gaji_per_jam', 0))
        for nip, pegawai in self.pegawai_dict.items():
            gaji_total = pegawai['gaji_pokok']
            if 'gaji_per_jam' in pegawai:
                # Fungsi jam_kerja_bulan harus diimplementasikan sesuai kebutuhan
                gaji_total += pegawai['gaji_per_jam'] * jam_kerja_bulan(nip, bulan)
            print(f"NIP: {nip}, Nama: {pegawai['nama']}, Gaji Bulan {bulan}: {gaji_total}")

    def tampilkan_list_divisi(self):
        print("List Divisi:")
        for divisi in self.divisi_dict.keys():
            print(divisi)

    def tampilkan_list_divisi_gaji(self):
        print("List Divisi beserta Standar Gajinya:")
        print("HR  : 1.000.000")
        print("IT  : 2.000.000")
        print("RND : 3.000.000")

    def tampilkan_pegawai_divisi(self, divisi):
        print(f"List Pegawai di Divisi {divisi}:")
        for nip, pegawai in self.pegawai_dict.items():
            if pegawai['divisi'] == divisi:
                print(f"NIP: {nip}, Nama: {pegawai['nama']}, Jabatan: {pegawai['jabatan']}")

    def tampilkan_pejabat_kantor(self):
        for nip, pegawai in self.pegawai_dict.items():
            if pegawai['jabatan'] in ['Direktur', 'Manager']:
                print(f"NIP: {nip}, Nama: {pegawai['nama']}, Jabatan: {pegawai['jabatan']}")

    def tampilkan_total_gaji_bulan(self, bulan):
        total_gaji = 0
        for nip, pegawai in self.pegawai_dict.items():
            gaji_total = pegawai['gaji_pokok']
            if 'gaji_per_jam' in pegawai:
                # Fungsi jam_kerja_bulan harus diimplementasikan sesuai kebutuhan
                gaji_total += pegawai['gaji_per_jam'] * jam_kerja_bulan(nip, bulan)
            total_gaji += gaji_total
        print(f"Total Gaji yang Harus Dibayar pada Bulan {bulan}: {total_gaji}")


# Fungsi untuk mendapatkan jam kerja pegawai pada bulan tertentu
def jam_kerja_bulan(nip,bulan):
    if  bulan == "januari" :
        x = int(input(f"Masukkan jam kerja anda di bulan {bulan} : "))
        return x
    elif bulan == "februari":
        x = int(input("Masukkan jam kerja anda di bulan februari : "))
        return x
    elif bulan == "maret" :
        x = int(input("Masukkan jam kerja anda di bulan maret : ")) 
        return x
    elif bulan == "april" : 
        x = int(input("Masukkan jam kerja anda di bulan april : "))
        return x
    elif bulan == "mei" : 
        x = int(input("Masukkan jam kerja anda di bulan mei : "))
        return x
    elif bulan == "juni":
        x = int(input("Masukkan jam kerja anda di bulan juni : "))
        return x
    elif bulan == "juli" :
        x = int(input("Masukkan jam kerja anda di bulan juli : ")) 
        return x
    elif bulan == "agustus" : 
        x = int(input("Masukkan jam kerja anda di bulan agustus : "))
        return x
    elif bulan == "september" : 
        x = int(input("Masukkan jam kerja anda di bulan september : "))
        return x
    elif bulan == "oktober" : 
        x = int(input("Masukkan jam kerja anda di bulan oktober : "))
        return x
    elif bulan == "november" : 
        x = int(input("Masukkan jam kerja anda di bulan november : "))
        return x
    elif bulan == "desember" : 
        x = int(input("Masukkan jam kerja anda di bulan desember : "))
        return x
    return x

class Direktur(DirekturSDM):
    def __init__(self):
        super().__init__()
    
    def login(self, username, password):
        file = open('c:/college/PBO/List Direktur.txt', 'r')
        content = file.read()

        if username in content and password in content:
            self.is_logged_in = True
            return "\nSelamat datang di Menu Direktur."
        else:
            return "Invalid username or password."
    
    def tampilkan_semua_pegawai(self, urut='nip'):
        sorted_pegawai = sorted(self.pegawai_list, key=lambda x: x[urut])
        headers = ["NIP", "Nama", "Jabatan", "Divisi", "Gaji Pokok", "Gaji per Jam"]
        data = [[pegawai['nip'], pegawai['nama'], pegawai['jabatan'], pegawai['divisi'], pegawai['gaji_pokok'], pegawai.get('gaji_per_jam', 0)] for pegawai in sorted_pegawai]
        print(tb(data, headers=headers, stralign="right"))

    def tampilkan_gaji_bulan(self, bulan, urut='nip'):
        sorted_pegawai = sorted(self.pegawai_list, key=lambda x: x['gaji_pokok'] + x.get('gaji_per_jam', 0))
        for pegawai in sorted_pegawai:
            gaji_total = pegawai['gaji_pokok']
            if 'gaji_per_jam' in pegawai:
                # Fungsi jam_kerja_bulan harus diimplementasikan sesuai kebutuhan
                gaji_total += pegawai['gaji_per_jam'] * jam_kerja_bulan(pegawai['nip'], bulan)
            print(f"NIP: {pegawai['nip']}, Nama: {pegawai['nama']}, Gaji Bulan {bulan}: {gaji_total}")

    def tampilkan_list_divisi(self):
        print("List Divisi:")
        for divisi in self.divisi_list:
            print(divisi)

    def tampilkan_list_divisi_gaji(self):
        print("List Divisi beserta Standar Gajinya:")
        print("List Divisi beserta Standar Gajinya:")
        print("HR  : 1.000.000")
        print("IT  : 2.000.000")
        print("RND : 3.000.000")

    def tampilkan_pegawai_divisi(self, divisi):
        print(f"List Pegawai di Divisi {divisi}:")
        for pegawai in self.pegawai_list:
            if pegawai['divisi'] == divisi:
                print(f"NIP: {pegawai['nip']}, Nama: {pegawai['nama']}, Jabatan: {pegawai['jabatan']}")

    def tampilkan_pejabat_kantor(self):
        for pegawai in self.pegawai_list:
            if pegawai['jabatan'] in ['Direktur', 'Manager']:
                print(f"NIP: {pegawai['nip']}, Nama: {pegawai['nama']}, Jabatan: {pegawai['jabatan']}")

    def tampilkan_total_gaji_bulan(self, bulan):
        total_gaji = 0
        for pegawai in self.pegawai_list:
            gaji_total = pegawai['gaji_pokok']
            if 'gaji_per_jam' in pegawai:
                # Fungsi jam_kerja_bulan harus diimplementasikan sesuai kebutuhan
                gaji_total += pegawai['gaji_per_jam'] * jam_kerja_bulan(pegawai['nip'], bulan)
            total_gaji += gaji_total
        print(f"Total Gaji yang Harus Dibayar pada Bulan {bulan}: {total_gaji}")

def input_data_pegawai(direktur_sdm, jumlah_pegawai, menu):
    for _ in range(jumlah_pegawai):
        nip = input("\nMasukkan NIP Pegawai: ")
        nama = input("Masukkan Nama Pegawai: ")
        jabatan = input("Masukkan Jabatan Pegawai: ")
        divisi = input("Masukkan Divisi Pegawai: ")
        
        if menu == 1:
            direktur_sdm.tambah_pegawai(nip, nama, jabatan, divisi)
        elif menu == 2:
            gaji_pokok = int(input("Masukkan Gaji Pokok Pegawai: "))
            gaji_per_jam = int(input("Masukkan Gaji per Jam Pegawai: "))
            direktur_sdm.tambah_gaji(nip, gaji_pokok, gaji_per_jam)
    
    return direktur_sdm

def main(direktur_sdm):
    jawab = "ya"
    while jawab.lower() == "ya":
        print("Selamat datang di aplikasi Gaji Pegawai !")
        print("1. Admin")
        print("2. Direktur SDM")
        print("3. Direktur")
        x = int(input("Masukkan pilihan menu anda : "))
        
        if x == 1:
            admin = Admin()
            while not admin.is_logged_in:
                user = input("Masukkan username : ")
                pw = input("Masukkan password   : ")
                hasil = admin.login(user, pw)
                print(hasil)
                if admin.is_logged_in:
                    admin.edit()

        elif x == 2:
            direktur_sdm = DirekturSDM()
            while not direktur_sdm.is_logged_in:
                user = input("Masukkan username : ")
                pw = input("Masukkan password   : ")
                hasil = direktur_sdm.login(user, pw)
                print(hasil)

            if direktur_sdm.is_logged_in:
                jawab = "ya"
                while jawab.lower() == "ya":
                    print("\n1. Menambah, mengedit data pegawai")
                    print("2. Menambah, mengedit data gaji pokok dan gaji per jam")
                    print("3. Menampilkan semua list pegawai beserta atribut data lainnya dengan urut NIP")
                    print("4. Menampilkan list pegawai dan gajinya pada bulan tertentu dengan urut NIP atau urut gaji")
                    print("5. Menampilkan list divisi")
                    print("6. Menampilkan list divisi beserta standar gajinya")
                    print("7. Menampilkan list pegawai di divisi tertentu")
                    print("8. Menampilkan daftar pejabat di kantor")
                    print("9. Menampilkan total gaji yang harus dibayar setiap bulan")
                    y = int(input("Masukkan pilihan menu anda : "))

                    if y in [1, 2]:
                        a = int(input("Masukkan jumlah pegawai yang ingin di input : "))
                        direktur_sdm = input_data_pegawai(direktur_sdm, a, y)
                    elif y == 3:
                        direktur_sdm.tampilkan_semua_pegawai()
                    elif y == 4:
                        bulan = input("\nMasukkan Bulan untuk Menampilkan Gaji: ")
                        print(f"\nGaji Pegawai pada Bulan {bulan}: ")
                        direktur_sdm.tampilkan_gaji_bulan(bulan)
                    elif y == 5:
                        direktur_sdm.tampilkan_list_divisi()
                    elif y == 6:
                        direktur_sdm.tampilkan_list_divisi_gaji()
                    elif y == 7:
                        divisi = input("\nMasukkan Divisi untuk Menampilkan Pegawai: ")
                        print(f"\nPegawai di Divisi {divisi}:")
                        direktur_sdm.tampilkan_pegawai_divisi(divisi)
                    elif y == 8:
                        print("\nDaftar Pejabat di Kantor:")
                        direktur_sdm.tampilkan_pejabat_kantor()
                    elif y == 9:
                        bulan_total_gaji = input("\nMasukkan Bulan untuk Menampilkan Total Gaji: ")
                        print(f"\nTotal Gaji yang Harus Dibayar pada Bulan {bulan_total_gaji}:")
                        direktur_sdm.tampilkan_total_gaji_bulan(bulan_total_gaji)

                    jawab = input("Apakah ingin kembali ke menu Direktur SDM? (ya/tidak): ")
                    if jawab.lower() != "ya":
                        main(direktur_sdm)
        
        elif x == 3 :
            direktur = Direktur()
            while not direktur.is_logged_in:
                user = input("Masukkan username : ")
                pw = input("Masukkan password   : ")
                hasil = direktur.login(user, pw)
                print(hasil)

            if direktur.is_logged_in:
                jawab = "ya"
                while jawab == "ya":
                    print("1. Menampilkan semua list pegawai beserta atribut data lainnya dengan urut NIP")
                    print("2. Menampilkan list pegawai dan gajinya pada bulan tertentu dengan urut NIP atau urut gaji")
                    print("3. Menampilkan list divisi")
                    print("4. Menampilkan list divisi beserta standar gajinya")
                    print("5. Menampilkan list pegawai di divisi tertentu")
                    print("6. Menampilan daftar pejabat di kantor")
                    print("7. Menampilkan total gaji yang harus dibayar setiap bulan")
                    y = int(input("Masukkan pilihan menu anda : "))
                    if y == 1 :
                        direktur_sdm.tampilkan_semua_pegawai()
                    elif y == 2 :
                        bulan = input("\nMasukkan Bulan untuk Menampilkan Gaji: ")
                        print(f"\nGaji Pegawai pada Bulan {bulan}: ")
                        direktur_sdm.tampilkan_gaji_bulan(bulan)
                    elif y == 3 :
                        direktur_sdm.tampilkan_list_divisi()
                    elif y == 4 :
                        direktur_sdm.tampilkan_list_divisi_gaji()
                    elif y == 5 :
                        divisi = input("\nMasukkan Divisi untuk Menampilkan Pegawai: ")
                        print(f"\nPegawai di Divisi {divisi}:")
                        direktur_sdm.tampilkan_pegawai_divisi(divisi)
                    elif y == 6 :
                        print("\nDaftar Pejabat di Kantor:")
                        direktur_sdm.tampilkan_pejabat_kantor()
                    elif y == 7 :
                        bulan_total_gaji = input("\nMasukkan Bulan untuk Menampilkan Total Gaji: ")
                        print(f"\nTotal Gaji yang Harus Dibayar pada Bulan {bulan_total_gaji}:")
                        direktur_sdm.tampilkan_total_gaji_bulan(bulan_total_gaji)
                    jawab = input("Apakah masih ingin menggunakan?(ya/tidak): ")
                print("Thankyou for using our Services, Logged out.")
        else : 
            return f"Invalid submit."
                    
if __name__ == "__main__":
    main(DirekturSDM)
