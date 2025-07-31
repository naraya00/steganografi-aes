from aes_enkripsi import encrypt_AES, decrypt_AES
from lsb_steganografi import encode_LSB, decode_LSB

# Input pesan dan password
pesan_rahasia = "Ini pesan rahasia dari lisaaa"
password = "kunciku123"

# 1. Enkripsi → hasil base64
pesan_terenkripsi_base64 = encrypt_AES(pesan_rahasia, password)

# 2. Ubah ke HEX string agar aman untuk disisipkan
pesan_hex = pesan_terenkripsi_base64.encode('utf-8').hex()

# 3. Tambahkan marker agar saat decode bisa dikenali
pesan_dengan_marker = "<<start>>" + pesan_hex + "<<end>>"

# 4. Encode ke gambar PNG
encode_LSB("media/gambar_asli.png", pesan_dengan_marker, "media/hasil_encode.png")
print("✅ Pesan telah disisipkan ke gambar")

# 5. Decode dari gambar hasil
hasil_decode = decode_LSB("media/hasil_encode.png")

# 6. Ambil isi di antara marker
try:
    isi_hex = hasil_decode.split("<<start>>")[1].split("<<end>>")[0]

    # 7. Konversi kembali dari hex → base64 string
    hasil_decode_base64 = bytes.fromhex(isi_hex).decode('utf-8')

    # 8. Dekripsi
    pesan_asli = decrypt_AES(hasil_decode_base64, password)
    print("📤 Pesan berhasil didekripsi:", pesan_asli)

except Exception as e:
    print("❌ Gagal mendekripsi pesan:", e)
