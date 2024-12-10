#Nama : Maulana Nur Hidayat
#NPM  : 2413020149

import time
import datetime

TARIF_PS = {
    "PS3": 5000,
    "PS4": 8000,
    "PS5": 10000
}
pelanggan_aktif = {}
print("Sistem Billing PlayStation\n")

while True:
    print("\nPilihan:")
    print("1. Tambah pelanggan baru")
    print("2. Selesaikan transaksi pelanggan")
    print("3. Keluar")
    
    pilihan = input("Pilih opsi (1/2/3): ")

    if pilihan == "1":
        print("\nPilih tipe PlayStation:")
        for tipe, tarif in TARIF_PS.items():
            print(f"- {tipe} (Rp{tarif:,}/jam)")

        while True:
            tipe_ps = input("Masukkan tipe PlayStation (PS3/PS4/PS5): ").upper()
            if tipe_ps in TARIF_PS:
                break
            print("Tipe PlayStation tidak valid, silakan pilih PS3, PS4, atau PS5.")

        tarif_per_jam = TARIF_PS[tipe_ps]

        nama_pelanggan = input("Nama pelanggan: ").upper()
        print("Sistem Billing: ")
        print("1. Main per jam")
        print("2. Unlimited waktu")
        sistem_billing = input("Masukkan sistem billing : ")
        if sistem_billing == '1':
            durasi_jam = float(input("Durasi bermain (jam): "))
            durasi_detik = int(durasi_jam * 3600)

# Hitung biaya
            biaya = round(durasi_jam * tarif_per_jam)
            print(f"\nPelanggan: {nama_pelanggan}")
            print(f"Tipe PlayStation: {tipe_ps}")
            print(f"Durasi bermain: {durasi_jam} jam")
            print(f"Biaya: Rp{biaya:,}")

# Mulai hitung mundur
            waktu_mulai = time.time()
            waktu_berakhir = waktu_mulai + durasi_detik
            
            pelanggan_aktif[nama_pelanggan] = {
                "tipe_ps": tipe_ps,
                "tarif_per_jam": tarif_per_jam,
                "waktu_masuk": waktu_masuk
            }
            print(f"\nPelanggan '{nama_pelanggan}' bermain di {tipe_ps}.")
            print(f"Waktu mulai: {waktu_mulai.strftime('%H:%M:%S')}")

            def sisa_waktu():
                sekarang = time.time()
                return max(0, int(waktu_berakhir - sekarang))
        elif sistem_billing == '2':
            waktu_masuk = datetime.datetime.now()

            pelanggan_aktif[nama_pelanggan] = {
                "tipe_ps": tipe_ps,
                "tarif_per_jam": tarif_per_jam,
                "waktu_masuk": waktu_masuk
            }
            print(f"\nPelanggan '{nama_pelanggan}' bermain di {tipe_ps}.")
            print(f"Waktu masuk: {waktu_masuk.strftime('%H:%M:%S')}")

    elif pilihan == "2":
        if not pelanggan_aktif:
            print("\nTidak ada pelanggan yang aktif.")
            continue

        print("\nPelanggan yang aktif:")
        for i, nama in enumerate(pelanggan_aktif.keys(), start=1):
            print(f"{i}. {nama}")

        nama_pelanggan = input("Masukkan nama pelanggan yang selesai: ").upper()
        if nama_pelanggan not in pelanggan_aktif:
            print("Nama pelanggan tidak ditemukan.")
            continue

        data = pelanggan_aktif.pop(nama_pelanggan)
        waktu_keluar = datetime.datetime.now()
        durasi = waktu_keluar - data["waktu_masuk"]
        durasi_jam = durasi.total_seconds() / 3600
        biaya = round(durasi_jam * data["tarif_per_jam"])

        print(f"\nPelanggan               : {nama_pelanggan}")
        print(f"Tipe PlayStation        : {data['tipe_ps']}")
        print(f"Waktu masuk             : {data['waktu_masuk'].strftime('%H:%M:%S')}")
        print(f"Waktu keluar            : {waktu_keluar.strftime('%H:%M:%S')}")
        print(f"Durasi bermain          : {durasi_jam:.2f} jam")
        print(f"Biaya yang harus dibayar: Rp{biaya:,}")

        with open("laporan_harian.txt", "a") as file:
            file.write(f"{nama_pelanggan}, {data['tipe_ps']}, {data['waktu_masuk']}, {waktu_keluar}, {durasi_jam:.2f} jam, Rp{biaya:,}\n")
        print("Data transaksi telah disimpan.")

    elif pilihan == "3":
        print("\nTerima kasih telah menggunakan Sistem Billing PlayStation.")
        break

    else:
        print("Pilihan tidak valid, silakan pilih 1, 2, atau 3.")