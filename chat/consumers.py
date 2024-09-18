import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import censor_profanity

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_name = f"chat_{self.room_id}"
        await self.channel_layer.group_add(
            self.room_name ,
            self.channel_name
        )
        await self.accept()
    async def disconnect(self , close_code):
        await self.channel.name.group_discard(
            self.room_name , 
            self.channel_name 
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.room_name,{
                "type" : "sendMessage" ,
                "message" : message , 
                "username" : username ,
            })
    async def sendMessage(self , event) : 
        message = event["message"]
        username = event["username"]
        clean_message = censor_profanity(message)
        await self.send(text_data = json.dumps({"message":clean_message ,"username":username}))