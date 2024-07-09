from djangochannelsrestframework import mixins
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
import json 
from djangochannelsrestframework.observer.generics import action, ObserverModelInstanceMixin

from .models import User
from .serializers import UserSerializer

class UserConsumer(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericAsyncAPIConsumer,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @database_sync_to_async
    def set_user_activity(self, is_active: bool):
        self.user.is_online = is_active
        if not is_active:
            self.user.was_online_at = timezone.now()
        self.user.save()

    async def update_user_activity(self, is_active: bool):
        await self.set_user_activity(is_active)
        
    async def disconnect_user_handler(self):
        await self.online_users()
        
    @database_sync_to_async
    def get_online_users(self):
        users = User.objects.filter(is_online=True)
        return list(users)
    
        
    async def connect(self):
        await self.channel_layer.group_add('users', self.channel_name)

        user = self.scope.get('user')
        if user:
            await self.accept()
            if user != AnonymousUser:
                self.user = user
                await self.update_user_activity(is_active=True)
            else:
                self.user = None
        else:
            await self.close(reason="User token is not valid.")
            
            
    @action()
    async def online_users(self, *args, **kwargs):
        try:
            users = await self.get_online_users()
            print("online users action: True")
            serialized_users = [{'id': user.id, 'username': user.username} for user in users]
            await self.channel_layer.group_send(
                'users',
                {
                    'type': 'send_online_users',
                    'users': serialized_users,
                }
            )
        except Exception as e:
            print('Online users error:', e)
            
    async def send_online_users(self, event):
        await self.send_json({
            'message_type': 'online_users',
            'users': event['users'],
        })
    
    async def disconnect(self, code):
        try:
            if self.user:
                await self.update_user_activity(is_active=False)
                await self.disconnect_user_handler()
        except Exception as e:
            print('Disconnect error:', e)
        finally:
            await super().disconnect(code)
        
        
    