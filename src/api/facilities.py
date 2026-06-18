from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.tasks.tasks import test_task
from src.api.dependencies import DBDep
from src.schemas.facilities import  FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("", summary="Получаем доступ к удобствам")
@cache(expire= 10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Добавляем удобства в номер")
async def add_facilities(db: DBDep, facilities_data: FacilitiesAdd= Body()):
    facilities = await db.facilities.add(facilities_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facilities}