from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundException, \
    RoomNotFoundHTTPException, AllRoomsAreBookedHTTPException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.get("")
@cache(expire= 10)
async def get_bookings(db:DBDep):
    return await BookingService(db).get_booking()

@router.get("/me")
async def get_my_bookings(db:DBDep, user_id: UserIdDep,):
    return await BookingService(db).get_my_bookings(user_id=user_id)


@router.post("")
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(
            user_id=user_id,
            booking_data=booking_data
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
