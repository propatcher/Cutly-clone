from app.users.dao import UserDAO
import pytest

@pytest.mark.parametrize("user_id,email,is_present",[
    (1,"ivan.petrov@example.com", True),
    (2,"maria.ivanova@example.com", True),
    (3,"alex.smith@example.com", True),
    (5,"....", False)
])
async def test_find_user_by_id(user_id,email,is_present):
    user = await UserDAO.find_by_id(user_id)
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user