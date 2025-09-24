import pytest
from httpx import AsyncClient
from app.tests.conftest import auth_ac

@pytest.mark.parametrize("link,status_code",[
    *[("yosdfsiodfsdiojfsi",401)]*10,
    ("youtube.com",401)
])
async def test_add_and_get_link(auth_ac: AsyncClient,link,status_code):
    response = await auth_ac.post("/links/create", params={
        "link":link   
    })
    
    assert response.status_code == status_code