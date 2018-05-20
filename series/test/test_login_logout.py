from django.test import TestCase, Client
from django.urls import reverse
from series.models import User


class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('testpass')
        self.user.save()

    def test_login_successful(self):
        self.assertEqual(True, self.client.login(username="testuser", password="testpass"))

    def test_login_unsuccessful(self):
        self.assertEqual(False, self.client.login(username="testuser2", password="wrongtestpass"))

    def test_login_invalid_username(self):
        response = self.client.post(reverse('login'), {'usrname': 'wrongtestuser', 'pwd': 'testpass'}, follow=True)
        self.assertContains(response, "Nem megfelelő", status_code=200)

    def test_login_invalid_password(self):
        response = self.client.post(reverse('login'), {'usrname': 'wrongtestuser', 'pwd': 'wrongtestpass'}, follow=True)
        self.assertContains(response, "Nem megfelelő", status_code=200)

    def test_login_valid(self):
        response = self.client.post(reverse('login'), {'usrname': 'testuser', 'pwd': 'testpass'}, follow=True)
        self.assertContains(response, "testuser", status_code=200)

    def test_login_correct_redirect(self):
        response = self.client.post(reverse('login'), {'usrname': 'testuser', 'pwd': 'testpass'}, follow=True)
        """ indexre irányít """
        self.assertEqual(response.redirect_chain[0][0], "/")

    def test_logout_successful(self):
        response = self.client.post(reverse('logout'), {'usrname': 'testuser', 'pwd': 'testpass'}, follow=True)
        self.assertEqual(response.status_code, 200)

    """ Nem tudunk kijelentkezni, ha nem voltunk bejelentkezve."""
    def test_logout_unsuccessful(self):
        pass

    def test_logout_correct_redirect(self):
        response = self.client.post(reverse('login'), {'usrname': 'testuser', 'pwd': 'testpass'}, follow=True)
        """ indexre irányít """
        self.assertEqual(response.redirect_chain[0][0], "/")
