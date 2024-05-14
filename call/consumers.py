from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from account.models import UserModel
from call.models import Call
from private.models import PrivateChat


class GeneralCallConsumer(AsyncJsonWebsocketConsumer):
    users = set()

    async def connect(self):
        self.user = self.scope.get('user')
        if not self.user.is_authenticated:
            await self.close()
        self.user_room_id = f"user_{self.user.id}"
        self.users.add(self.user.id)
        await self.channel_layer.group_add(self.user_room_id, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        self.users.discard(self.user.id)
        await self.channel_layer.group_discard(self.user_room_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        user_id = content.get('user_id')
        call_type = content.get('call_type')
        callee = await self.get_user(user_id)
        if callee:
            call = await self.save_call(caller=self.user, callee=callee, content=content)
            await self.channel_layer.group_send(
                self.user_room_id,
                {'type': 'send_call_request', 'call': call.id if callee.id in self.users else None,
                 'call_type': call_type if call_type in [1, 2] else 1, 'caller': self.user.id, 'callee': callee.id}
            )
            await self.channel_layer.group_send(
                f"user_{callee.id}",
                {'type': 'send_call_request', 'call': call.id if callee.id in self.users else None,
                 'call_type': call_type if call_type in [1, 2] else 1, 'caller': self.user.id, 'callee': callee.id}
            )

    async def send_call_request(self, event):
        call = event.get('call')
        call_type = event.get('call_type')
        caller = event.get('caller')
        callee = event.get('callee')
        await self.send_json(content={'call_id': call if call else None, 'call_type': call_type,
                                      'caller_id': caller, 'callee_id': callee})

    @database_sync_to_async
    def get_user(self, user_id):
        return UserModel.objects.filter(id=user_id).first()

    @database_sync_to_async
    def save_call(self, caller, callee, content):
        private_chat = PrivateChat.objects.filter(Q(owner=callee, user=caller) | Q(owner=caller, user=callee)).first()
        if private_chat:
            return Call.objects.create(
                private_chat=private_chat,
                type=content.get('call_type'),
                caller=caller,
                callee=callee,
                status=Call.NOT_ANSWERED,
            )
        return False


# class VideoChatConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope.get('user')
#         if not self.user.is_authenticated:
#             await self.close()
#         self.video_call_id = self.scope['url_route']['kwargs']['video_chat_id']
#         self.video_call_room_id = f"video_chat{self.video_call_id}"
#         self.video_call = await self.get_video_chat(self.user, self.video_call_id)
#         if self.video_call:
#             await self.channel_layer.group_add(self.video_call_room_id, self.channel_name)
#             await self.accept()
#         else:
#             await self.close()
#
#     async def disconnect(self, code):
#         # await self.channel_layer.group_send(
#         #     self.video_call_room_id,
#         #     {'type': 'end_call_request', 'message_type': 'end_request'}
#         # )
#         await self.channel_layer.group_discard(self.video_call_room_id, self.channel_name)
#
#     async def receive_json(self, content, **kwargs):
#         message_type = content.get('message_type')
#         match message_type:
#             case 'cancel':
#                 await self.update_call_status(video_call=self.video_call, status=Call.CANCELED)
#                 await self.channel_layer.group_send(
#                     self.video_call_room_id,
#                     {'type': 'cancel_call', 'message_type': 'cancel'}
#                 )
#             case 'reject':
#                 await self.update_call_status(video_call=self.video_call, status=Call.REJECT)
#                 await self.channel_layer.group_send(
#                     self.video_call_room_id,
#                     {'type': 'reject_call', 'message_type': 'reject'}
#                 )
#             case 'end_request':
#                 await self.update_call_status(video_call=self.video_call, status=Call.NOT_ANSWERED)
#                 await self.channel_layer.group_send(
#                     self.video_call_room_id,
#                     {'type': 'end_call_request', 'message_type': 'end_request'}
#                 )
#             case 'finish':
#                 # update user status
#                 await self.channel_layer.group_send(
#                     self.video_call_room_id,
#                     {'type': 'finish_call', 'message_type': 'finish'}
#                 )
#             case 'accept':
#                 # update user status
#                 await self.update_call_status(video_call=self.video_call, status=Call.ANSWERED)
#                 await self.channel_layer.group_send(
#                     self.video_call_room_id,
#                     {'type': 'accept_call', 'message_type': 'accept'}
#                 )
#             case 'forward':
#                 await self.channel_layer.group_send(
#                     self.video_call_room_id,
#                     {'type': 'forward_wrtc', 'message_type': content.get('message_type'),
#                      'content_type': content.get('content_type'),
#                      'sender_id': content.get('sender_id'), 'payload': content.get('payload')}
#                 )
#             case _:
#                 print('Invalid message type')
#
#     async def cancel_call(self, event):
#         await self.send_json(content={'message_type': event.get('message_type')})
#
#     async def reject_call(self, event):
#         await self.send_json(content={'message_type': event.get('message_type')})
#
#     async def end_call_request(self, event):
#         await self.send_json(content={'message_type': event.get('message_type')})
#
#     async def accept_call(self, event):
#         await self.send_json(content={'message_type': event.get('message_type')})
#
#     async def finish_call(self, event):
#         await self.send_json(content={'message_type': event.get('message_type')})
#
#     async def forward_wrtc(self, event):
#         await self.send_json(content={
#             'message_type': event.get('message_type'),
#             'content_type': event.get('content_type'),
#             'sender_id': event.get('sender_id'),
#             'payload': event.get('payload')
#         })
#
#     @database_sync_to_async
#     def get_video_chat(self, user, video_call_id):
#         return Call.objects.filter(id=video_call_id, type=Call.VIDEO).filter(Q(caller=user) | Q(callee=user)).first()
#
#     @database_sync_to_async
#     def update_call_status(self, video_call, status):
#         video_call.status = status
#         video_call.save()
#


class CallConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        if not self.user.is_authenticated:
            await self.close()
        self.call_id = self.scope['url_route']['kwargs']['call_id']
        self.call_room_id = f"call_{self.call_id}"
        self.call = await self.get_call(self.user, self.call_id)
        if self.call:
            await self.channel_layer.group_add(self.call_room_id, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        # await self.channel_layer.group_send(
        #     self.call_room_id,
        #     {'type': 'end_call_request', 'message_type': 'end_request'}
        # )
        await self.channel_layer.group_discard(self.call_room_id, self.channel_name)

    async def receive_json(self, content, **kwargs):
        message_type = content.get('message_type')
        match message_type:
            case 'cancel':
                await self.update_call_status(call=self.call, status=Call.CANCELED)
                await self.channel_layer.group_send(
                    self.call_room_id,
                    {'type': 'cancel_call', 'message_type': 'cancel'}
                )
            case 'reject':
                await self.update_call_status(call=self.call, status=Call.REJECT)
                await self.channel_layer.group_send(
                    self.call_room_id,
                    {'type': 'reject_call', 'message_type': 'reject'}
                )
            case 'end_request':
                await self.update_call_status(call=self.call, status=Call.NOT_ANSWERED)
                await self.channel_layer.group_send(
                    self.call_room_id,
                    {'type': 'end_call_request', 'message_type': 'end_request'}
                )
            case 'finish':
                # update user status
                await self.channel_layer.group_send(
                    self.call_room_id,
                    {'type': 'finish_call', 'message_type': 'finish'}
                )
            case 'accept':
                # update user status
                await self.update_call_status(call=self.call, status=Call.ANSWERED)
                await self.channel_layer.group_send(
                    self.call_room_id,
                    {'type': 'accept_call', 'message_type': 'accept'}
                )
            case 'forward':
                await self.channel_layer.group_send(
                    self.call_room_id,
                    {'type': 'forward_wrtc', 'message_type': content.get('message_type'),
                     'content_type': content.get('content_type'),
                     'sender_id': content.get('sender_id'), 'payload': content.get('payload')}
                )
            case _:
                print('Invalid message type')

    async def cancel_call(self, event):
        await self.send_json(content={'message_type': event.get('message_type')})

    async def reject_call(self, event):
        await self.send_json(content={'message_type': event.get('message_type')})

    async def end_call_request(self, event):
        await self.send_json(content={'message_type': event.get('message_type')})

    async def accept_call(self, event):
        await self.send_json(content={'message_type': event.get('message_type')})

    async def finish_call(self, event):
        await self.send_json(content={'message_type': event.get('message_type')})

    async def forward_wrtc(self, event):
        await self.send_json(content={
            'message_type': event.get('message_type'),
            'content_type': event.get('content_type'),
            'sender_id': event.get('sender_id'),
            'payload': event.get('payload')
        })

    @database_sync_to_async
    def get_call(self, user, call_id):
        return Call.objects.filter(id=call_id).filter(Q(caller=user) | Q(callee=user)).first()

    @database_sync_to_async
    def update_call_status(self, call, status):
        call.status = status
        call.save()
