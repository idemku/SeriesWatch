from django.test import TestCase
from series.models import SeriesTable
from series.models import User


class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Run once to set up non-modified data for all class methods.
        pass

    def setUp(self):
        # Run once for every test method to setup clean data.
        pass

    def test_username_correct(self):
        user = User(username="testuser", password="test")
        self.assertEqual(user.get_username(), "testuser")

    def test_user_default_email_status(self):
        user = User(username="testuser", password="test")
        self.assertEqual(user.emailNotify, False)

    def test_user_notify_status(self):
        usr = User(username="testuser", password="test", emailNotify=True)
        self.assertEqual(usr.emailNotify, True)

    def test_SeriesTable_str(self):
        sr_table = SeriesTable(seriesID=1418)
        self.assertEqual(sr_table.seriesID, 1418)

    def test_SeriesTable_user_amount(self):
        users = [
            User(username="testusr1", password="test", emailNotify=True),
            User(username="testusr2", password="test", emailNotify=True)
        ]

        sr_table = SeriesTable(seriesID=1418)
        sr_table.save()

        for user in users:
            user.save()
            sr_table.users.add(user)

        sr_table.users.count()
        self.assertEqual(sr_table.users.count(), len(users))

    # Több ugyanolyan nevű Usert a django nem enged hozzáadni a táblához, így azt nem teszteljük.

