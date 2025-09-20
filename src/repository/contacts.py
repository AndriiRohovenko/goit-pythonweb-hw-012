from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract, and_, or_, select
from datetime import date, timedelta
from src.db.models import Contacts, User


class ContactsRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, limit: int, skip: int, user: User):
        result = await self.db.execute(
            select(Contacts)
            .filter(Contacts.user_id == user.id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, contact_id: int, user: User):
        result = await self.db.execute(
            select(Contacts).filter(
                Contacts.id == contact_id, Contacts.user_id == user.id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str, user: User):
        result = await self.db.execute(
            select(Contacts).filter(
                Contacts.email == email, Contacts.user_id == user.id
            )
        )
        return result.scalar_one_or_none()

    async def create(self, body: Contacts, user: User, avatar: str = None):
        new_contact = Contacts(**body.model_dump(), user_id=user.id, avatar=avatar)
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def update(self, existing_contact: Contacts, data: dict):
        for field, value in data.items():
            setattr(existing_contact, field, value)
        await self.db.commit()
        await self.db.refresh(existing_contact)
        return existing_contact

    async def delete(self, contact: Contacts):
        await self.db.delete(contact)
        await self.db.commit()

    async def search(
        self,
        name: str | None,
        email: str | None,
        phone: str | None,
        user: User,
    ):
        query = select(Contacts).filter(Contacts.user_id == user.id)

        if name:
            query = query.where(Contacts.name.ilike(f"%{name}%"))
        if email:
            query = query.where(Contacts.email.ilike(f"%{email}%"))
        if phone:
            query = query.where(Contacts.phone.ilike(f"%{phone}%"))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def upcoming_birthdays(self, days: int, user: User):
        today = date.today()
        upcoming = today + timedelta(days=days)

        query = (
            select(Contacts)
            .filter(Contacts.user_id == user.id)
            .where(
                or_(
                    and_(
                        extract("month", Contacts.birthdate) == today.month,
                        extract("day", Contacts.birthdate) >= today.day,
                        extract("day", Contacts.birthdate) <= upcoming.day,
                    ),
                    and_(
                        extract("month", Contacts.birthdate) == upcoming.month,
                        extract("day", Contacts.birthdate) <= upcoming.day,
                    ),
                )
            )
        )

        result = await self.db.execute(query)
        return result.scalars().all()
