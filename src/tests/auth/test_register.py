from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse


class SignupTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'test_user',
            'email': 'piterson@gmail.com',
            'password1': 'secretPassword',
            'password2': 'secretPassword'
        }

    def get_user(self):
        return User.objects.get(username=self.credentials['username'])

    def test_signup(self):
        response = self.client.post(reverse('test-signup'), self.credentials)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=self.credentials['username']).exists())

    def test_signup_nonexistent_email(self):
        """This test may break if someone will create email as one being used"""

        self.credentials['email'] = 'this_email_shouldnt_exist@gmail.com'
        response = self.client.post(reverse('test-signup'), self.credentials)

        self.assertEqual(response.status_code, 400)

    def test_account_not_verified(self):
        """After users register they get unverified profiles"""
        response = self.client.post(reverse('test-signup'), self.credentials)
        user = self.get_user()

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.profile.verified)

    def test_account_verification(self):
        """Testing account activation link that users receive in mailbox"""
        self.client.post(reverse('test-signup'), self.credentials)
        user = self.get_user()
        token = user.profile.verification_token
        response = self.client.get(reverse('verify-email', kwargs={'token': token}))
        user = self.get_user()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.profile.verified)
