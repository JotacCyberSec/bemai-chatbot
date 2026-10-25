from fastapi import APIRouter, Depends

from ..deps import butuh_peran
from ._stub import belum_dibuat

# Hanya siswa. Konteks diambil dari materi KELAS SISWA (dari akun, bukan dari body).
# Tambahkan batas jumlah pertanyaan per siswa per menit sebelum memanggil model AI.
router = APIRouter(tags=["chat"], dependencies=[Depends(butuh_peran("siswa"))])


@router.post("/chat")
def tanya():
    belum_dibuat()
