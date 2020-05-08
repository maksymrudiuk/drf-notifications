import json

from rest_framework.status import HTTP_400_BAD_REQUEST

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class AsyncJsonWebTokenSocketMixin:

    async def jwt_auth_error_handling(self):

        data = {}

        if self.has_jwt_auth_error():
            error = self.scope['auth_error']
        else:
            return

        if isinstance(error, InvalidToken):
            data['error'] = {
                'status_code': error.status_code,
                'detail': 'Invalid token error',
            }
        elif isinstance(error, TokenError):
            data['error'] = {
                'status_code': HTTP_400_BAD_REQUEST,
                'detail': 'Token error',
            }
        elif isinstance(error, KeyError):
            data['error'] = {
                'status_code': HTTP_400_BAD_REQUEST,
                'detail': 'Key error',
            }
        else:
            data['error'] = {
                'status_code': HTTP_400_BAD_REQUEST,
                'details': 'Uncaught error',
            }

        await self.accept()
        await self.send(text_data=json.dumps(data), close=True)

    def has_jwt_auth_error(self):
        return 'auth_error' in self.scope.keys()


class JsonWebTokenSocketMixin:

    def jwt_auth_error_handling(self):

        data = {}

        if self.has_jwt_auth_error():
            error = self.scope['auth_error']
        else:
            return

        if isinstance(error, InvalidToken):
            data['error'] = {
                'status_code': error.status_code,
                'detail': error.detail,
            }
        elif isinstance(error, TokenError):
            data['error'] = {
                'status_code': HTTP_400_BAD_REQUEST,
                'detail': 'Invalid token error',
            }
        elif isinstance(error, KeyError):
            data['error'] = {
                'status_code': HTTP_400_BAD_REQUEST,
                'detail': 'Key error',
            }
        else:
            data['error'] = {
                'status_code': HTTP_400_BAD_REQUEST,
                'details': 'Uncaught error',
            }

        self.accept()
        self.send(text_data=json.dumps(data), close=True)

    def has_jwt_auth_error(self):
        return 'auth_error' in self.scope.keys()
