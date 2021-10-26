import json
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.http import HttpResponseNotFound
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from validate_email import validate_email

from user.models import Profile
from ...tokens import account_activation_token


def signup(request):
    if request.body is not None:
        res = json.loads(request.body)
        if res['email'] is not None:
            user = User.objects.create_user(res['username'], res['email'], res['password'])
            user.save()
            # authenticate(request, username=res['username'], password=res['password'])
            login(request, user, backend='skill.backends.EmailAuthBackend')

            return HttpResponse('ok')
    else:
        return redirect('/')


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.body is not None:

            # add field checks

            rdata = json.loads(request.body)
            email = rdata['email']
            # validate_email arguments set by default
            # It requires additional testing !!!
            email_is_valid = validate_email(email_address=email, check_regex=True,
                                            check_mx=True, from_address=None,
                                            helo_host=None, smtp_timeout=10,
                                            dns_timeout=10, use_blacklist=True)

            if email_is_valid or email_is_valid is None:
                if User.objects.filter(email=rdata['email']).exists():
                    return HttpResponse(json.dumps({'message': 'User already exists!'}), status=409)

                user = User.objects.create_user(rdata['email'], rdata['email'], rdata['password'])
                user.first_name = rdata['username']
                user.save()
                send_email_verification_mail(request, email)

                tokens = get_tokens_for_user(user)
                response = {
                    'refresh_token': tokens['refresh'],
                    'access_token': f"Bearer {tokens['access']}"
                }
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'message': 'Invalid email.'}), status=401)
        else:
            return HttpResponseNotFound({'message': 'Empty request !!!'})


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        rdata = json.loads(request.body)
        try:
            userdata = User.objects.filter(email=rdata['email']).first()

            user = authenticate(request,
                                username=userdata.username,
                                password=rdata['password'])

            tokens = get_tokens_for_user(user)
            response = {
                'refresh_token': tokens['refresh'],
                'access_token': f"Bearer {tokens['access']}"
            }

        except(TypeError, ValueError, IndexError, AttributeError):
            return HttpResponse(json.dumps({'message': 'Email or password is invalid!'}), status=401)
        return HttpResponse(json.dumps(response), content_type='application/json')


def signin(request):
    if request.body is not None:
        res = json.loads(request.body)
        # response is processed in staticfiles/js_files/test_signin.js
        response = {}
        try:
            userdata = User.objects.filter(email=res['email']).first()
            if userdata.profile.verified:
                user = authenticate(request,
                                    username=userdata.username,
                                    password=res['password'])
                login(request, user, backend='skill.backends.EmailAuthBackend')

                tokens = get_tokens_for_user(user)
                response['refresh_token'] = tokens['refresh']
                response['access_token'] = tokens['access']
            else:
                response['verify_email'] = 'To log in you need to verify your email'

        except(TypeError, ValueError, OverflowError, IndexError):
            user = None
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        return redirect('/')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def exit(request):
    logout(request)
    return redirect('/')


def forgot(request):
    if request.body is not None:
        res = json.loads(request.body)
        user = User.objects.filter(email=res['email']).first()
        current_site = get_current_site(request)
        message = render_to_string('mail/pass.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        mail_subject = 'Activate your blog account.'
        to_email = res['email']
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return render(request, 'auth/forgot.html', {})
    else:
        return render(request, 'auth/forgot.html', {})


def api(request):
    return render(request, 'react.html', {})


def send_email_verification_mail(request, email):
    # For now it plays role of Welcome email, because
    # mail verification not used anymore (for now)
    current_site = get_current_site(request)
    user = get_object_or_404(User, email=email)
    message = render_to_string('mail/verify_email.html', {
        'user': user,
        'domain': current_site.domain,
        'token': user.profile.verification_token,
    })
    mail_subject = 'Activate your account at skill.im'
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.send(fail_silently=False)


def verify_email(request, token):
    try:
        profile = Profile.objects.get(verification_token=token)
    except(TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        profile = None
    if profile is not None:
        profile.verified = True
        profile.save()
        return render(request, 'auth/email_activated.html')
    else:
        return HttpResponse('Activation link is invalid!', status=404)
