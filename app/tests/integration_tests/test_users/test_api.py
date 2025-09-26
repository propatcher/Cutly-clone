import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("jossdoasoda@mail.ru", "kotopes", 200),
        ("jossdoasoda@mail.ru", "kotopes", 409),
        ("abcde", "dsfdsffs", 422),
        (
            "jossdoasgoksad0asd0said0asid0said0asids0adias0disa0-disa0-disa0-di0-asid0a-sid0a-sds0sdfsfsdfdsfdsfsdfdsfsdfsdfsdfsdfdsa-idoda@mafdsfsdfsdfsfafadsfadsfdsafasfdsail.ru",
            "kotopes",
            422,
        ),
    ],
)
async def test_register_new_user_success(
    email, password, status_code, ac: AsyncClient
):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    print(response)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("maria.ivanova@example.com", "secret", 200),
        ("alex.smith@example.com", "secret", 200),
        ("alex.smith@example.com", "fdsdsfsdfsdfsdf", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    print(response)
    assert response.status_code == status_code
