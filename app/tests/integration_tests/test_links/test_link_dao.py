


from app.links.dao import LinksDAO


async def test_add_and_get_new_link():
    short_code = await LinksDAO.add_link(
        original_url="https://www.youtube.com/@Prezidentkayfa/videos",
        user_id=1
    )
    
    new_link = await LinksDAO.find_one_or_none(short_code=short_code)
    
    assert new_link is not None
    assert new_link.user_id == 1
    assert new_link.short_code == short_code