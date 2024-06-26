from config.db import Session
from config.security import hasher
from src.common.utils import async_command
from ..models import User


@async_command
async def create_admin(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
) -> None:
    async with Session() as db:
        user = User(
            email=email,
            hashed_password=hasher.hash(password),
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_admin=True,
        )

        db.add(user)
        await db.commit()
