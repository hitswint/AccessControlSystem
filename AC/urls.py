from django.urls import path
from AC.views import index, OtaVersionView, OtaUpdateView
# from swint.models import Article, Category

urlpatterns = [
    path(r'^$', index, name='index-view'),
    path(r'^Fota/image.version$',
        OtaVersionView.as_view(),
        name='ota-version-view'),
    path(r'^Fota/image.bin$', OtaUpdateView.as_view(), name='ota-update-view'),
]
