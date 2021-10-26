from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse


class SigninTest(TestCase):

    def setUp(self):
        # credentials must be in json format
        self.credentials = '{"email":"piterson@gmail.com", "password":"secretPassword"}'
        self.test_user = User.objects.create_user(
            username="test_user",
            email="piterson@gmail.com",
            password="secretPassword"
        )

    def test_login_email_verified(self):
        """If user has verified email,
        'signin' endpoint should return access and refresh tokens)"""
        self.test_user.profile.verified = True
        self.test_user.profile.save()
        response = self.client.post(reverse('signin'), data=self.credentials,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access_token')

    def test_login_email_not_verified(self):
        """If user has not verified email,
        'signin' endpoint should return message that asks to verify email"""
        response = self.client.post(reverse('signin'), data=self.credentials,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'verify_email')
