from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.contrib.auth.models import User

from .serializers import GoodsSerializer, TaskSerializer, MyGoodsSerializer
from .models import GoodsForTracking, MyTasks, MyTrackedGoods


class MyTrackedGoodsPaginationClass(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class GoodsForTrackingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = GoodsForTracking.objects.all()
    serializer_class = GoodsSerializer


class MyTasksViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    queryset = MyTasks.objects.all()

    def get_queryset(self):
        u = get_object_or_404(User, pk=self.request.user.id)
        queryset = MyTasks.objects.filter(user=u)
        return queryset

   
class MyTrackedGoodsFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    start_date = filters.DateTimeFilter(field_name='date_field', lookup_expr='gte')
    till_date = filters.DateTimeFilter(field_name='date_field', lookup_expr='lte')

    class Meta:
        model = MyTrackedGoods
        fields = ['name', 'start_date', 'till_date']


class MyTrackedGoodsViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MyTrackedGoods.objects.all()
    serializer_class = MyGoodsSerializer
    filterset_class = MyTrackedGoodsFilter
    pagination_class = MyTrackedGoodsPaginationClass
    
    def get_queryset(self):
        u = get_object_or_404(User, pk=self.request.user.id)
        queryset = MyTrackedGoods.objects.filter(user=u)
        return queryset

