from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache
from datetime import date
from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import  ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.services.hotels import HotelService

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
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}")
@cache(expire=30)
async def get_hotel(db: DBDep,hotel_id: int):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException



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
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменяем все данные об отеле ")
async def edit_hotels(db: DBDep,hotel_id :int,hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_data, hotel_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Изменяем выбранные данные об отеле")
async def edit_part_hotels(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep,
):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def  delete_hotels(db: DBDep,hotel_id : int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}


