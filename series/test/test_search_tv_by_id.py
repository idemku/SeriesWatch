from django.test import TestCase
from series.views import search_tv_by_id


class SearchTvTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.movie_id = 63247
        self.dict = search_tv_by_id(self.movie_id) # Westworld

    def test_search_tv_correct_name(self):
        self.assertEqual(self.dict["name"], "Westworld")

    def test_search_tv_correct_first_air(self):
        self.assertEqual(self.dict["first_air_date"], "2016-10-02")

    def test_search_tv_id(self):
        self.assertEqual(self.movie_id, float(self.dict["id"]))

    def test_search_tv_finished_series(self):
        self.dict = search_tv_by_id(1408)  # DR. House
        self.assertEqual("Ismeretlen", self.dict["next_episode_date"])