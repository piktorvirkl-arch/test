from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.address import Address

class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Address]:
        query = select(Address).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, address_id: int) -> Optional[Address]:
        query = select(Address).where(Address.id == address_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, address_data: dict) -> Address:
        address = Address(**address_data)
        self.session.add(address)
        return address

    async def delete(self, address_id: int) -> bool:
        query = delete(Address).where(Address.id == address_id)
        result = await self.session.execute(query)
        return result.rowcount > 0
