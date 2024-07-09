from rest_framework import serializers

from .models import GoodsForTracking, MyTrackedGoods, MyTasks


class GoodsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GoodsForTracking
        fields = '__all__'


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    goods = serializers.SlugRelatedField(
        slug_field='name', 
        queryset=GoodsForTracking.objects.all().order_by('name'),
        label='выберите наименование товара для отслеживания')
    
    def create(self, validated_data):
        task = MyTasks()
        task.goods = validated_data['goods']
        try:
            task.parse_till_date = validated_data['parse_till_date']
        except KeyError:
            pass
        task.set_interval = validated_data['set_interval']
        task.user = self.context['request'].user
        task.save()
        return task
    
    class Meta:
        model = MyTasks
        exclude = ['user']
        extra_kwargs = {'start_date': {'read_only': True}}
   

class MyGoodsSerializer(serializers.HyperlinkedModelSerializer):
    date_field = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = MyTrackedGoods
        exclude = ['user']
        


