from django.contrib.auth import get_user_model, login
from django.http import request
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Post, Order, Review, Leader, HomeData, Client
from .Controllers.Payment.payment import Payment
from catalog.serializers import CourseForLiderSerializer, RatingSerializer

User = get_user_model()


class CustomJWTSerializer(TokenObtainPairSerializer):
    # username_field = 'id'

    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        # or User.objects.filter(username=attrs.get("username")
        user_obj = User.objects.filter(id=attrs.get("username")).first()
        if user_obj:
            credentials['username'] = user_obj.username

        return super().validate(credentials)


class UserPublicSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserSaveSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        login(request, user, backend='skill.backends.EmailAuthBackend')
        return user


class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        # view_name='skill-api:detail',
        view_name='detail',
        lookup_field='slug'
    )
    user = UserPublicSerializer(read_only=True)
    publish = serializers.DateField(default=timezone.now())

    class Meta:
        model = Post
        fields = [
            'url',
            'slug',
            'user',
            'title',
            'content',
            'draft',
            'publish',
            'updated',
            'timestamp',
        ]


class OrderSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        pay = Payment()
        url = pay.create(validated_data)
        order = Order.objects.create(
            resource_id=1,
            customer_id=1,
            price=666.456,
            status=1,
            check_no=url,
            country=validated_data['country']
        )
        order.save()

        return order

    class Meta:
        model = Order
        fields = [
            'id', 'country', 'check_no'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    rating_id = RatingSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user_id', 'message', 'rating_id']


class LeaderSerializer(serializers.ModelSerializer):
    course = CourseForLiderSerializer(read_only=True)

    class Meta:
        model = Leader
        fields = ['course']


class ClientFilterSerializer(serializers.ListSerializer):
    """Filter out clients by country"""
    def to_representation(self, data):
        country = self.context['country']
        data = data.filter(country=country)
        return super(ClientFilterSerializer, self).to_representation(data)


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = ClientFilterSerializer
        model = Client
        fields = ['name', 'logo']


class HomeSerializer(serializers.ModelSerializer):
    leaders = LeaderSerializer(many=True, read_only=True)
    clients = ClientSerializer(many=True, read_only=True)

    class Meta:
        model = HomeData
        fields = [
            'font',
            'opportunities',
            'why_us',
            'leaders',
            'clients'
        ]
