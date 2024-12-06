from app.database.models import User
from app.manager.base import BaseManager
from app.repository.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserManager(BaseManager[User, UserRepository, UserCreate, UserUpdate]):
    pass


user_manager = UserManager(User, UserRepository)
