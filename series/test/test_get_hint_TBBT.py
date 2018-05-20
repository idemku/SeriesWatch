from django.test import TestCase, Client
from django.urls import reverse
import json


class GetHintTestTBBT(TestCase):

    @classmethod
    def setUpTestData(self):
        self.c = Client()
        self.response = self.c.get(reverse('get-hint', args=["The Big Bang Theory"]))
        self.json_data = json.loads(self.response.content.decode("utf-8"))

    def test_hint_correct_title_TBBT(self):
        self.assertEqual(self.json_data['results'][0]['original_name'], "The Big Bang Theory")

    def test_hint_first_air_TBBT(self):
        self.assertEqual(self.json_data['results'][0]['first_air_date'], "2007-09-24")

    def test_hint_origin_country_TBBT(self):
        self.assertEqual(self.json_data['results'][0]['origin_country'], ['US'])

    def test_hint_origin_country_TBBT(self):
        self.assertEqual(self.json_data['results'][0]['original_language'], 'en')
