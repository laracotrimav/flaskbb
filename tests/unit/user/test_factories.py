from flask import current_app
from flask_login import login_user

from flaskbb.user.forms import ChangePasswordForm
from flaskbb.user.services.factories import (
    change_details_form_factory,
    change_email_form_factory,
    change_password_form_factory,
    password_update_handler,
    settings_form_factory,
)


def test_settings_form_factory_loads_current_user_settings(user, request_context):
    user.theme = "solarized"
    user.language = "en"

    login_user(user)

    form = settings_form_factory()

    assert (form.theme.data, form.language.data) == (
        user.theme,
        user.language,
    )


def test_change_password_form_factory_returns_password_form(user, request_context):
    login_user(user)

    form = change_password_form_factory()

    assert isinstance(form, ChangePasswordForm)


def test_change_email_form_factory_uses_current_user(user, request_context):
    login_user(user)

    form = change_email_form_factory()

    assert form.user == user


def test_change_details_form_factory_loads_current_user(user, request_context):
    user.location = "Goiânia"

    login_user(user)

    form = change_details_form_factory()

    assert form.location.data == user.location


def test_password_update_handler_requests_password_validators(
    request_context, mocker
):
    hook = mocker.patch(
        "flaskbb.user.services.factories.pluggy.hook.flaskbb_gather_password_validators",
        return_value=[[]],
    )

    password_update_handler()

    hook.assert_called_once()
    assert hook.call_args.kwargs["app"] == current_app