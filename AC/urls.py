from django.conf.urls import url
from TM.views import index, index_plot
# from swint.models import Article, Category

urlpatterns = [
    url(r'^$', index, name='index-view'),
    url(r'^plot$', index_plot, name='index-plot-view'),
]
