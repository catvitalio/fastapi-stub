from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.security import hasher
from config.settings import settings
from src.common.exceptions.confirmation_token import InvalidTokenException
from src.common.services import ConfirmationTokenService
from src.common.tasks import send_mail
from ...dtos import RegisterCompleteDto, RegisterDto
from ...exceptions.auth import (
    UserAlreadyActiveException,
    UserWithThisEmailAlreadyExistsException,
)
from ...models import User


class RegisterService:
    TOKEN_TTL = timedelta(days=365)

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._token_service = ConfirmationTokenService(ttl=self.TOKEN_TTL)

    async def register(self, dto: RegisterDto) -> None:
        await self._validate_user(dto)
        user = await self._create_user(dto)
        await self._send_mail(user)

    async def _validate_user(self, dto: RegisterDto) -> None:
        user = await self._get_user(dto.email, is_active=True)
        if user:
            raise UserWithThisEmailAlreadyExistsException

    async def _create_user(self, dto: RegisterDto) -> User:
        user = await self._get_user(dto.email, is_active=False)
        if not user:
            user = User(
                email=dto.email,
                hashed_password=hasher.hash(dto.password),
                first_name=dto.first_name,
                last_name=dto.last_name,
                is_active=False,
            )
            self._db.add(user)
            await self._db.commit()
            await self._db.refresh(user)

        return user

    async def _get_user(self, email: str, *, is_active: bool) -> User | None:
        results = await self._db.execute(
            select(User).where(User.email == email, User.is_active == is_active),
        )
        return results.scalar_one_or_none()

    async def _send_mail(self, user: User) -> None:
        token = self._token_service.generate(user.id)
        await send_mail.kiq(
            'Registration',
            'mail/register.html',
            {'link': f'{settings.FRONTEND_URL}/confirm?token={token}'},
            [user.email],
        )

    async def complete(self, dto: RegisterCompleteDto) -> User:
        id = self._token_service.decode(dto.token)  # noqa: A001
        user = await self._db.get(User, int(id))

        if not user:
            raise InvalidTokenException
        elif user.is_active:
            raise UserAlreadyActiveException

        user.is_active = True
        await self._db.commit()

        return user
