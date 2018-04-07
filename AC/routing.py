# routing.py
from channels.routing import route
from TM.consumers import ws_connect, ws_message, ws_disconnect
# from .channel_handlers import braintree_process

# route(‘channel名称’, ‘消费方法’,’路径’)
# 其中路径若为空，则消费者获得所以发送给websocket.receive频道的消息。path必须以/开头
channel_routing = [
    # route("http.request", http_consumer)
    # 响应http.request，有HTTP请求时就会响应，同时urls.py里面的表单会失效。
    # route("work-run", worker_calling, path=r"^/websocket/"),
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
