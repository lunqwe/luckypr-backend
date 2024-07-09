from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]

        if token:
            try:
                authentication = JWTAuthentication()
                validated_token = await sync_to_async(authentication.get_validated_token)(token)
                user = await sync_to_async(authentication.get_user)(validated_token)
                
                scope['user'] = user
            except Exception as e:
                print(e)
                scope['user'] = None
        else:
            scope['user'] = AnonymousUser()
            
        return await self.inner(scope, receive, send)