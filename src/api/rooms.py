from datetime import date
from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, Query
from src.api.dependencies import DBDep
from src.exceptions import  RoomNotFoundHTTPException, \
    HotelNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.schemas.rooms import  RoomAddRequest,  RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получаем доступ к номерам отеля")
@cache(expire=30)
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        date_from: date = Query(examples=["2026-08-28"]),
        date_to: date = Query(examples=["2026-08-08"]),
):
    return await RoomService(db).get_filter_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получаем доступ к номеру")
@cache(expire=30)
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        return await db.rooms.get_one_or_none_with_rels(id=room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException



@router.post("/{hotel_id}/rooms", summary="Добавляем новый номер")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest= Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменяем все данные о номере ")
async def edit_room(db: DBDep,hotel_id :int,room_id: int, room_data: RoomAddRequest):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Изменяем выбранные данные о номере")
async def edit_part_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    await RoomService(db).edit_part_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def  delete_room(db: DBDep,hotel_id : int, room_id: int):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}