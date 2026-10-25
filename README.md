# Bemai — Chatbot Pembelajaran SMP Muhammadiyah

Asisten belajar berbasis materi sekolah. Guru mengisi materi, siswa bertanya dan berlatih,
hasilnya terbaca guru. Prototipe untuk PKM.

## Struktur

```
aplikasi-pkm/
  docker-compose.yml          produksi: api + web (database di Supabase)
  docker-compose.dev.yml      lokal: Postgres + api (auto-reload) + web
  backend/                    FastAPI (lihat backend/app dan tests)
  db/                         skema SQL, seed, retensi, role aplikasi
  frontend/
    index.html                halaman (markup saja)
    assets/logo-muhammadiyah.svg
    src/styles/
      dasar.css               variabel warna, tipe teks, tombol, kartu, form
      tata-letak.css          rangka aplikasi: sidebar, topbar, grid, halaman login
      halaman.css             gaya tiap halaman: chat, kuis, nilai, analisis, modal
    src/js/
      konstanta.js            nama aplikasi, daftar tingkat & rombel, kunci penyimpanan
      data-contoh.js          data awal (5 materi IPA/Matematika/B.Indonesia + 9 soal)
      util.js                 pemilih elemen, escaping teks, format tanggal
      status.js               penyimpanan lokal, migrasi data, retensi 24 jam
      seleksi.js              query data: materi per kelas, soal per kelas, hasil per kelas
      ui.js                   navigasi halaman, modal, notifikasi
      siswa/
        chat.js               tanya jawab dengan chatbot
        materi.js             daftar materi kelas + tombol tanya ke chatbot
        latihan.js            pilih materi, kerjakan soal, nilai
        rangkuman.js          rangkuman otomatis dari materi
        riwayat.js            riwayat latihan & pertanyaan siswa
      guru/
        dashboard.js          kartu ringkas + aktivitas terbaru
        materi.js             kelola materi
        soal.js               kelola soal + generate soal dari materi
        upload.js             unggah dokumen (tempel teks)
        analisis.js           analisis hasil belajar, catatan teknis, reset data
      api.js                  pemanggil /api (belum dipakai modul lain)
      main.js                 pemetaan aksi tombol + titik masuk aplikasi
  docs/api.md                 kontrak API antara front-end dan back-end
  docs/deploy.md              langkah Supabase + server
  mocks/data-contoh.json      sumber seed (db/seed.sql dibuat darinya)
```

## Menjalankan

Pengembangan lokal (butuh Docker; frontend dan backend langsung terbaca dari disk):

```
docker compose -f docker-compose.dev.yml up --build
```

Buka http://127.0.0.1:8081 (Swagger di /api/docs). Database lokal berisi skema dan seed;
buat akun guru dengan `docker compose -f docker-compose.dev.yml exec api python -m app.cli buat-guru --email ... --nama ...`.
Frontend saja tanpa backend masih bisa dibuka dengan `cd frontend && python3 -m http.server 8899`
(masih memakai data lokal browser sampai `status.js` disambungkan ke `api.js`).

Tes backend (Postgres sungguhan, bukan mock):

```
cd backend && pip install -r requirements-dev.txt
TEST_DATABASE_URL=postgresql://bemai_app:dev-sandi-lokal@127.0.0.1:55432/bemai pytest
```

Deploy: lihat `docs/deploy.md`.

## Pembagian kerja

Front-end memegang semua yang dilihat dan disentuh pengguna: markup, gaya, alur halaman,
state tampilan, serta seluruh panggilan data. Back-end (FastAPI) memegang akun, hak akses per peran,
penilaian, analisis, dan pemanggilan model AI. Database: Postgres di Supabase, diakses HANYA oleh backend.

Semua komunikasi lewat `docs/api.md`. Bentuk JSON tidak diubah sepihak.

## Konvensi

- Berkas gaya: satu berkas satu lapisan (dasar, tata letak, halaman)
- Berkas JS: satu berkas satu tanggung jawab, impor eksplisit antar berkas
- State global hanya di `status.js`, diakses sebagai `status.db`, `status.kelasSiswa`
- Kelas selalu ditulis lengkap: `"VIII C"` (tingkat + rombel), bukan `"VIII"`
- Data analisis (hasil latihan, aktivitas, chat) otomatis dibuang setelah 24 jam

## Kondisi sekarang

Sudah jalan: login dua peran, chat menjawab dari materi kelas siswa, latihan + penilaian,
rangkuman, riwayat, dashboard guru, kelola materi, kelola soal, unggah dokumen (tempel teks),
analisis per tingkat dan per rombel, serta pembersihan data analisis 24 jam.

Belum tersambung: model bahasa (jawaban chat masih pencarian kata kunci di materi),
database, akun asli, dan ekstraksi PDF/DOCX. Ketiganya bergantung pada back-end.

## Pembahasan, latihan ulang, dan edit

- Setelah mengumpulkan latihan, siswa melihat jawaban sendiri, kunci, dan pembahasan guru.
  Soal lama tanpa pembahasan menampilkan kutipan materi yang memuat jawaban benar jika tersedia;
  jika tidak, aplikasi memberi tahu bahwa penjelasan belum ditambahkan.
- Tombol **Coba lagi** hanya mengulang soal salah atau belum dijawab. Setiap percobaan
  disimpan terpisah, ikut dihitung dalam dashboard, dan tetap mengikuti retensi 24 jam.
  Hasil ulang memiliki `ulangDari` yang menunjuk ID percobaan sebelumnya.
- Guru dapat memilih **Edit** pada daftar materi dan bank soal. Perubahan mempertahankan ID,
  hubungan materi–soal, dan nilai terdahulu. Pembatalan tidak menyimpan perubahan.
- Editor materi mencakup judul, mata pelajaran, tingkat, rombel, isi, dan rangkuman.
  Kelas tujuan soal terkait tidak otomatis berubah; periksa lewat editor soal.
- Editor soal mencakup materi sumber, pertanyaan, pilihan, kunci, kelas tujuan, dan
  `pembahasan` opsional. Pembahasan juga tersedia saat menambahkan soal manual;
  soal definisi otomatis menyimpan penjelasan dari materi sumber.

Pemeriksaan browser: jalankan server lokal terlebih dulu, lalu gunakan Node dan Playwright
(dengan Chromium terpasang) untuk menjalankan `node tests/rendering.cjs` dan
`node tests/learning.cjs`. Pengujian memakai penyimpanan browser terpisah dari data demo pengguna.

## Keamanan dan peran (RBAC)

- Dua pintu login terpisah (`/auth/login/guru`, `/auth/login/siswa`); peran dibaca server dari akun.
- Semua penjaga ada di `backend/app/deps.py`. Router guru dikunci di level router (`butuh_peran("guru")`),
  jadi endpoint baru otomatis terlindungi. Kelas siswa selalu dari akun, bukan dari `?kelas=`.
- `backend/tests/test_auth_dan_rbac.py` memuat matriks akses; jalankan setiap menambah endpoint.
- Kunci jawaban ada di tabel `soal_kunci`, terpisah dari soal. Role database `bemai_app` tidak bisa
  membuat tabel dan tidak bisa mengubah/menghapus `log_audit`.

## Status backend

Sudah jadi dan teruji: skema + RLS + retensi, login/logout/ganti sandi, sesi, penjaga peran, CSRF, CLI buat guru.
Masih kerangka (501): materi, soal, latihan, chat, analisis, siswa — isi di `backend/app/routers/`.
