from django.db.models import Sum
from rest_framework import serializers

from catalog.models import Course, Module
from orders.models import Order, OrderItem




class CourseSerializer(serializers.ModelSerializer):
    """Serializer used in OrderSerializer"""
    class Meta:
        model = Course
        fields = ['name', 'title', 'mnemo']


class ModuleSerializer(serializers.ModelSerializer):
    """Serializer used in OrderSerializer"""
    class Meta:
        model = Module
        fields = ['name', 'mnemo', 'price', 'old_price']


class AddMoreSerializer(serializers.ModelSerializer):
    """Serializer used in OrderSerializer"""
    class Meta:
        model = Module
        fields = ['name', 'mnemo', 'price', 'old_price']


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_old_price = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    promocode = serializers.SerializerMethodField()
    add_more = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.items.aggregate(Sum('module__price')).get('module__price__sum')

    def get_total_old_price(self, obj):
        return obj.items.aggregate(Sum('module__old_price')).get('module__old_price__sum')

    def get_currency(self, obj):
        return 'грн.'

    def get_discount(self, obj):
        return 15

    def get_promocode(self, obj):
        return 'QWERTYUI'

    def get_courses(self, obj):
        modules = Module.objects.filter(id__in=obj.items.values('module_id'))
        courses = {}

        for module in modules:
            if module.course not in courses:
                courses[module.course] = [module]
            else:
                courses[module.course].append(module)

        data = []

        for course, modules in courses.items():
            course_data = CourseSerializer(course).data
            course_data['modules'] = ModuleSerializer(modules, many=True).data
            data.append(course_data)

        return data

    def get_add_more(self, obj):
        add_more = []

        for module in Module.objects.all():
            if module not in Module.objects.filter(id__in=obj.items.values('module_id')):
                add_more.append(module)

        return AddMoreSerializer(add_more, many=True).data

    class Meta:
        model = Order
        fields = ['total_price', 'total_old_price', 'currency', 'discount', 'promocode', 'courses', 'add_more']


class OrderItemSerializer(serializers.ModelSerializer):
    module = serializers.SlugRelatedField(queryset=Module.objects.all(), slug_field='mnemo')

    class Meta:
        model = OrderItem
        fields = '__all__'
