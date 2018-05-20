from django.test import TestCase
from django.urls import reverse
from series.models import User, SeriesTable


class SubscribeTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('testpass')
        self.user.save()

        sr_table = SeriesTable(seriesID=1418)
        sr_table.save()

    def test_subscribe_successful_with_login(self):

        response = self.client.get(reverse('unsubscribe', args=[1418]), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_subscribe_successful_without_login(self):

        response = self.client.get(reverse('unsubscribe', args=[1418]), follow=True)
        self.assertEqual(response.redirect_chain[len(response.redirect_chain) - 1][1], 302)