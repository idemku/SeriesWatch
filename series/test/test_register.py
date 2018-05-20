from django.test import TestCase
from django.urls import reverse


class RegisterTest(TestCase):

    def test_register(self):
        self.register_user()

        self.assertEqual(self.response.redirect_chain[0][0], '/')

    def test_register_user_pw_dont_match(self):
        response = self.client.post(reverse('register'), {'usrname-r': 'testuser',
                                                          'email-r': 'test@test.com',
                                                          'pwd-r': 'testpass',
                                                          'pwd-r2': 'testpass2'}, follow=True)

        self.assertContains(response, "A megadott jelszavak nem egyeznek meg", status_code=200)

    def test_register_same_user(self):
        self.register_user()
        self.register_user()

        self.assertContains(self.response, "Már van ilyen nevű felhasználó", status_code=200)

    def register_user(self):
        self.response = self.client.post(reverse('register'), {'usrname-r': 'testuser',
                                                               'email-r': 'test@test.com',
                                                               'pwd-r': 'testpass',
                                                               'pwd-r2': 'testpass'}, follow=True)