from django.conf.urls import url
from users.views import register, register_handle, login, login_check, \
	logout, user, address, order

urlpatterns = [
    url(r'^register/$', register, name='register'),  # 用户注册
	url(r'^register_handle/$', register_handle, name='register_handle'),  # 用户注册处理
	url(r'^login/$', login, name='login'),  # 显示登录页面
	url(r'^login_check/$', login_check, name='login_check'),  # 用户登录校验
	url(r'^logout/$', logout, name='logout'),  # 用户退出登录
	url(r'^$', user, name='user'),  # 用户中心-信息页
	url(r'^address/$', address, name='address'),  # 用户中心-地址页
	url(r'^order/$', order, name='order'),  # 用户中心-订单页
]
