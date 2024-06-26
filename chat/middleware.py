from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from graphql_jwt.shortcuts import get_user_by_token
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs

@database_sync_to_async
def get_user(token):
    user = get_user_by_token(token)
    if not user:
        return AnonymousUser()
    return user


class QueryAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that takes token from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        qs = parse_qs(scope["query_string"].decode())
        token = qs.get('token', [None])[0]  # Extract the token value
        scope['user'] = await get_user(token)
        return await self.app(scope, receive, send)
