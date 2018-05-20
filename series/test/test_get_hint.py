from django.test import TestCase, Client
from django.urls import reverse
import json

class GetHintTest(TestCase):


    def custom_setup(self, title):
        self.response = response = self.client.get(reverse('get-hint', args=[title]))
        self.json_data = json.loads(response.content.decode("utf-8"))

    """ Teszteljük sorozattal """

    def test_hint_correct_title_Westworld(self):
        self.custom_setup("Westworld")
        self.assertEqual(self.json_data['results'][0]['original_name'], "Westworld")

    def test_hint_first_air_Westworld(self):
        self.custom_setup("Westworld")
        self.assertEqual(self.json_data['results'][0]['first_air_date'], "2016-10-02")

    def test_hint_origin_country_Westworld(self):
        self.custom_setup("Westworld")
        self.assertEqual(self.json_data['results'][0]['origin_country'], ['US'])

    def test_hint_origin_country_Westworld(self):
        self.custom_setup("Westworld")
        self.assertEqual(self.json_data['results'][0]['original_language'], 'en')

    """ Egy másik sorozattal is teszteljük"""

    def test_hint_correct_title_TBBT(self):
        self.custom_setup("The Big Bang Theory")
        #print(json_data['results'][0])
        self.assertEqual(self.json_data['results'][0]['original_name'], "The Big Bang Theory")

    def test_hint_first_air_TBBT(self):
        self.custom_setup("The Big Bang Theory")
        self.assertEqual(self.json_data['results'][0]['first_air_date'], "2007-09-24")

    def test_hint_origin_country_TBBT(self):
        self.custom_setup("The Big Bang Theory")
        self.assertEqual(self.json_data['results'][0]['origin_country'], ['US'])

    def test_hint_origin_country_TBBT(self):
        self.custom_setup("The Big Bang Theory")
        self.assertEqual(self.json_data['results'][0]['original_language'], 'en')
