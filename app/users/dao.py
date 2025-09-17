from app.users.models import User
from app.dao.base_dao import BaseDAO

class UserDAO(BaseDAO):
    model = User
