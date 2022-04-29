from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import *
from .tasks import parse_card


class TestCaseMain(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user3', email='user3@example.com', password='12345')
        self.token = Token.objects.filter(user=self.user).first()
        self.goods = GoodsForTracking.objects.create(name='Зарядное устройство для авто', articul=63289091)
        self.task = MyTasks.objects.create(goods=self.goods, set_interval=MyTasks.INTERVAL[0][0], user=self.user)
    
    def test_goods_for_tracking_create(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.post('/api/goods_for_tracking/', 
            {'name': 'зарядное устройство', 'articul': 85886}, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_goods_for_tracking_list(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.get('/api/goods_for_tracking/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_goods_for_tracking_update(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.put(f'/api/goods_for_tracking/{self.goods.id}/', {'articul': 6789, 'name': 'Зарядное устройство для авто'})
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_goods_for_tracking_delete(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.delete(f'/api/goods_for_tracking/{self.goods.id}/')
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_my_task_create(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.post('/api/my_tasks/', 
            {'goods': self.goods.name, 'set_interval': MyTasks.INTERVAL[0][0], 'user': {'user.id': self.user.id}}, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
       
    def test_my_tasks_list(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.get('/api/my_tasks/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_my_task_delete(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.delete(f'/api/my_tasks/{self.task.id}/')
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_my_tracked_goods_list(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        request = self.client.get('/api/my_tracked_goods/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def my_tracked_goods_delete(self):
        self.client.force_authenticate(user=self.user, token=self.token.key)
        parse_card(self.task.goods.articul, self.user.id)
        goods = MyTrackedGoods.objects.filter(articul=self.task.goods.articul).first()
        request = self.client.delete(f'/api/my_tracked_goods/{goods.id}/')
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
