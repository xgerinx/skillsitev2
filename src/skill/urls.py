from django.urls import path, re_path, include
from django.views.generic import TemplateView
from .Controllers.Home import home
from .Controllers.Auth import auth
from .Controllers.Admin import admin
from .Controllers.Payment import payment
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    HomeAPIView,
    PostDetailAPIView,
    OrderCreateAPIView,
    UserCreateAPIView,
    ReviewsAPIView,
    LeadersAPIView,
    SignupView,
    SigninView,
    PostCreateAPIView,
    send_verification_link,
)

from .serializers import CustomJWTSerializer

# app_name = 'skill-api'
urlpatterns = [
    path('', home.index),
    path('api/home/', HomeAPIView.as_view(), name='api-home'),
    path('locale/', home.locale),
    # path('order/', payment.create),

    # path('api/orders/', OrderCreateAPIView.as_view()),
    # path('api/reviews/', ReviewsAPIView.as_view(), name='list-create'),
    # path('api/leaders/', LeadersAPIView.as_view(), name='leaders'),
    # path('api/login/', include('rest_social_auth.urls_jwt_pair')),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    # /auth/token/login/ - token
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path('auth/', include('djoser.urls.jwt')),

    path('api/register/', auth.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', auth.LoginAPIView.as_view(), name='api_login'),


    # path('signin/', auth.signin, name='signin'),
    # path('signin/', include('social_django.urls', namespace='social')),
    # path('signup/', auth.signup, name='order-create'),
    # for testing purposes only
    # path('test-signin/', SigninView.as_view(), name='test-signin'),
    # path('test-signup/', SignupView.as_view(), name='test-signup'),
    # path('test-post-create/', PostCreateAPIView.as_view(), name='test-post-create'),
    # path('signup/', UserCreateAPIView.as_view()),
    path('logout/', auth.exit, name='logout'),
    path('forgot/', auth.forgot, name='forgot'),
    path('verify/email/<token>/', auth.verify_email, name='verify-email'),
    path('get/verification/link/<email>/', send_verification_link, name='send-verification-link'),
    path('react/', TemplateView.as_view(template_name='react.html')),
    path('close/', TemplateView.as_view(template_name='close.html')),
    # path('administrator/', admin.admin, name='admin'),
    # path('react/payment/', TemplateView.as_view(template_name='react.html')),
    re_path(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),
]
