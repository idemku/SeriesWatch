from django.test import TestCase
from series.models import User
from django.urls import reverse


class SubscribeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('testpass')
        self.user.save()

    def test_subscribe_successful_with_login(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse('subscribe', args=[63247]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_subscribe_successful_without_login(self):
        response = self.client.get(reverse('subscribe', args=[63247]), follow=True)
        self.assertEqual(response.redirect_chain[len(response.redirect_chain) - 1][1], 302)