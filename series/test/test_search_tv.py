from django.test import TestCase
from series.views import search_tv


class SearchTvTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.movie_name = "Westworld"
        self.dict = search_tv(self.movie_name)

    def test_search_tv_correct_name(self):
        self.assertEqual(self.dict["name"], self.movie_name)

    def test_search_tv_correct_first_air(self):
        self.assertEqual(self.dict["first_air_date"], "2016-10-02")

    def test_search_tv_vote_average_valid(self):
        valid = 0 <= float(self.dict["vote_average"]) <= 10
        self.assertEqual(True, valid)

    def test_search_tv_id(self):
        valid = 0 <= float(self.dict["id"])
        self.assertEqual(True, valid)

    def test_seact_tv_finished_series(self):
        self.dict = search_tv("House M.D")
        self.assertEqual("Ismeretlen", self.dict["next_episode_date"])