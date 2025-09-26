from app.links.dao import LinksDAO


async def test_add_and_get_new_link():
    link = await LinksDAO.add_link(
        original_url="https://www.youtube.com/@Prezidentkayfa/videos",
        user_id=1,
    )

    new_link = await LinksDAO.find_one_or_none(original_url=link.original_url)

    assert new_link is not None
