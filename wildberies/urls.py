"""wildberies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from main.views import GoodsForTrackingViewSet, MyTasksViewSet, MyTrackedGoodsViewSet
from singup.views import UserSingUpApiView


router = DefaultRouter()
router.register('singup', UserSingUpApiView)
router.register('goods_for_tracking', GoodsForTrackingViewSet)
router.register('my_tasks', MyTasksViewSet)
router.register('my_tracked_goods', MyTrackedGoodsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/', include(router.urls)),
]
