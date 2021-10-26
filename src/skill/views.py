from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from validate_email import validate_email

from .models import Post, Order, Review, Leader, HomeData
from .permissions import IsOwnerOrReadOnly
from .serializers import (PostSerializer, UserSerializer, OrderSerializer, ReviewSerializer,
                          LeaderSerializer, HomeSerializer)
from .forms.auth.forms import SignupForm, AuthForm
from .Controllers.Auth.auth import send_email_verification_mail
from .utils import get_country


class HomeAPIView(generics.RetrieveAPIView):
    queryset = HomeData.objects.all()
    serializer_class = HomeSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.queryset.first()

    def get_serializer_context(self):
        """Add current user country to serializer context"""
        country = get_country(self.request)
        context = super().get_serializer_context()
        context['country'] = country
        return context


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]


class OrderCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(email=self.request.user)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ReviewsAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)


class LeadersAPIView(generics.ListCreateAPIView):
    queryset = Leader.objects.all()
    serializer_class = LeaderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(email=self.request.user)


class SignupView(View):
    form_class = SignupForm
    template_name = 'auth/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # validate_email arguments set by default
            # It requires additional testing !!!
            email_is_valid = validate_email(email_address=email, check_regex=True,
                                            check_mx=True, from_address=None,
                                            helo_host=None, smtp_timeout=10,
                                            dns_timeout=10, use_blacklist=True)

            if email_is_valid or email_is_valid is None:
                form.save()
                send_email_verification_mail(request, email)
                return render(request, 'auth/verif_email_sent.html')
            else:
                return HttpResponseBadRequest('Invalid email. Please check your email and try again')
        else:
            return HttpResponseBadRequest('Invalid data')


class SigninView(View):
    template_name = 'auth/signin.html'
    form_class = AuthForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class PostCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]


def send_verification_link(request, email):
    send_email_verification_mail(request, email)
    return render(request, 'auth/verif_email_sent.html')
