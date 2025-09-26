import pytest

from app.clicks.dao import ClicksDAO
from app.links.dao import LinksDAO
from app.users.dao import UserDAO


@pytest.mark.parametrize(
    "user_id,email,is_present",
    [
        (1, "ivan.petrov@example.com", True),
        (2, "maria.ivanova@example.com", True),
        (3, "alex.smith@example.com", True),
        (5, "....", False),
    ],
)
async def test_find_user_by_id(user_id, email, is_present):
    user = await UserDAO.find_by_id(user_id)
    if is_present:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert not user


@pytest.mark.parametrize(
    "link_id,is_present", [(1, True), (2, True), (3, True), (100, False)]
)
async def test_find_link_by_id(link_id, is_present):
    link = await LinksDAO.find_by_id(link_id)
    if is_present:
        assert link
        assert link.id == link_id
    else:
        assert not link


@pytest.mark.parametrize(
    "click_id,link_id,user_agent,is_present",
    [
        (
            1,
            1,
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            True,
        ),
        (
            2,
            1,
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            True,
        ),
        (100, 1, "alex.smith@example.com", False),
        (500, 5, "....", False),
    ],
)
async def test_find_click_by_id(click_id, link_id, user_agent, is_present):
    click = await ClicksDAO.find_by_id(click_id)
    if is_present:
        assert click
        assert click.id == click_id
        assert click.link_id == link_id
        assert click.user_agent == user_agent
    else:
        assert not click


@pytest.mark.parametrize(
    "user_id,is_present", [(1, True), (2, True), (100, False)]
)
async def test_find_click_by_user_id(user_id, is_present):
    click = await ClicksDAO.get_user_links_with_clicks_join(user_id)
    if is_present:
        assert len(click) > 0
    else:
        assert len(click) == 0


@pytest.mark.parametrize(
    "original_url,user_id",
    [
        ("https://vk.com/feed", 1),
        ("https://samara.hh.ru/", 2),
    ],
)
async def test_add_link_success(original_url, user_id):
    link = await LinksDAO.add_link(original_url, user_id)
    assert link is not None
    assert link.original_url == original_url
    assert link.user_id == user_id
