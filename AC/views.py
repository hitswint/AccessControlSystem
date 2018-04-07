# from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
# from django.views.generic import ListView
# from django.conf import settings
from TM.models import Temperature
# import logging
from django.views.decorators.csrf import csrf_exempt
import sqlite3
# 查看tables：apt安装sqlite3，然后sqlite3 db.sqlite3，输入.tables。
import matplotlib.pyplot as plt
# import os
import TM.gl as gl
from channels import Group
# matplotlib.use('Agg')
# import matplotlib

# logger = logging.getLogger(__name__)

# Create your views here.


@csrf_exempt
def index(request):
    if request.method == 'POST':
        add = Temperature(value=request.POST.get("temperature_data", ""))
        add.save()  # 不save无法保存到数据库
        return HttpResponse(gl.ON_OFF)
    else:
        on_off_value = request.GET.get('on_off_button')
        if on_off_value:
            gl.ON_OFF = int(on_off_value)
            # Channel('websocket.receive').send({'text': str(gl.ON_OFF)})
            Group('default').send({'text': str(gl.ON_OFF)})
            return HttpResponse(gl.ON_OFF)
        # temperature_list = Temperature.objects.all()
        return render_to_response('TM/index.html', {'on_off': gl.ON_OFF})


def index_plot(request):
    # 从sqlite中获取数据。
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT * FROM TM_Temperature")
    data = cur.fetchall()
    data_0 = [int(row[0]) for row in data][-500:]
    data_2 = [float(row[2]) for row in data][-500:]

    plot_file = 'static/TM/plot.png'
    fig1, ax1 = plt.subplots(figsize=(8, 4), dpi=98)
    ax1.set_title(u'房间温度', fontproperties='KaiTi')
    ax1.set_xlabel(u'时间(小时)', fontproperties='KaiTi')
    ax1.set_ylabel(u'温度(\u2103)', fontproperties='KaiTi')
    plt.ylim(-30, 30)
    ax1.plot(
        data_0,
        data_2, )
    fig1.savefig(plot_file)
    plt.close(fig1)

    # temperature_list = Temperature.objects.all()
    return HttpResponse(plot_file)


# * Base_Mixin
# class Base_Mixin(object):
#     """Basic mix class."""

#     def get_context_data(self, *args, **kwargs):
#         context = super(Base_Mixin, self).get_context_data(**kwargs)
#         try:
#             # 网站标题等内容
#             context['website_title'] = settings.WEBSITE_TITLE
#         except Exception:
#             logger.error(u'[BaseMixin]加载基本信息出错')
#         return context

# * Index_View
# class Index_View(Base_Mixin, ListView):
#     """view for index.html"""
#     model = Temperature
#     # 或者
#     # queryset = Temperature.objects.all()
#     template_name = 'TM/index.html'
#     context_object_name = 'temperature_list'

#     # def get(self, request, *args, **kwargs):
#     #     article_id = self.kwargs.get('id')

#     #     # 如果ip不存在就把文章的浏览次数+1。
#     #     if ip not in visited_ips:
#     #         try:
#     #             article = self.queryset.get(id=article_id)
#     #         except ArticleSwint.DoesNotExist:
#     #             logger.error(u'[ArticleView]访问不存在的文章:[%s]' % article_id)
#     #             raise Http404
#     #         else:
#     #             article.view_times += 1
#     #             article.save()
#     #             visited_ips.append(ip)

#     #         # 更新缓存
#     #         cache.set(article_id, visited_ips, 15 * 60)

#     #     return super(Article_View, self).get(request, *args, **kwargs)

#     @csrf_exempt
#     def post(self, request, *args, **kwargs):
#         add = Temperature(value=request.POST)
#         add.save()  # 不save无法保存到数据库
#         # 或者
#         # Temperature.objects.create(value=request.POST)
#         kwargs['Temp'] = request.POST + 1

#         return super(Index_View, self).post(request, *args, **kwargs)
