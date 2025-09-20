from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    UploadFile,
    File,
)
from src.db.configurations import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import UserUploadAvatarResponceSchema
from src.schemas.auth import User
from src.services.auth import get_current_user
from src.services.users import UserService
from src.repository.users import UserRepository
from src.conf.limiter import limiter
from src.services.upload_file import UploadFileService
from src.conf.config import config as settings

router = APIRouter(prefix="/users", tags=["users"])


async def user_service(db: AsyncSession = Depends(get_db_session)):
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/me", response_model=User)
@limiter.limit("5/minute")
async def me(request: Request, user: User = Depends(get_current_user)):
    return user


@router.patch(
    "/avatar",
    status_code=status.HTTP_200_OK,
    response_model=UserUploadAvatarResponceSchema,
)
async def update_user_avatar(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    service: UserService = Depends(user_service),
):

    avatar_url = UploadFileService(
        settings.CLOUDINARY_NAME,
        settings.CLOUDINARY_API_KEY,
        settings.CLOUDINARY_API_SECRET,
    ).upload_file(file, user.name)

    user_service = UserService(service)
    user = await user_service.update_avatar_url(user.email, avatar_url)

    return user
