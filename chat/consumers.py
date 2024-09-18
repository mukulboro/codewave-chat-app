import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import censor_profanity
from .models import Chat, ChatMessage
from auther.models import PublicUser, PrivateUser
from asgiref.sync import sync_to_async
import random

def compare(current_username, chat):
    is_user1 = False
    if chat.user1.user.username == current_username:
        name_shown = list(chat.u1_name_shown)
        location_shown = list(chat.u1_address_shown)
        is_user1 = True
    else:
        name_shown = list(chat.u2_name_shown)
        location_shown = list(chat.u2_address_shown)
    
    if "0" in location_shown:
        while True:
            random_index = random.randint(0, len(location_shown) - 1)
            if location_shown[random_index] == "0":
                location_shown[random_index] = "1"
                break
    else:
        while True:
            random_index = random.randint(0, len(name_shown) - 1)
            if name_shown[random_index] == "0":
                name_shown[random_index] = "1"
                break
    
    return "".join(name_shown), "".join(location_shown) ,is_user1


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
        message = (text_data_json["message"])["message"]
        username = text_data_json["username"]
        chat_id = self.room_id
        chat = await sync_to_async(Chat.objects.get)(id = chat_id)
        private_user = await sync_to_async(PrivateUser.objects.get)(username = username)
        public_user = await sync_to_async(PublicUser.objects.get)(user = private_user)
        type = (text_data_json["message"])["type"]
        if type == "REVEAL_LETTER":
            new_pattern, new_location_pattern, is_user1 = await sync_to_async(compare)(username, chat)
            if is_user1:
                chat.u1_name_shown = new_pattern
                chat.u1_address_shown = new_location_pattern
            else:    
                chat.u2_name_shown = new_pattern
                chat.u2_address_shown = new_location_pattern
            
            await sync_to_async(chat.save)()

            await self.channel_layer.group_send(
                self.room_name,{
                    "type" : "REVEAL_LETTER",
                    "chat_id" : chat_id
                })
            
        else:
            clean_message = censor_profanity(message)
            new_message = await sync_to_async(ChatMessage.objects.create)(
            chat = chat ,
            message = clean_message , 
            sender = public_user
        )
            await sync_to_async(new_message.save)()
            await self.channel_layer.group_send(
                self.room_name,{
                    "type" : "sendMessage" ,
                    "message" : clean_message , 
                    "username" : username ,
                    "chat_id" : chat_id
                })
    async def sendMessage(self , event) : 
        message = event["message"]
        username = event["username"]
        e_type = event["type"]
        await self.send(text_data = json.dumps({"message":message ,"username":username}))
    async def REVEAL_LETTER(self , event):
        chat_id = event["chat_id"]
        await self.send(text_data = json.dumps({"chat_id" : chat_id, "type" : "REVEAL_LETTER"}))