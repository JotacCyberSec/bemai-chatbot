from fastapi import APIRouter, Depends

from ..deps import butuh_peran
from ._stub import belum_dibuat

router = APIRouter(tags=["analisis"], dependencies=[Depends(butuh_peran("guru"))])


@router.get("/analisis")
def analisis(tingkat: str | None = None, rombel: str | None = None):
    belum_dibuat()


@router.delete("/analisis")
def hapus_analisis():
    belum_dibuat()


@router.get("/dashboard")
def dashboard():
    belum_dibuat()
