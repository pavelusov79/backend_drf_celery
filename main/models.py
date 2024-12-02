import datetime
import json

from django.db import models
from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask, IntervalSchedule, PeriodicTasks
from django.utils import timezone


class GoodsForTracking(models.Model):
    name = models.CharField(
        verbose_name='введите наименование товара с сайта wildberries для отслежения цен', 
        max_length=128)
    articul = models.PositiveIntegerField(
        verbose_name='введите артикул товара с сайта wildberries')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class MyTrackedGoods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='полное наименование товара', max_length=128)
    articul = models.PositiveIntegerField(verbose_name='артикул')
    brand_name = models.CharField(verbose_name='брэнд', max_length=32)
    price = models.PositiveIntegerField(verbose_name='цена товара')
    discount_price = models.PositiveIntegerField(
        verbose_name='цена товара со скидкой', blank=True, null=True)
    date_field = models.DateTimeField(
        default=timezone.now, verbose_name="дата время")


class MyTasks(models.Model):
    INTERVAL = (
        (3600, '1 hour'),
        (3600*12, '12 hours'),
        (3600*24, '24 hours'),
        (180, '3 min test'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(
        GoodsForTracking, 
        on_delete=models.CASCADE, 
        verbose_name='выберите товар для отслеживания')
    set_interval = models.CharField(
        max_length=15, 
        choices=INTERVAL, 
        verbose_name='выберите интервал отслеживания')
    start_date = models.DateTimeField(default=timezone.now)
    parse_till_date = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name='введите дату окончания отслеживания', 
        help_text='поле может быть пустым')


def task_post_save(sender, instance, signal, *args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=instance.set_interval, 
        period=IntervalSchedule.SECONDS)
    t = PeriodicTask.objects.create(
        interval=schedule, 
        name=f"task{instance.id}",
        task='main.tasks.parse_card',
        args=json.dumps([instance.goods.articul, instance.user.id]), 
        start_time=datetime.datetime.now(),
        expires=instance.parse_till_date)
    t.last_run_at = None
    t.save()
    PeriodicTasks.changed(t)


models.signals.post_save.connect(task_post_save, sender=MyTasks)




 


