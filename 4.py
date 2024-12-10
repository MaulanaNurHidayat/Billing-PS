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
member_data = {}  # Format: {nama_member: jumlah_kunjungan}
billing_status = {i: "Kosong" for i in range(1, 11)}  # Billing dari 1 hingga 10
laporan_harian = []  # List untuk menyimpan laporan harian

print("Sistem Billing PlayStation\n")

while True:
    # Monitor waktu pelanggan
    waktu_sekarang = time.time()
    for nama, data in list(pelanggan_aktif.items()):
        if data["waktu_berakhir"] is not None and waktu_sekarang > data["waktu_berakhir"]:
            print(f"\n[NOTIFIKASI] Waktu bermain pelanggan '{nama}' telah habis!")
            pelanggan_aktif[nama]["waktu_berakhir"] = None  # Tandai waktu habis

    print("\nPilihan:")
    print("1. Tambah pelanggan baru")
    print("2. Lihat sisa waktu pelanggan")
    print("3. Selesaikan transaksi pelanggan")
    print("4. Lihat status billing")
    print("5. Lihat laporan harian")
    print("6. Keluar")

    pilihan = input("Pilih opsi (1/2/3/4/5/6): ")

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
        if nama_pelanggan in member_data:
            member_data[nama_pelanggan] += 1
        else:
            member_data[nama_pelanggan] = 1

        is_gratis = False
        if member_data[nama_pelanggan] == 3:
            is_gratis = True
            print(f"[INFO] Pelanggan '{nama_pelanggan}' adalah member setia! Gratis 1 jam bermain!")

        print("Sistem Billing: ")
        print("1. Main per jam")
        print("2. Unlimited waktu")
        sistem_billing = input("Masukkan sistem billing: ")

        # Pilih billing yang kosong
        print("\nPilih billing yang kosong:")
        for nomor, status in billing_status.items():
            if status == "Kosong":
                print(f"- Billing {nomor} (Kosong)")

        while True:
            nomor_billing = int(input("Masukkan nomor billing: "))
            if nomor_billing in billing_status and billing_status[nomor_billing] == "Kosong":
                billing_status[nomor_billing] = "Terpakai"
                break
            print("Nomor billing tidak valid atau sudah terpakai.")

        waktu_masuk = datetime.datetime.now()

        if sistem_billing == '1':
            durasi_jam = float(input("Durasi bermain (jam): "))
            if is_gratis:
                durasi_jam += 1

            durasi_detik = int(durasi_jam * 3600)
            biaya = durasi_jam * tarif_per_jam
            if durasi_jam > 3:
                biaya *= 0.5
                print("[INFO] Diskon 50% untuk durasi lebih dari 3 jam!")
            biaya = round(biaya)

            waktu_berakhir = time.time() + durasi_detik

            pelanggan_aktif[nama_pelanggan] = {
                "tipe_ps": tipe_ps,
                "tarif_per_jam": tarif_per_jam,
                "waktu_masuk": waktu_masuk,
                "waktu_berakhir": waktu_berakhir,
                "sistem_billing": "Per Jam",
                "nomor_billing": nomor_billing
            }

        elif sistem_billing == '2':
            pelanggan_aktif[nama_pelanggan] = {
                "tipe_ps": tipe_ps,
                "tarif_per_jam": tarif_per_jam,
                "waktu_masuk": waktu_masuk,
                "waktu_berakhir": None,
                "sistem_billing": "Unlimited",
                "nomor_billing": nomor_billing
            }

        print(f"Pelanggan '{nama_pelanggan}' bermain di {tipe_ps}. Nomor billing: {nomor_billing}")

    elif pilihan == "2":
        if not pelanggan_aktif:
            print("\nTidak ada pelanggan yang aktif.")
            continue

        print("\nPelanggan yang aktif:")
        for nama, data in pelanggan_aktif.items():
            waktu_sisa = None
            if data["waktu_berakhir"] is not None:
                waktu_sisa = max(0, int(data["waktu_berakhir"] - time.time()))

            if waktu_sisa is None:
                print(f"- {nama} (Unlimited)")
            else:
                jam, sisa_detik = divmod(waktu_sisa, 3600)
                menit, detik = divmod(sisa_detik, 60)
                print(f"- {nama} (Sisa waktu: {jam} jam {menit} menit {detik} detik)")

    elif pilihan == "3":
        if not pelanggan_aktif:
            print("\nTidak ada pelanggan yang aktif.")
            continue

        print("\nPelanggan yang aktif:")
        for nama in pelanggan_aktif.keys():
            print(f"- {nama}")

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

        if data["sistem_billing"] == "Unlimited":
            biaya = f"Unlimited (Rp{data['tarif_per_jam']:,}/jam)"
        else:
            biaya = (durasi_total_detik / 3600) * data['tarif_per_jam']
            biaya = round(biaya)

        # Update laporan harian
        laporan_harian.append({
            "nama": nama_pelanggan,
            "status_member": f"Member ({member_data[nama_pelanggan]} kali)" if nama_pelanggan in member_data else "Pelanggan Baru",
            "waktu_masuk": data["waktu_masuk"],
            "waktu_keluar": waktu_keluar,
            "durasi": f"{durasi_jam} jam {durasi_menit} menit",
            "sistem_billing": data["sistem_billing"],
            "biaya_total": biaya
        })

        billing_status[data["nomor_billing"]] = "Kosong"

        print(f"\nNomor Billing   : {data['nomor_billing']}")
        print(f"Pelanggan       : {nama_pelanggan}")
        print(f"Tipe PlayStation: {data['tipe_ps']}")
        print(f"Waktu masuk     : {data['waktu_masuk'].strftime('%H:%M:%S')}")
        print(f"Waktu keluar    : {waktu_keluar.strftime('%H:%M:%S')}")
        print(f"Durasi bermain  : {durasi_jam} jam {durasi_menit} menit")
        print(f"Biaya           : Rp{biaya:,}")

    elif pilihan == "4":
        print("\nStatus Billing:")
        for nomor, status in billing_status.items():
            print(f"Billing {nomor}: {status}")

    elif pilihan == "5":
        print("\nLaporan Harian:")
        for laporan in laporan_harian:
            print("\n---")
            for key, value in laporan.items():
                print(f"{key.capitalize():<15}: {value}")

    elif pilihan == "6":
        print("\nTerima kasih telah menggunakan Sistem Billing PlayStation.")
        break

    else:
        print("Pilihan tidak valid, silakan pilih 1, 2, 3, 4, atau 5.")