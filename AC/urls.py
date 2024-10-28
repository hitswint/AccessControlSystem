from django.urls import path, re_path
from AC.views import index, OtaVersionView, OtaUpdateView
# from swint.models import Article, Category

urlpatterns = [
    re_path(r'^$', index, name='index-view'),
    re_path(r'^Fota/image.version$',
        OtaVersionView.as_view(),
        name='ota-version-view'),
    re_path(r'^Fota/image.bin$', OtaUpdateView.as_view(), name='ota-update-view'),
]
