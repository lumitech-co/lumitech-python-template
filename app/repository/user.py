from app.database.models import User
from app.repository.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    pass


user_repository = UserRepository(User)
