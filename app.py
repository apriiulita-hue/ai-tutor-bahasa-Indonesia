import os
import re
import sqlite3
from collections import Counter
from datetime import datetime

import streamlit as st

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="AI Tutor Bahasa Indonesia",
    page_icon="📚",
    layout="wide",
)

st.markdown("""
<style>
h1 {
    font-size: 2.65rem !important;
    font-weight: 750 !important;
}

h2 {
    font-size: 1.9rem !important;
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab"] {
    font-size: 1.1rem !important;
    padding: 15px 18px !important;
    min-height: 58px !important;
}

.stButton button,
.stLinkButton a {
    min-height: 48px !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# KODE LAMA KAMU DILANJUTKAN DI SINI
JUDUL_BAB = "Mengenal Puisi yang Menginspirasikan Adanya Kesempatan untuk Semua"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

JUDUL_BAB = "Mengenal Puisi yang Menginspirasikan Adanya Kesempatan untuk Semua"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FOLDER_DATABASE = os.path.join(BASE_DIR, "database")
FILE_DATABASE_NILAI = os.path.join(BASE_DIR, "nilai_tutor.db")

TAUTAN_UNDANGAN_CLASSROOM = "https://classroom.google.com/c/ODkyODE1Mzc3OTEy?cjc=np2jitrm"
# ADMIN: ganti tautan di bawah dengan tautan video dan tugas yang sebenarnya.
KONFIGURASI_SUBBAB = {
    "Subbab 1 — Menemukan Tema dan Pesan dalam Cerpen": {
        "judul": "Menemukan Tema dan Pesan dalam Cerpen yang Menginspirasikan Penggubahan Puisi",
        "video_url": "https://youtu.be/8vyywfvqrp4?si=knWxi8Cm2F4wKwe4",  
        "tugas_url": "https://classroom.google.com/c/ODkyODE1Mzc3OTEy/a/ODkyODE1NjU4ODky/details",  
        "materi": """
### Tujuan pembelajaran
Peserta didik mampu menemukan tema dan pesan dalam cerpen serta memilih gagasan yang dapat dikembangkan menjadi puisi.

### Materi inti
- **Tema** adalah gagasan pokok yang mendasari cerita.
- **Pesan/amanat** adalah nilai atau pelajaran yang dapat dipetik pembaca dari cerita.
- Untuk menemukan tema dan pesan, perhatikan tokoh, konflik, tindakan tokoh, perubahan yang terjadi, dan akhir cerita.
- Gagasan dari cerpen dapat menjadi inspirasi puisi. Puisi tidak harus menceritakan ulang seluruh cerpen; penulis dapat berfokus pada perasaan, nilai, atau pesan yang paling berkesan.

### Langkah membaca cerpen
1. Baca cerpen secara utuh.
2. Catat tokoh dan konflik utama.
3. Temukan gagasan yang paling sering muncul atau paling menentukan cerita.
4. Simpulkan pesan berdasarkan peristiwa dan tindakan tokoh.
5. Pilih bagian atau pesan yang paling menginspirasi untuk dikembangkan menjadi puisi.

**Catatan:** tambahkan teks cerpen yang digunakan di kelas pada bagian ini atau pada file materi TXT di folder `database/`.
""",
        "tugas": "Baca cerpen yang ditentukan guru. Tuliskan tema, pesan, bukti dari peristiwa dalam cerpen, dan satu gagasan yang dapat dikembangkan menjadi puisi.",
    },
    "Subbab 2 — Mengenal Unsur-Unsur Puisi": {
        "judul": "Mengenal Unsur-Unsur Puisi",
        "video_url": "https://youtu.be/DIbB-67KUC4?si=eJ6ZHeOSJ2naP2oN",
        "tugas_url": "https://classroom.google.com/c/ODkyODE1Mzc3OTEy/a/ODkyODEyNTY0Njc3/details",
        "materi": """
### Tujuan pembelajaran
Peserta didik mampu mengenali unsur pembangun puisi dan menjelaskan fungsinya dalam menyampaikan gagasan atau perasaan.

### Materi inti
- **Diksi**: pilihan kata yang digunakan penyair.
- **Imaji/citraan**: kata atau ungkapan yang membangkitkan pengalaman indrawi pembaca.
- **Majas**: penggunaan bahasa kias untuk memberi efek atau makna tertentu.
- **Rima**: pengulangan bunyi yang dapat menciptakan musikalitas.
- **Irama**: alunan atau pergantian tekanan dan panjang-pendek bunyi ketika puisi dibaca.
- **Tipografi**: bentuk atau tata letak puisi pada halaman.
- **Tema dan amanat**: gagasan utama dan pesan yang disampaikan puisi.

Unsur yang tampak langsung pada bentuk dan bunyi puisi sering disebut unsur fisik, sedangkan gagasan, perasaan, tema, dan amanat berkaitan dengan unsur batin. Pengelompokan dan istilah dapat disesuaikan dengan buku ajar yang digunakan guru.

### Cara mengamati puisi
1. Baca puisi lebih dari sekali.
2. Tandai kata yang menarik atau memiliki makna kias.
3. Identifikasi gambaran indrawi dan pengulangan bunyi.
4. Simpulkan tema, suasana, dan pesan puisi.
""",
        "tugas": "Pilih puisi yang disediakan guru. Identifikasi sekurang-kurangnya tiga unsur puisi dan sertakan bukti berupa kata atau larik yang mendukung jawabanmu.",
    },
    "Subbab 3 — Menulis Puisi Berdasarkan Cerpen": {
        "judul": "Menulis Puisi Berdasarkan Cerpen",
        "video_url": "https://youtu.be/vL2y8EuOGl4?si=VnrVJjKTcd6sOYjN",
        "tugas_url": "https://classroom.google.com/c/ODkyODE1Mzc3OTEy/a/ODkyODE2OTY4MTE5/details",
        "materi": """
### Tujuan pembelajaran
Peserta didik mampu mengembangkan tema atau pesan dari cerpen menjadi puisi dengan pilihan kata dan ungkapan yang sesuai.

### Langkah menulis puisi
1. Pilih tema, peristiwa, tokoh, atau pesan dari cerpen yang paling berkesan.
2. Tentukan perasaan atau sudut pandang yang ingin disampaikan.
3. Buat daftar kata kunci dan gambaran indrawi.
4. Pilih diksi yang kuat dan sesuai dengan gagasan.
5. Susun kata menjadi larik dan bait; gunakan majas atau rima bila mendukung puisi.
6. Baca ulang, revisi kata yang kurang tepat, dan periksa apakah pesan utama masih terasa.

### Checklist revisi
- Apakah puisi terinspirasi dari cerpen yang dipilih?
- Apakah gagasan atau pesan dapat dipahami?
- Apakah pilihan katanya menarik dan sesuai?
- Apakah ada citraan atau ungkapan yang menghidupkan puisi?
- Apakah larik dan bait disusun dengan sengaja?
""",
        "tugas": "Tulislah puisi berdasarkan cerpen yang dipelajari. Beri judul, gunakan pilihan kata yang sesuai, lalu periksa kembali puisi sebelum dikumpulkan.",
    },
}

# Soal contoh awal. Silakan sesuaikan dengan buku ajar dan materi guru.
# Format setiap soal: pertanyaan, pilihan, indeks jawaban benar, pembahasan.
BANK_SOAL = {
    "Subbab 1 — Menemukan Tema dan Pesan dalam Cerpen": [
        ("Apa yang dimaksud dengan tema cerpen?", [
            "Gagasan pokok yang mendasari cerita",
            "Nama penerbit buku",
            "Daftar tokoh di akhir cerita",
            "Tempat cerita dicetak",
        ], 0, "Tema adalah gagasan pokok yang mendasari cerita."),
        ("Hal yang paling membantu pembaca menyimpulkan pesan cerpen adalah ...", [
            "Jumlah halaman saja",
            "Tindakan tokoh dan akibat yang terjadi",
            "Warna sampul buku",
            "Ukuran huruf",
        ], 1, "Tindakan tokoh, konflik, dan akibatnya dapat memberi petunjuk tentang pesan cerita."),
        ("Pesan atau amanat dalam cerpen berarti ...", [
            "Urutan paragraf",
            "Nama tokoh utama",
            "Pelajaran atau nilai yang dapat dipetik pembaca",
            "Tempat penjualan buku",
        ], 2, "Amanat merupakan pesan atau pelajaran yang dapat dipetik dari cerita."),
        ("Jika tokoh menolong temannya tanpa membedakan latar belakang, pesan yang mungkin muncul adalah ...", [
            "Kita harus selalu menang",
            "Persahabatan hanya untuk orang yang sama",
            "Pertolongan harus dibalas dengan hadiah",
            "Setiap orang layak mendapat pertolongan",
        ], 3, "Tindakan menolong tanpa membeda-bedakan dapat menyampaikan nilai kepedulian dan kesetaraan."),
        ("Bagian cerpen yang dapat menjadi inspirasi puisi adalah ...", [
            "Hanya nama pengarang",
            "Perasaan, peristiwa, atau pesan yang berkesan",
            "Nomor halaman saja",
            "Daftar isi buku saja",
        ], 1, "Puisi dapat dikembangkan dari perasaan, peristiwa, atau pesan yang paling berkesan."),
    ],
    "Subbab 2 — Mengenal Unsur-Unsur Puisi": [
        ("Pilihan kata yang digunakan penyair disebut ...", [
            "Diksi",
            "Alur",
            "Latar",
            "Sudut pandang",
        ], 0, "Diksi adalah pilihan kata dalam puisi."),
        ("Ungkapan 'angin berbisik di telingaku' menggunakan bahasa kias berupa ...", [
            "Data statistik",
            "Personifikasi",
            "Definisi",
            "Dialog langsung",
        ], 1, "Personifikasi memberi sifat atau tindakan manusia kepada benda atau gejala alam."),
        ("Kata-kata yang membuat pembaca seolah-olah melihat, mendengar, atau merasakan sesuatu disebut ...", [
            "Tipografi",
            "Amanat",
            "Imaji atau citraan",
            "Judul",
        ], 2, "Imaji/citraan membangkitkan pengalaman indrawi pembaca."),
        ("Pengulangan bunyi pada akhir larik puisi berkaitan dengan ...", [
            "Tokoh",
            "Latar",
            "Konflik",
            "Rima",
        ], 3, "Rima berkaitan dengan pengulangan atau persamaan bunyi."),
        ("Gagasan utama yang dibicarakan dalam puisi disebut ...", [
            "Tema",
            "Ukuran kertas",
            "Nama penerbit",
            "Jumlah bait",
        ], 0, "Tema adalah gagasan utama puisi."),
    ],
    "Subbab 3 — Menulis Puisi Berdasarkan Cerpen": [
        ("Langkah awal yang tepat sebelum menulis puisi berdasarkan cerpen adalah ...", [
            "Menyalin seluruh cerpen",
            "Memilih gagasan atau pesan cerpen yang ingin dikembangkan",
            "Menentukan warna kertas",
            "Menghapus tokoh dari cerita",
        ], 1, "Pilih gagasan, peristiwa, atau pesan yang paling berkesan sebagai titik awal puisi."),
        ("Setelah menentukan gagasan puisi, penulis sebaiknya ...", [
            "Langsung mengumpulkan tanpa membaca ulang",
            "Menghindari semua kata konkret",
            "Mengembangkan kata kunci dan memilih diksi",
            "Menyalin puisi orang lain",
        ], 2, "Kata kunci dan diksi membantu mengembangkan gagasan menjadi larik puisi."),
        ("Mengapa puisi berdasarkan cerpen tidak harus menceritakan ulang seluruh cerpen?", [
            "Karena puisi tidak boleh memiliki tema",
            "Karena puisi tidak boleh memiliki judul",
            "Karena cerpen selalu lebih pendek",
            "Karena puisi dapat berfokus pada satu perasaan, peristiwa, atau pesan",
        ], 3, "Puisi dapat menafsirkan satu bagian atau pesan cerpen secara kreatif."),
        ("Kegiatan membaca ulang dan memperbaiki pilihan kata disebut ...", [
            "Revisi",
            "Publikasi",
            "Penyalinan",
            "Pengarsipan",
        ], 0, "Revisi dilakukan untuk memperbaiki dan menyempurnakan karya."),
        ("Manakah tindakan yang menunjukkan puisi terinspirasi dari cerpen?", [
            "Menulis kata secara acak tanpa gagasan",
            "Mengembangkan pesan keberanian tokoh menjadi larik puisi",
            "Menyalin daftar isi",
            "Mengganti semua kata dengan angka",
        ], 1, "Mengembangkan pesan atau pengalaman tokoh menjadi larik puisi menunjukkan keterkaitan dengan cerpen."),
    ],
}

# =========================================================
# DATABASE NILAI (PERSISTEN DI FILE SQLITE)
# =========================================================
def siapkan_database_nilai():
    with sqlite3.connect(FILE_DATABASE_NILAI) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS hasil_tes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_peserta TEXT NOT NULL,
                subbab TEXT NOT NULL,
                jenis_tes TEXT NOT NULL,
                skor INTEGER NOT NULL,
                jumlah_soal INTEGER NOT NULL,
                waktu TEXT NOT NULL
            )
        """)

def simpan_hasil_tes(nama, subbab, jenis_tes, skor, jumlah_soal):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(FILE_DATABASE_NILAI) as conn:
        conn.execute(
            """INSERT INTO hasil_tes
            (nama_peserta, subbab, jenis_tes, skor, jumlah_soal, waktu)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (nama.strip(), subbab, jenis_tes, skor, jumlah_soal, waktu),
        )

def ambil_hasil_tes(nama):
    with sqlite3.connect(FILE_DATABASE_NILAI) as conn:
        rows = conn.execute(
            """SELECT subbab, jenis_tes, skor, jumlah_soal, waktu
            FROM hasil_tes WHERE nama_peserta = ?
            ORDER BY id DESC""",
            (nama.strip(),),
        ).fetchall()
    return rows

siapkan_database_nilai()

# =========================================================
# FUNGSI PENCARIAN TXT (DIPERTAHANKAN DARI KODE AWAL)
# =========================================================
def baca_database():
    data = []
    os.makedirs(FOLDER_DATABASE, exist_ok=True)
    for nama_file in os.listdir(FOLDER_DATABASE):
        if nama_file.lower().endswith(".txt"):
            lokasi_file = os.path.join(FOLDER_DATABASE, nama_file)
            try:
                with open(lokasi_file, "r", encoding="utf-8") as file:
                    data.append({"nama_file": nama_file, "isi": file.read()})
            except Exception as error:
                st.error(f"Gagal membaca {nama_file}: {error}")
    return data

def bersihkan_teks(teks):
    teks = teks.lower()
    teks = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks.strip()

STOPWORDS = {
    "yang", "dan", "di", "ke", "dari", "pada", "dengan", "untuk", "dalam",
    "adalah", "itu", "ini", "atau", "apa", "bagaimana", "mengapa", "sebutkan",
    "jelaskan", "jelaskanlah", "tentang", "suatu", "sebuah", "secara",
    "merupakan", "dapat", "akan", "sebagai", "oleh", "lebih", "juga",
    "tidak", "tersebut",
}

def ambil_kata_kunci(pertanyaan):
    teks = bersihkan_teks(pertanyaan)
    return [kata for kata in teks.split() if len(kata) > 2 and kata not in STOPWORDS]

def hitung_relevansi(pertanyaan, isi):
    kata_kunci = ambil_kata_kunci(pertanyaan)
    if not kata_kunci:
        return 0
    teks_database = bersihkan_teks(isi)
    frekuensi = Counter(teks_database.split())
    skor = sum(min(frekuensi[kata], 10) for kata in kata_kunci if kata in frekuensi)
    if bersihkan_teks(pertanyaan) in teks_database:
        skor += 20
    baris_awal = teks_database[:500]
    skor += sum(5 for kata in kata_kunci if kata in baris_awal)
    return skor

def cari_materi(pertanyaan, database):
    hasil = []
    for data in database:
        skor = hitung_relevansi(pertanyaan, data["isi"])
        if skor > 0:
            hasil.append({
                "nama_file": data["nama_file"],
                "isi": data["isi"],
                "skor": skor,
            })
    hasil.sort(key=lambda item: item["skor"], reverse=True)
    return hasil

def ambil_potongan_relevan(pertanyaan, isi, jumlah_maksimal=1200):
    kata_kunci = ambil_kata_kunci(pertanyaan)
    paragraf = re.split(r"\n\s*\n|\r\n", isi)
    paragraf_relevan = []
    for paragraf_item in paragraf:
        paragraf_bersih = bersihkan_teks(paragraf_item)
        skor = sum(1 for kata in kata_kunci if kata in paragraf_bersih)
        if skor > 0:
            paragraf_relevan.append((skor, paragraf_item.strip()))
    paragraf_relevan.sort(key=lambda item: item[0], reverse=True)
    hasil = ""
    for _, paragraf_item in paragraf_relevan:
        if len(hasil) + len(paragraf_item) <= jumlah_maksimal:
            hasil += paragraf_item + "\n\n"
    return hasil.strip() or isi[:jumlah_maksimal]

database_txt = baca_database()



# ==========================================
# PROFIL TIM PEMBUAT AI TUTOR
# ==========================================

ANGGOTA_TIM = [
    {
        "nama": "Apri Ulita",
        "foto": "foto_tim/anggota1.jpeg",
        "peran": "Pengembang Web Tutor AI",
        "prodi": "Pendidikan Bahasa dan Sastra Indonesia",
        "deskripsi": "Mengembangkan aplikasi AI Tutor Bahasa Indonesia."
    },
    {
        "nama": "Hadya Aminah Harahap",
        "foto": "foto_tim/anggota2.jpeg",
        "peran": "Penyusun Media Pembelajaran",
        "prodi": "Pendidikan Bahasa dan Sastra Indonesia",
        "deskripsi": "Menyusun dan mengembangkan media pembelajaran."
    },
    {
        "nama": "Enjelina Pitri Simamora",
        "foto": "foto_tim/anggota3.jpeg",
        "peran": "Penyusun Materi",
        "prodi": "Pendidikan Bahasa dan Sastra Indonesia",
        "deskripsi": "Menyusun materi pembelajaran Bahasa Indonesia."
    },
    {
        "nama": "Irma Yanti Sitorus",
        "foto": "foto_tim/anggota4.jpeg",
        "peran": "Perancang LKPD",
        "prodi": "Pendidikan Bahasa dan Sastra Indonesia",
        "deskripsi": "Merancang lembar kerja peserta didik."
    },
    {
        "nama": "Najla Haifa Tarigan",
        "foto": "foto_tim/anggota5.jpeg",
        "peran": "Perancang LKPD",
        "prodi": "Pendidikan Bahasa dan Sastra Indonesia",
        "deskripsi": "Mendukung penyusunan lembar kerja peserta didik."
    },
    {
        "nama": "Eylen Yossi Siagian",
        "foto": "foto_tim/anggota6.jpeg",
        "peran": "Perancang Alur Pembelajaran",
        "prodi": "Pendidikan Bahasa dan Sastra Indonesia",
        "deskripsi": "Merancang alur pembelajaran aplikasi."
    },
    {
        "nama": "Tia Hairani",
        "foto": "foto_tim/anggota7.jpeg",
        "peran": "Penyusun Soal Pre dan Post Tes",
        "prodi": "Pendidikan Bahasa dan Sastra Indonesia",
        "deskripsi": "Menyusun soal evaluasi pembelajaran."
    },
]


def tampilkan_profil_anggota(anggota, ringkas=False):
    lokasi_foto = os.path.join(
        BASE_DIR,
        anggota.get("foto", "")
    )

    if anggota.get("foto") and os.path.isfile(lokasi_foto):
        st.image(
            lokasi_foto,
            use_container_width=True
        )
    else:
        st.warning(
            f"Foto {anggota.get('nama', 'anggota')} belum ditemukan."
        )
        st.caption(f"Lokasi foto: {lokasi_foto}")

    st.markdown(
        f"**{anggota.get('nama', 'Nama belum diisi')}**"
    )
    st.caption(
        anggota.get("peran", "Peran belum diisi")
    )

    if not ringkas:
        st.write(
            f"**Program studi:** "
            f"{anggota.get('prodi', 'Belum diisi')}"
        )
        st.write(
            anggota.get(
                "deskripsi",
                "Deskripsi belum tersedia."
            )
        )


def tampilkan_tim(ringkas=False):
    jumlah_kolom = 2 if ringkas else 3

    for awal in range(0, len(ANGGOTA_TIM), jumlah_kolom):
        kelompok = ANGGOTA_TIM[awal:awal + jumlah_kolom]
        kolom = st.columns(jumlah_kolom)

        for tempat, anggota in zip(kolom, kelompok):
            with tempat:
                with st.container(border=True):
                    tampilkan_profil_anggota(
                        anggota,
                        ringkas=ringkas
                    )

# =========================================================
# HEADER DAN SIDEBAR
# =========================================================
st.title("📚 AI Tutor Bahasa Indonesia")
st.caption("Ruang belajar interaktif berbasis Streamlit dan Knowledge Base TXT.")
st.info(f"**Bab:** {JUDUL_BAB}")

with st.expander("👥 Kenalan dengan Tim Pembuat AI Tutor"):
    st.write(
        "Kami adalah tim pengembang AI Tutor Bahasa Indonesia. "
        "Aplikasi ini dibuat untuk mendukung pembelajaran "
        "Bahasa Indonesia yang interaktif dan menyenangkan."
    )
    tampilkan_tim()

st.subheader("Bergabung dengan Kelas")
st.write("Klik tombol berikut untuk masuk ke kelas pembelajaran.")
st.link_button(
    "🎓 Gabung ke Google Classroom",
    TAUTAN_UNDANGAN_CLASSROOM,
    use_container_width=True
)

with st.sidebar:
    st.header("👩‍🎓 Identitas Peserta Didik")
    nama_peserta = st.text_input(
        "Nama peserta didik",
        key="nama_peserta",
        placeholder="Masukkan nama lengkap",
    )
    st.caption("Gunakan nama yang sama setiap kali belajar agar riwayat nilai dapat ditampilkan.")
    st.divider()
    st.header("📖 Knowledge Base")
    st.write(f"Folder database: `{FOLDER_DATABASE}/`")
    st.write(f"Jumlah file TXT: **{len(database_txt)}**")
    if database_txt:
        for item in database_txt:
            st.write("📄 " + os.path.splitext(item["nama_file"])[0].replace("_", " ").title())
    else:
        st.warning("Belum ada file TXT. Buat folder database dan masukkan materi berformat .txt.")
    st.divider()
    st.caption("Catatan: penyimpanan nilai menggunakan file SQLite lokal `nilai_tutor.db`.")

# =========================================================
# NAVIGASI SUBBAB
# =========================================================
st.subheader("🧭 Ruang Belajar")
pilihan_subbab = st.selectbox("Pilih subbab", list(KONFIGURASI_SUBBAB.keys()))
info_subbab = KONFIGURASI_SUBBAB[pilihan_subbab]
st.markdown(f"### {info_subbab['judul']}")

tab_pre, tab_materi, tab_post, tab_tugas = st.tabs([
    "📝 Pre-test",
    "📖 Materi & Tutor AI",
    "✅ Post-test",
    "📤 Pengumpulan Tugas",
])

def tampilkan_tes(jenis_tes, subbab):
    if not nama_peserta.strip():
        st.warning("Masukkan nama peserta didik pada panel sebelah kiri sebelum mengerjakan tes.")
        return

    soal = BANK_SOAL[subbab]
    hasil_key = f"hasil_{jenis_tes}_{subbab}"
    sudah_dikerjakan = st.session_state.get(hasil_key)
    if sudah_dikerjakan and sudah_dikerjakan.get("nama") != nama_peserta.strip():
        sudah_dikerjakan = None

    if sudah_dikerjakan:
        st.success(f"{jenis_tes.title()} sudah dikerjakan.")
        st.metric("Skor", f"{sudah_dikerjakan['skor']} / 100")
        st.write(f"Jawaban benar: **{sudah_dikerjakan['benar']} dari {len(soal)} soal**")
        with st.expander("Lihat pembahasan"):
            for nomor, detail in enumerate(sudah_dikerjakan["detail"], start=1):
                st.markdown(f"**Soal {nomor}: {'Benar' if detail['benar'] else 'Perlu dipelajari lagi'}**")
                st.write(detail["pertanyaan"])
                st.write(f"Jawaban kamu: {detail['jawaban_peserta']}")
                st.write(f"Jawaban benar: {detail['jawaban_benar']}")
                st.caption(detail["pembahasan"])
        if st.button(f"Ulangi {jenis_tes}", key=f"ulang_{jenis_tes}_{subbab}"):
            del st.session_state[hasil_key]
            st.rerun()
        return

    st.write(
        "Jawab semua pertanyaan berikut. Skor akan dihitung otomatis setelah kamu menekan tombol **Kirim Jawaban**."
    )
    with st.form(key=f"form_{jenis_tes}_{subbab}"):
        jawaban_dipilih = []
        for nomor, item_soal in enumerate(soal, start=1):
            pertanyaan_soal, pilihan, _, _ = item_soal
            jawaban = st.radio(
                f"{nomor}. {pertanyaan_soal}",
                pilihan,
                index=None,
                key=f"{jenis_tes}_{subbab}_{nomor}",
            )
            jawaban_dipilih.append(jawaban)
        dikirim = st.form_submit_button("Kirim Jawaban", use_container_width=True)

    if dikirim:
        if any(jawaban is None for jawaban in jawaban_dipilih):
            st.warning("Silakan jawab semua soal terlebih dahulu.")
            return

        benar = 0
        detail_hasil = []
        for item_soal, jawaban_peserta in zip(soal, jawaban_dipilih):
            pertanyaan_soal, pilihan, indeks_benar, pembahasan = item_soal
            jawaban_benar = pilihan[indeks_benar]
            tepat = jawaban_peserta == jawaban_benar
            benar += int(tepat)
            detail_hasil.append({
                "pertanyaan": pertanyaan_soal,
                "jawaban_peserta": jawaban_peserta,
                "jawaban_benar": jawaban_benar,
                "benar": tepat,
                "pembahasan": pembahasan,
            })

        skor = round((benar / len(soal)) * 100)
        hasil = {
            "nama": nama_peserta.strip(),
            "skor": skor,
            "benar": benar,
            "detail": detail_hasil,
        }
        st.session_state[hasil_key] = hasil
        simpan_hasil_tes(nama_peserta, subbab, jenis_tes, skor, len(soal))
        st.rerun()

with tab_pre:
    st.subheader(f"Pre-test — {pilihan_subbab.split('—')[0].strip()}")
    st.write("Tes awal untuk mengetahui pemahaman sebelum mempelajari subbab ini.")
    tampilkan_tes("pre-test", pilihan_subbab)

with tab_materi:
    st.subheader("Tujuan dan Materi Pembelajaran")
    st.markdown(info_subbab["materi"])

    if info_subbab["video_url"].strip():
        st.link_button("▶️ Buka Video Pembelajaran", info_subbab["video_url"])
    else:
        st.info("Tautan video belum diisi. Admin dapat mengisinya pada `KONFIGURASI_SUBBAB` di kode Python.")

    st.divider()
    st.subheader("💬 Tanya Tutor Materi")
    st.caption("Tutor ini mencari jawaban dari file TXT di folder database; bukan chatbot generatif. Tambahkan materi yang relevan ke database TXT agar pencarian lebih akurat.")
    pertanyaan_tutor = st.text_area(
        "Apa yang ingin kamu tanyakan?",
        key=f"pertanyaan_tutor_{pilihan_subbab}",
        placeholder="Contoh: Bagaimana cara menemukan pesan dalam cerpen?",
        height=100,
    )
    if st.button("🔍 Cari jawaban di materi", key=f"tanya_{pilihan_subbab}", use_container_width=True):
        if not pertanyaan_tutor.strip():
            st.warning("Tuliskan pertanyaan terlebih dahulu.")
        elif not database_txt:
            st.warning("Database TXT belum tersedia. Tambahkan file materi ke folder database/.")
        else:
            hasil_cari = cari_materi(pertanyaan_tutor, database_txt)
            if hasil_cari:
                utama = hasil_cari[0]
                st.success(f"Sumber paling relevan: {utama['nama_file']}")
                st.write(ambil_potongan_relevan(pertanyaan_tutor, utama["isi"]))
                if len(hasil_cari) > 1:
                    with st.expander("Lihat sumber materi terkait"):
                        for item in hasil_cari[1:4]:
                            st.markdown(f"**{item['nama_file']}**")
                            st.write(ambil_potongan_relevan(pertanyaan_tutor, item["isi"], 700))
            else:
                st.warning("Materi yang sesuai belum ditemukan. Coba gunakan kata kunci yang lebih spesifik.")

with tab_post:
    st.subheader(f"Post-test — {pilihan_subbab.split('—')[0].strip()}")
    st.write("Tes akhir untuk memeriksa pemahaman setelah mempelajari subbab.")
    tampilkan_tes("post-test", pilihan_subbab)

with tab_tugas:
    st.subheader("📤 Pengumpulan Tugas")
    st.write(info_subbab["tugas"])
    st.warning(
        "Setelah membuka Google Classroom, pastikan kamu menekan tombol **Serahkan/Turn in** pada tugas yang benar."
    )
    if info_subbab["tugas_url"].strip():
        st.link_button("Buka Tugas di Google Classroom", info_subbab["tugas_url"], use_container_width=True)
    else:
        st.info("Tautan tugas belum diisi. Tempel tautan tugas khusus Google Classroom pada `tugas_url` untuk subbab ini.")

# =========================================================
# RIWAYAT NILAI PESERTA DIDIK
# =========================================================
st.divider()
with st.expander("📊 Riwayat Nilai Saya"):
    if not nama_peserta.strip():
        st.info("Masukkan nama pada panel sebelah kiri untuk melihat riwayat nilai.")
    else:
        riwayat = ambil_hasil_tes(nama_peserta)
        if riwayat:
            st.dataframe(
                [
                    {
                        "Subbab": row[0],
                        "Jenis tes": row[1].title(),
                        "Skor": row[2],
                        "Jumlah soal": row[3],
                        "Waktu": row[4],
                    }
                    for row in riwayat
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Belum ada hasil tes yang tersimpan untuk nama ini.")

st.divider()
st.caption(
    "AI Tutor Bahasa Indonesia | Streamlit + database TXT + SQLite. "
    "Tautan video dan Google Classroom harus diisi oleh admin sebelum digunakan."
)
