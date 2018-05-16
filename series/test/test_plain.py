from django.test import TestCase
from django.urls import reverse


class PlainTest(TestCase):

    def test_index_loads(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_get_hint_loads(self):
        response = self.client.get(reverse("get-hint", args=["test"]))
        self.assertEqual(response.status_code, 200)

    # Visszairányít a főoldalra, ha nem adunk meg adatokat.

    def test_plain_login_loads_without_data(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_plain_logout_loads_without_data(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_plain_register_loads_without_data(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_plain_myprofile_loads_without_login(self):
        response = self.client.get(reverse('myprofile'))
        self.assertEqual(response.status_code, 302)

    def test_subscribe_loads_without_login(self):
        response = self.client.get(reverse('subscribe', args=[0]))
        self.assertEqual(response.status_code, 302)

    def test_unsubscribe_loads_without_login(self):
        response = self.client.get(reverse('unsubscribe', args=[0]))
        self.assertEqual(response.status_code, 302)

    def test_plain_my_series_loads(self):
        response = self.client.get(reverse('my-series'))
        self.assertEqual(response.status_code, 302)