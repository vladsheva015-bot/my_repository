from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache
from datetime import date
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получаем доступ к отелям")
@cache(expire=30)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location : str| None = Query(None, description="Локация"),
        title : str | None = Query(None ,description="название отеля"),
        date_from: date = Query(examples=["2026-08-28"]),
        date_to: date = Query(examples=["2026-08-08"]),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from = date_from,
        date_to = date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/{hotels_id}")
@cache(expire=30)
async def get_hotel(db: DBDep,hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Добавляем новый отель")
async def create_hotel(db: DBDep,hotel_data: HotelAdd= Body(openapi_examples={
    "1":{"summary": "Сочи",
         "value": {
            "title": "Отель ol_in_inclusive 5 звезд у моря",
            "location": "Сочи, ул. Мира, 3",
         }
    },
    "2":{"summary": "Дубай",
         "value": {
            "title": "Отель Rich у фонтана",
            "location": "Дубай, ул. Шейха, 5",
         }
    }
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменяем все данные об отеле ")
async def edit_hotels(db: DBDep,hotel_id :int,hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Изменяем выбранные данные об отеле")
async def edit_part_hotels(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):
    await db.hotels.edit(hotel_data, exclude_unset = True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def  delete_hotels(db: DBDep,hotel_id : int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


