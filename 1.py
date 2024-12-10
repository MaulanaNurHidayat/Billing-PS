import time
import threading
import subprocess

TARIF_PS = {
    "PS3": 5000,
    "PS4": 8000,
    "PS5": 10000
}

print("Sistem Billing PlayStation\n")
print("Pilih tipe PlayStation:")
for tipe, tarif in TARIF_PS.items():
    print(f"- {tipe} (Rp{tarif:,}/jam)")

while True:
    tipe_ps = input("\nMasukkan tipe PlayStation (PS3/PS4/PS5): ").upper()
    if tipe_ps in TARIF_PS:
        break
    print("Tipe PlayStation tidak valid, silakan pilih PS3, PS4, atau PS5.")

tarif_per_jam = TARIF_PS[tipe_ps]

# Input data pelanggan
nama_pelanggan = input("Masukkan nama pelanggan: ")
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

def sisa_waktu():
    sekarang = time.time()
    return max(0, int(waktu_berakhir - sekarang))

# Thread untuk hitung mundur dan mematikan TV
def countdown_thread():
    while True:
        sekarang = time.time()
        if sekarang >= waktu_berakhir:
            print(f"\nWaktu bermain untuk {nama_pelanggan} habis!")
            try:
                subprocess.run(["echo", "standby 0", "|", "cec-client", "-s"], check=True)
                print("TV berhasil dimatikan.")
            except Exception as e:
                print(f"Terjadi kesalahan saat mematikan TV: {e}")
            break
        time.sleep(1)

# Jalankan countdown di thread terpisah
thread = threading.Thread(target=countdown_thread)
thread.start()

print("\nHitung mundur dimulai. Nikmati permainan Anda!")

# Opsi untuk menampilkan waktu sisa
while True:
    print("\nPilihan:")
    print("1. Lihat waktu sisa")
    print("2. Keluar")

    pilihan = input("Pilih opsi (1/2): ")
    if pilihan == "1":
        sisa = sisa_waktu()
        jam, sisa_detik = divmod(sisa, 3600)
        menit, detik = divmod(sisa_detik, 60)
        print(f"Waktu tersisa: {jam:02d}:{menit:02d}:{detik:02d}")
    elif pilihan == "2":
        print("\nTerima kasih telah menggunakan Sistem Billing PlayStation.")
        break
    else:
        print("Pilihan tidak valid, silakan pilih 1 atau 2.")