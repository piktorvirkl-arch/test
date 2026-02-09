import logging
from arq.connections import RedisSettings
from sqlalchemy import select, update


from app.db.session import AsyncSessionLocal
from app.models.address import Address
from app.core.config import settings
from app.services.external_api import ShipEngineClient

logger = logging.getLogger(__name__)

async def validate_address_task(ctx, address_id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Address).where(Address.id == address_id))
        address = result.scalar_one_or_none()
        
        if not address:
            logger.warning(f"Task Failed: Address {address_id} not found")
            return
        
        address_data = {
            "address_line1": address.address_line1,
            "city_locality": address.city_locality,
            "state_province": address.state_province,
            "postal_code": address.postal_code,
            "country_code": address.country_code
        }
        if address.address_line2:
            address_data["address_line2"] = address.address_line2

        try:
            shipengine_client = ShipEngineClient()
            is_valid_result = await shipengine_client.validate_address(address_data)
            status_str = "verified" if is_valid_result else "unverified"

            await session.execute(
                update(Address)
                .where(Address.id == address_id)
                .values(is_valid=is_valid_result)
            )
            await session.commit()
            
            logger.info(f"Result for ID {address_id}: {status_str} (is_valid={is_valid_result})")

        except Exception as e:
            logger.error(f"Error processing address {address_id}: {e}", exc_info=True)

class WorkerSettings:
    functions = [validate_address_task]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
