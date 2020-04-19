"""wfh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from work_for_hire import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('seller/', views.seller, name="seller"),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_user, name='login'),
    path('all_services/', views.all_services, name='all_services'),
    path('seller_services/', views.seller_services, name='seller_services'),
    path('order_show/', views.order_show, name='order_show'),
    path('buyer_rst/', views.buyer_request_create, name='buyer_rst_create'),
    path('requests/', views.buyer_rst_show, name='buyer_rst_show'),
    path('inbox_view/', views.inbox_view, name='inbox_view'),
    path('msg/', views.message_view, name='message_view'),

    re_path(r'^inbox/(?P<people_id>[\w-]+)/$', views.create_inbox_members, name='contact'),
    re_path(r'^chatting/(?P<order_id>[\w-]+)/$', views.chatting, name='chatting'),
    re_path(r'^delete_services/(?P<su_pk>[\w-]+)/$', views.delete_services, name='delete_services'),
    re_path(r'^update_services/(?P<su_pk>[\w-]+)/$', views.update_services, name='update_services'),
    re_path(r'^deliver/(?P<o_pk>[\w-]+)/$', views.deliver_success, name="delivery"),
    re_path(r'^order/(?P<srv_pk>[\w-]+)/$', views.order_services, name="purchase_services"),
    re_path(r'^index/(?P<u_id>[\w-]+)/$', views.services_show, name="services_show"),
    re_path(r'^(?P<s_pk>[\w-]+)/$', views.services_pk, name="services_pk"),
    re_path(r'^profile/(?P<u_id>[\w-]+)/$', views.portfolio_show, name="portfolio_show"),
    re_path(r'^create/(?P<pk_create>[\w-]+)/$', views.create_s, name='create_s'),
    re_path(r'^portfolio/(?P<up_id>[\w-]+)/$', views.portfolio, name='portfolio'),
    # re_path(r'^messages/(?P<inbox_id>[\w-]+)$', views.message_view, name='message_view'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
