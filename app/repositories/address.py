from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.address import Address

class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, address_data: dict) -> Address:
        new_address = Address(**address_data)
        self.session.add(new_address)
        await self.session.flush()
        return new_address
    
    async def get_by_id(self, address_id: int) -> Address | None:
        return await self.session.get(Address, address_id)
    
    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.session.execute(select(Address).offset(skip).limit(limit))
        return result.scalars().all()

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Address))
        return result.scalar()

    async def delete(self, address_id: int) -> bool:
        address = await self.get_by_id(address_id)
        if address:
            await self.session.delete(address)
            await self.session.flush()
            return True
        return False