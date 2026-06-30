from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.services.facilities import FacilityService
from src.api.dependencies import DBDep
from src.schemas.facilities import  FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получаем доступ к удобствам")
@cache(expire= 10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facility()


@router.post("", summary="Добавляем удобства в номер")
async def add_facilities(db: DBDep, facilities_data: FacilitiesAdd= Body()):
    facilities = await FacilityService(db).create_facility(facilities_data)

    return {"status": "OK", "data": facilities}