import logging

from django.conf import settings
from django.db import close_old_connections
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from jwt import decode as jwt_decode
from urllib.parse import parse_qs


logger = logging.getLogger('django')


class JWTTokenAuthMiddleware:
    """
    Custom jwt token auth middleware for django-channels
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()

        try:
            # Use UntypedToken to validate token
            token = parse_qs(scope["query_string"].decode("utf-8"))["token"][0]
            UntypedToken(token)
        except (KeyError, InvalidToken, TokenError) as e:
            logger.info('Token error {}'.format(e))
            return self.inner(dict(scope, user=AnonymousUser(), auth_error=e))
        else:
            # Decode data if token is valid and get user
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user = get_user_model().objects.get(id=decoded_data['user_id'])

            return self.inner(dict(scope, user=user))
