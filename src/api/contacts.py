from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from src.db.configurations import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.contacts import ContactSchema
from src.services.auth import get_current_user
from src.services.contacts import ContactService
from src.repository.contacts import ContactsRepository


router = APIRouter(prefix="/contacts", tags=["contacts"])


async def contact_service(db: AsyncSession = Depends(get_db_session)):
    repo = ContactsRepository(db)
    return ContactService(repo)


@router.get(
    "/",
    response_model=list[ContactSchema],
    status_code=status.HTTP_200_OK,
)
async def get_contacts(
    skip: int = 0,
    limit: int = 25,
    service: ContactService = Depends(contact_service),
    current_user=Depends(get_current_user),
):
    return await service.get_contacts(user=current_user, skip=skip, limit=limit)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    contact: ContactSchema,
    service: ContactService = Depends(contact_service),
    current_user=Depends(get_current_user),
):
    return await service.create_contact(contact, user=current_user)


@router.get(
    "/{contact_id}",
    response_model=ContactSchema,
    status_code=status.HTTP_200_OK,
)
async def get_contact(
    contact_id: int,
    service: ContactService = Depends(contact_service),
    current_user=Depends(get_current_user),
):
    return await service.get_contact(contact_id, user=current_user)


@router.patch(
    "/{contact_id}",
    status_code=status.HTTP_200_OK,
)
async def update_contact(
    contact_id: int,
    contact: ContactSchema,
    service: ContactService = Depends(contact_service),
    current_user=Depends(get_current_user),
):
    return await service.update_contact(contact_id, contact, user=current_user)


@router.delete(
    "/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_contact(
    contact_id: int,
    service: ContactService = Depends(contact_service),
    current_user=Depends(get_current_user),
):
    await service.delete_contact(contact_id, user=current_user)


@router.get(
    "/search/",
    response_model=list[ContactSchema],
    status_code=status.HTTP_200_OK,
)
async def search_contacts(
    name: str | None = Query(None, description="Filter by name"),
    email: str | None = Query(None, description="Filter by email"),
    phone: str | None = Query(None, description="Filter by phone"),
    service: ContactService = Depends(contact_service),
    current_user=Depends(get_current_user),
):
    return await service.search_contacts(name, email, phone, user=current_user)


@router.get(
    "/upcoming-birthdays/",
    response_model=list[ContactSchema],
    status_code=status.HTTP_200_OK,
)
async def get_upcoming_birthdays(
    service: ContactService = Depends(contact_service),
    current_user=Depends(get_current_user),
):
    return await service.upcoming_birthdays(days=7, user=current_user)
