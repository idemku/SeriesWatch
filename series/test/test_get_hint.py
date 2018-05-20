from django.test import TestCase, Client
from django.urls import reverse
import json


class GetHintTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.c = Client()
        self.response = self.c.get(reverse('get-hint', args=["Westworld"]))
        self.json_data = json.loads(self.response.content.decode("utf-8"))

    def test_hint_correct_title_Westworld(self):
        self.assertEqual(self.json_data['results'][0]['original_name'], "Westworld")

    def test_hint_first_air_Westworld(self):
        self.assertEqual(self.json_data['results'][0]['first_air_date'], "2016-10-02")

    def test_hint_origin_country_Westworld(self):
        self.assertEqual(self.json_data['results'][0]['origin_country'], ['US'])

    def test_hint_origin_country_Westworld(self):
        self.assertEqual(self.json_data['results'][0]['original_language'], 'en')

