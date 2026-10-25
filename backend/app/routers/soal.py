from fastapi import APIRouter, Depends

from ..deps import Pengguna, butuh_peran, kelas_efektif
from ._stub import belum_dibuat

baca = APIRouter(prefix="/soal", tags=["soal"], dependencies=[Depends(butuh_peran("guru", "siswa"))])
tulis = APIRouter(prefix="/soal", tags=["soal"], dependencies=[Depends(butuh_peran("guru"))])


@baca.get("")
def daftar(kelas: str | None = None, p: Pengguna = Depends(butuh_peran("guru", "siswa"))):
    """JANGAN pernah menyertakan soal_kunci.jawaban di respons untuk siswa."""
    kelas_dipakai = kelas_efektif(p, kelas)  # noqa: F841
    belum_dibuat()


@tulis.post("")
def tambah():
    belum_dibuat()


@tulis.put("/{soal_id}")
def ubah(soal_id: int):
    """Tidak ada di api.md versi lama, tapi guru bisa mengedit soal di frontend."""
    belum_dibuat()


@tulis.delete("/{soal_id}")
def hapus(soal_id: int):
    belum_dibuat()


@tulis.post("/generate")
def generate():
    belum_dibuat()


@tulis.post("/terbitkan")
def terbitkan():
    belum_dibuat()
