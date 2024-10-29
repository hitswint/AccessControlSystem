# from channels.sessions import channel_session
# from channels import Group


# @channel_session
# def ws_connect(message):
#     Group('default').add(message.reply_channel)
#     message.reply_channel.send({"text": "This is a message from server"})


# def ws_message(message):
#     pass
#     # temp_data = message.content['text']  # 获取传递参数
#     # add = Temperature(value=temp_data)
#     # add.save()  # 不save无法保存到数据库
#     # Channel('websocket.receive').send({'message': 'your message'})
#     # Group('default').send({'text': str(gl.ON_OFF)})  # 调用websocket返回结果


# def ws_disconnect(message):
#     message.reply_channel.send({"text": "Disconnected."})

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'default'

        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # 从某个用户(websocket)接收到消息时执行函数，向频道组发送信息
    def receive(self, text_data):
        # 发送消息到频道组，组内各频道都调用send_message方法

        # 接收json
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # async_to_sync(self.channel_layer.group_send)(
        #     self.group_name,
        #     {
        #         'type': 'send_message',
        #         'message': message
        #     }
        # )

        # 接收字符串
        # async_to_sync(self.channel_layer.group_send)(
        #     self.group_name,
        #     {
        #         'type': 'send_message',
        #         'message': text_data
        #     }
        # )

        pass

    # 从频道组接收到消息后执行方法，向某个用户(websocket)发送信息
    def send_message(self, event):
        message = event['message']
        # 通过websocket发送消息到客户端

        # 发送json
        # self.send(text_data=json.dumps({
        #     'text': message
        # }))

        # 发送字符串
        self.send(message)
