import time
import datetime
import threading

TARIF_PS = {
    "PS2": 3000,
    "PS3": 5000,
    "PS4": 8000,
    "PS5": 10000
}
pelanggan_aktif = {}
print("Sistem Billing PlayStation\n")


# Fungsi untuk memeriksa waktu bermain pelanggan
def monitor_waktu():
    while True:
        waktu_sekarang = time.time()
        for nama, data in list(pelanggan_aktif.items()):
            if data["waktu_berakhir"] is not None and waktu_sekarang > data["waktu_berakhir"]:
                print(f"\n[NOTIFIKASI] Waktu bermain pelanggan '{nama}' telah habis!")
                pelanggan_aktif[nama]["waktu_berakhir"] = None  # Tandai waktu habis
        time.sleep(5)  # Interval pengecekan


# Jalankan thread untuk memonitor waktu
threading.Thread(target=monitor_waktu, daemon=True).start()

while True:
    print("\nPilihan:")
    print("1. Tambah pelanggan baru")
    print("2. Lihat sisa waktu pelanggan")
    print("3. Selesaikan transaksi pelanggan")
    print("4. Keluar")
    
    pilihan = input("Pilih opsi (1/2/3/4): ")

    if pilihan == "1":
        print("\nPilih tipe PlayStation:")
        for tipe, tarif in TARIF_PS.items():
            print(f"- {tipe} (Rp{tarif:,}/jam)")

        while True:
            tipe_ps = input("Masukkan tipe PlayStation (PS2/PS3/PS4/PS5): ").upper()
            if tipe_ps in TARIF_PS:
                break
            print("Tipe PlayStation tidak valid, silakan pilih PS2, PS3, PS4, atau PS5.")

        tarif_per_jam = TARIF_PS[tipe_ps]

        nama_pelanggan = input("Nama pelanggan: ").upper()
        print("Sistem Billing: ")
        print("1. Main per jam")
        print("2. Unlimited waktu")
        sistem_billing = input("Masukkan sistem billing: ")

        waktu_masuk = datetime.datetime.now()

        if sistem_billing == '1':
            durasi_jam = float(input("Durasi bermain (jam): "))
            durasi_detik = int(durasi_jam * 3600)

            # Hitung biaya
            biaya = round(durasi_jam * tarif_per_jam)
            print(f"\nPelanggan       : {nama_pelanggan}")
            print(f"Tipe PlayStation: {tipe_ps}")
            print(f"Durasi bermain  : {durasi_jam} jam")
            print(f"Biaya           : Rp{biaya:,}")

            # Set waktu berakhir
            waktu_berakhir = time.time() + durasi_detik

            pelanggan_aktif[nama_pelanggan] = {
                "tipe_ps": tipe_ps,
                "tarif_per_jam": tarif_per_jam,
                "waktu_masuk": waktu_masuk,
                "waktu_berakhir": waktu_berakhir,
                "sistem_billing": "Per Jam"
            }

            print(f"\nPelanggan '{nama_pelanggan}' bermain di {tipe_ps}.")
            print(f"Waktu mulai: {waktu_masuk.strftime('%H:%M:%S')}")

        elif sistem_billing == '2':
            pelanggan_aktif[nama_pelanggan] = {
                "tipe_ps": tipe_ps,
                "tarif_per_jam": tarif_per_jam,
                "waktu_masuk": waktu_masuk,
                "waktu_berakhir": None,
                "sistem_billing": "Unlimited"
            }
            print(f"\nPelanggan '{nama_pelanggan}' bermain di {tipe_ps}.")
            print(f"Waktu masuk: {waktu_masuk.strftime('%H:%M:%S')}")

    elif pilihan == "2":
        if not pelanggan_aktif:
            print("\nTidak ada pelanggan yang aktif.")
            continue

        print("\nPelanggan yang aktif:")
        for nama, data in pelanggan_aktif.items():
            if data["waktu_berakhir"] is None:
                print(f"- {nama} (Unlimited)")
            else:
                waktu_sisa = max(0, int(data["waktu_berakhir"] - time.time()))
                if waktu_sisa > 0:
                    jam, sisa_detik = divmod(waktu_sisa, 3600)
                    menit, detik = divmod(sisa_detik, 60)
                    print(f"- {nama} (Sisa waktu: {jam} jam {menit} menit {detik} detik)")
                else:
                    print(f"- {nama} (Waktu habis!)")

    elif pilihan == "3":
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
        durasi_total_detik = int(durasi.total_seconds())
        durasi_jam, durasi_sisa_detik = divmod(durasi_total_detik, 3600)
        durasi_menit, _ = divmod(durasi_sisa_detik, 60)

        # Hitung biaya
        if data["sistem_billing"] == "Per Jam":
            biaya = round((durasi_jam + durasi_menit / 60) * data["tarif_per_jam"])
        else:
            biaya = "Rp0 (Unlimited)"

        print(f"\nPelanggan               : {nama_pelanggan}")
        print(f"Tipe PlayStation        : {data['tipe_ps']}")
        print(f"Waktu masuk             : {data['waktu_masuk'].strftime('%H:%M:%S')}")
        print(f"Waktu keluar            : {waktu_keluar.strftime('%H:%M:%S')}")
        print(f"Durasi bermain          : {durasi_jam} jam {durasi_menit} menit")
        print(f"Biaya yang harus dibayar: {biaya}")

        # Output ke file laporan_harian.txt
        with open("laporan_harian.txt", "a") as file:
            file.write(
                f"Pelanggan               : {nama_pelanggan}\n"
                f"Tipe PlayStation        : {data['tipe_ps']}\n"
                f"Waktu masuk             : {data['waktu_masuk'].strftime('%H:%M:%S')}\n"
                f"Waktu keluar            : {waktu_keluar.strftime('%H:%M:%S')}\n"
                f"Durasi bermain          : {durasi_jam} jam {durasi_menit} menit\n"
                f"Biaya yang harus dibayar: {biaya}\n"
                f"{'-'*50}\n"
            )
        print("Data transaksi telah disimpan.")

    elif pilihan == "4":
        print("\nTerima kasih telah menggunakan Sistem Billing PlayStation.")
        break

    else:
        print("Pilihan tidak valid, silakan pilih 1, 2, 3, atau 4.")