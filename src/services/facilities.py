from src.schemas.facilities import FacilitiesAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task

class FacilityService(BaseService):

    async def get_facility(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilitiesAdd):
        facilities = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()
        return facilities