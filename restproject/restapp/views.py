from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class UserView(viewsets.ModelViewSet):
    queryset = Userprofile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class CouponView(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
