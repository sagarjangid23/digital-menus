from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def for_owner(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):
    '''
    A decorator to check logged in user could be a restaurant owner and redirects to the login page if the user isn't authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_owner,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return actual_decorator(function)
    return actual_decorator