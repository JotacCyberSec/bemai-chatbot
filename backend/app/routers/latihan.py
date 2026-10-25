from fastapi import APIRouter, Depends

from ..deps import butuh_peran
from ._stub import belum_dibuat

# Hanya siswa. Penilaian di server; kunci jawaban baru dikirim setelah jawaban dikumpulkan.
router = APIRouter(tags=["latihan"], dependencies=[Depends(butuh_peran("siswa"))])


@router.post("/latihan")
def kumpulkan():
    belum_dibuat()
