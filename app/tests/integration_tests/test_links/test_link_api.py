import pytest
from httpx import AsyncClient

@pytest.mark.parametrize("link,status_code",[
    *[("yosdfsiodfsdiojfsi", 422)] * 10,
    ("https://youtube.com", 200)
])
async def test_add_and_get_link(auth_ac: AsyncClient,link,status_code):
    response = await auth_ac.post("/links/create", json={
        "link":link   
    })
    
    assert response.status_code == status_code