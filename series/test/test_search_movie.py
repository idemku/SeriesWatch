from django.test import TestCase
from series.views import search_movie


class SearchMovieTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.movie_name = "Django Unchained"
        """ Magyarul adja vissza a filmcímet """
        self.movie_name_hu = "Django elszabadul"
        self.dict = search_movie(self.movie_name)

    def test_search_tv_correct_name(self):
        self.assertEqual(self.dict["name"], self.movie_name_hu)

    def test_search_tv_correct_first_air(self):
        self.assertEqual(self.dict["first_air_date"], "2012-12-25")

    def test_search_tv_vote_average_valid(self):
        valid = 0 <= float(self.dict["vote_average"]) <= 10
        self.assertEqual(True, valid)

    def test_search_movie_id(self):
        valid = 0 <= float(self.dict["id"])
        self.assertEqual(True, valid)

    """ Reméljük nincs következő része egy filmnek """
    def test_search_movie_next_episode(self):
        self.assertEqual("Ismeretlen", self.dict["next_episode_date"])
