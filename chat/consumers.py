from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from members.models import Members
from .models import Group, Message
import json


class JoinAndLeave(WebsocketConsumer):
	def connect(self):
		self.room_uuid = self.scope['url_route']['kwargs']['uuid']
		self.room_group_name = f'chat_{self.room_uuid}'

		async_to_sync(self.channel_layer.group_add)(
		    self.room_group_name, self.channel_name
		)
		self.accept()

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		user_id = self.scope['user'].user_id

		user = Members.objects.get(user_id=user_id)
		group = Group.objects.get(uuid=self.room_uuid)

		db_insert = Message(author=user,content=message,group=group)
		db_insert.save()

		async_to_sync(self.channel_layer.group_send)(
		    self.room_group_name, {'type': 'chat_message', 'message': f'{user.username}: {message}'}
		)

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
		    self.room_group_name, self.channel_name
		)

	def chat_message(self, event):
		message = event['message']
		self.send(text_data=json.dumps({'message': message}))