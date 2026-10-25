from fastapi import APIRouter, Depends

from ..deps import Pengguna, butuh_peran, kelas_efektif
from ._stub import belum_dibuat

# Baca: guru dan siswa. Siswa hanya menerima materi kelasnya (kelas_efektif mengabaikan ?kelas=).
baca = APIRouter(prefix="/materi", tags=["materi"], dependencies=[Depends(butuh_peran("guru", "siswa"))])
# Tulis: guru saja. Dikunci di level router, jadi endpoint baru di sini otomatis terlindungi.
tulis = APIRouter(prefix="/materi", tags=["materi"], dependencies=[Depends(butuh_peran("guru"))])


@baca.get("")
def daftar(kelas: str | None = None, p: Pengguna = Depends(butuh_peran("guru", "siswa"))):
    kelas_dipakai = kelas_efektif(p, kelas)  # noqa: F841  -> pakai ini di query, BUKAN `kelas`
    belum_dibuat()


@baca.get("/{materi_id}")
def satu(materi_id: int, p: Pengguna = Depends(butuh_peran("guru", "siswa"))):
    # Siswa: pastikan materi memang untuk kelasnya (kalau tidak, 404 -- bukan 403).
    belum_dibuat()


@tulis.post("")
def tambah():
    belum_dibuat()


@tulis.put("/{materi_id}")
def ubah(materi_id: int):
    belum_dibuat()


@tulis.delete("/{materi_id}")
def hapus(materi_id: int):
    belum_dibuat()


@tulis.post("/unggah")
def unggah():
    """multipart `file` (.pdf/.docx/.txt). Batasi ukuran, cek tipe dari ISI file, batasi hasil ekstraksi."""
    belum_dibuat()
