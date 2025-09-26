import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "link,status_code",
    [*[("yosdfsiodfsdiojfsi", 422)] * 10, ("https://youtube.com", 200)],
)
async def test_add_and_get_link(auth_ac: AsyncClient, link, status_code):
    response = await auth_ac.post("/links/create", json={"link": link})

    assert response.status_code == status_code


async def test_get_your_links(auth_ac: AsyncClient, ac: AsyncClient):
    auth_response = await auth_ac.get("/links")
    response = await ac.get("/links")

    assert auth_response.status_code == 200
    assert response.status_code == 401
