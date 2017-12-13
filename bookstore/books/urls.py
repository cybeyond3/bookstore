from django.conf.urls import url
from .views import index, detail, list

urlpatterns = [
    url(r'^$', index, name='index'), # 首页
    url(r'^books/(?P<books_id>\d+)/$', detail, name='detail'),  # 详情页
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)/$', list, name='list'),  # 列表页
]
