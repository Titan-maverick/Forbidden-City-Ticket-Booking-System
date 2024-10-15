"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from gugong.views import (success_view, WeChatLoginView,
                          UpdatePhoneView, UpdateVisitorView,
                          DeleteVisitorView, AddVisitorView, ComfirmOrdersView,
                          UserOrdersView, PayView, RefundView,
                          AvailableTicketsView, OtherAvailableTicketsView)

urlpatterns = [
    path('', success_view, name='success_view'),  # 空路径
    path('login/', WeChatLoginView.as_view(), name='wechat-login'),
    path('update-phone/', UpdatePhoneView.as_view(), name='update_phone'),
    path('update-visitor/', UpdateVisitorView.as_view(), name='update_visitor'),
    path('delete-visitor/', DeleteVisitorView.as_view(), name='delete_visitor'),
    path('add-visitor/', AddVisitorView.as_view(), name='add-visitor'),
    path('comfirm-orders/', ComfirmOrdersView.as_view(), name='comfirm-orders'),
    path('my-orders/', UserOrdersView.as_view(), name='my-orders'),
    path('pay/', PayView.as_view(), name='pay'),
    path('refund/', RefundView.as_view(), name='refund'),
    path('get-available-tickets/', AvailableTicketsView.as_view(), name='get-available-tickets'),
    path('get-available-othertickets/', OtherAvailableTicketsView.as_view(), name='get-available-othertickets'),
]
