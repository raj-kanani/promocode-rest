from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = DefaultRouter()
router.register('user', views.UserView)
router.register('coupon', views.CouponView)
router.register('order', views.OrderView)

urlpatterns = [
    path('gettoken/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls))
]
