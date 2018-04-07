from channels.sessions import channel_session
from channels import Group
from TM.models import Temperature


@channel_session
def ws_connect(message):
    Group('default').add(message.reply_channel)
    message.reply_channel.send({"text": "This is a message from server"})


def ws_message(message):
    temp_data = message.content['text']  # 获取传递参数
    add = Temperature(value=temp_data)
    add.save()  # 不save无法保存到数据库
    # Channel('websocket.receive').send({'message': 'your message'})
    # Group('default').send({'text': str(gl.ON_OFF)})  # 调用websocket返回结果


def ws_disconnect(message):
    message.reply_channel.send({"text": "Disconnected."})
