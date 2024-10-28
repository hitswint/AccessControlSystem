from django.shortcuts import render
# from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import DetailView
# from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# import os
import AC.gl as gl
import glob
import os
# from channels import Group
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# Create your views here.


@csrf_exempt
def index(request):
    if request.method == 'GET':
        un_lock_value = request.GET.get('un_lock_button')
        spk_value = request.GET.get('spk_button')
        com_value = request.GET.get('com_button')
        update_value = request.GET.get('update_button')
        channel_layer = get_channel_layer()
        if un_lock_value:
            # Channel('websocket.receive').send({'text': str(gl.ON_OFF)})
            gl.UN_LOCK = not gl.UN_LOCK
            if gl.UN_LOCK:
                un_lock_ret = 'unlocked'
            else:
                un_lock_ret = 'locked'

            # Group('default').send({'text': un_lock_value})
            async_to_sync(channel_layer.send)(
                'default',
                {'text': un_lock_value}
            )
            return HttpResponse(un_lock_ret)
        elif spk_value:
            gl.SPK = not gl.SPK
            if gl.SPK:
                spk_ret = 'on'
            else:
                spk_ret = 'off'

            # Group('default').send({'text': spk_value})
            async_to_sync(channel_layer.send)(
                'default',
                {'text': spk_value}
            )
            return HttpResponse(spk_ret)
        elif com_value:
            # Group('default').send({'text': com_value})
            async_to_sync(channel_layer.send)(
                'default',
                {'text': com_value}
            )
            return HttpResponse("Come in!")
        elif update_value:
            # Group('default').send({'text': update_value})
            async_to_sync(channel_layer.send)(
                'default',
                {'text': update_value}
            )
            return HttpResponse("Updating!")
        else:
            un_lock_ret = 'locked'
            spk_ret = 'off'
            return render(request, 'AC/index.html', {
                'un_lock_ret': un_lock_ret,
                'spk_ret': spk_ret,
            })


# * ota_version
class OtaVersionView(DetailView):
    """view for category.html"""

    def get(self, request, *args, **kwargs):
        # 列出文件下所有文件：listdir("./")。
        try:
            new_ver = sorted(glob.glob("Fota/image-*.bin"))[-1][-12:-4]
        except IndexError:
            new_ver = 0
        return HttpResponse(new_ver)


# * ota_update
class OtaUpdateView(DetailView):
    """view for category.html"""

    def get(self, request, *args, **kwargs):
        # request.META字典保存着request中的headers。
        # Version = request.META.get('X_ESP8266_VERSION', '')
        # bin文件命名为image-18040821.bin。
        filepath = sorted(glob.glob("Fota/image-*.bin"))[-1]
        # .split("/")

        response = HttpResponse(
            file_iterator(filepath), content_type='application/octet-stream')
        response[
            'Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(
                filepath)
        response['Content-Length'] = os.path.getsize(filepath)  # 传输给客户端的文件大小
        return response


def file_iterator(file_name, chunk_size=512):
    with open(file_name, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
