from django.conf.urls import url
from AC.views import index, OtaVersionView, OtaUpdateView
# from swint.models import Article, Category

urlpatterns = [
    url(r'^$', index, name='index-view'),
    url(r'^Fota/image.version$',
        OtaVersionView.as_view(),
        name='ota-version-view'),
    url(r'^Fota/image.bin$', OtaUpdateView.as_view(), name='ota-update-view'),
]
