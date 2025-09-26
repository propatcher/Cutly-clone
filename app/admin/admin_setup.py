from sqladmin import Admin, ModelView

from app.clicks.models import Click
from app.links.models import Link
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.created_at]
    form_excluded_columns = [User.hashed_password]


class LinkAdmin(ModelView, model=Link):
    column_list = [
        Link.id,
        Link.original_url,
        Link.short_code,
        Link.user_id,
        Link.is_active,
        Link.clicks_count,
        Link.created_at,
    ]


class ClickAdmin(ModelView, model=Click):
    column_list = [
        Click.id,
        Click.link_id,
        Click.ip_address,
        Click.user_agent,
        Click.clicked_at,
    ]


def setup_admin(app, engine):
    admin = Admin(app, engine)

    admin.add_view(UserAdmin)
    admin.add_view(LinkAdmin)
    admin.add_view(ClickAdmin)

    return admin
