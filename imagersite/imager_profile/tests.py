# from __future__ import unicode_literals

from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

import factory
from faker import Faker
from splinter import Browser
from time import sleep

from .models import ImagerProfile

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Create a fake user."""
    class Meta:
        model = User

    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory(username='badass', email='badass@example.com')
        self.user1.set_password('abc')
        self.user1.save()
        self.profile1 = self.user1.profile

    # Test 1
    # Check that User works as we expect as base class
    def test_create_user(self):
        expected = [
            'badass',
            'badass@example.com'
        ]
        actual = [
            self.user1.username,
            self.user1.email
        ]
        self.assertEqual(actual, expected)
        self.assertIsInstance(self.user1.profile, ImagerProfile)

    # Test 2
    # Check that an imagerProfile is created when user is created
    def test_create_imagerprofile(self):
        self.assertEqual(self.profile1.user.username, 'badass')

    # Test 3
    # Check that camera field can optionally hold data
    def test_camera_field(self):
        self.assertFalse(self.profile1.camera)
        self.profile1.camera = 'potato'
        self.assertEqual(self.profile1.camera, 'potato')

    # Test 4
    # Check that address field can optionally hold data
    def test_address_field(self):
        self.assertFalse(self.profile1.address)
        self.profile1.address = '123 Fake St'
        self.assertEqual(self.profile1.address, '123 Fake St')

    # Test 5
    # Check that web_url field can optionally hold data
    def test_web_url_field(self):
        self.assertFalse(self.profile1.web_url)
        self.profile1.web_url = 'example.com'
        self.assertEqual(self.profile1.web_url, 'example.com')

    # Test 6
    # Check that type_photography field can optionally hold data
    def test_type_photography_field(self):
        self.assertFalse(self.profile1.type_photography)
        self.profile1.web_url = 'astrophotography'
        self.assertEqual(self.profile1.web_url, 'astrophotography')

    # Test 7
    # Check that is_active property works as expected
    def test_is_active(self):
        self.assertIs(self.profile1.user.is_active, True)
        self.assertIs(self.profile1.is_active, True)

    # Test 8
    # Check that is_active can be changed
    def test_is_not_active(self):
        self.assertIs(self.profile1.is_active, True)
        self.profile1.user.is_active = False
        self.assertIs(self.profile1.is_active, False)

    # Test 9
    # Check that ActiveProfileManager works
    def test_active(self):
        self.assertIs(len(ImagerProfile.active.all()), 1)
        self.profile1.user.is_active = False
        self.profile1.user.save()
        self.assertFalse(ImagerProfile.active.all())

    # Test 10
    # Check that if user is killed, imagerProfile is killed
    def test_no_imagerprofile(self):
        self.assertIs(len(ImagerProfile.objects.all()), 1)
        self.user1.delete()
        self.assertFalse(ImagerProfile.objects.all())

    # Test 11
    # Check that if imagerProfile is killed, user is killed
    def test_no_user(self):
        self.assertIs(len(User.objects.all()), 1)
        self.profile1.delete()
        self.assertFalse(User.objects.all())

    # Test 12
    # Check string representation of profile
    def test_string_profile(self):
        self.assertEqual(str(self.profile1), self.user1.get_full_name())


class UserProfileTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('secret')
        self.user1.save()
        self.profile1 = self.user1.profile
        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def test_user1_profile_view_self(self):
        self.client.login(
            username=self.user1.username, password='secret'
        )
        response = self.client.get(reverse('profile:detail'))
        self.assertContains(response, self.user1.email)
        self.assertContains(response, self.user1.username)

    def test_user1_profile_update_view_self(self):
        self.client.login(
            username=self.user1.username, password='secret'
        )
        response = self.client.get(reverse('profile:edit'))
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user1.email)

    def test_user1_profile_update_post_self(self):
        self.client.login(
            username=self.user1.username, password='secret'
        )
        new_data = {
            'email': 'new@example.com',
            'camera': 'Super Nikon',
            'address': '123 Anywhere Dr',
            'web_url': 'http://www.example.com',
            'type_photography': 'existential'
        }
        response = self.client.post(
            reverse('profile:edit'), new_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('profile:detail'))
        for key in new_data:
            self.assertContains(response, new_data[key])


class LiveServerSplinterTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(LiveServerSplinterTest, cls).setUpClass()
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(LiveServerSplinterTest, cls).tearDownClass()
        sleep(3)

    def setUp(self):
        self.user1 = UserFactory(
            username='john',
            email='john@example.com',
            first_name='John',
            last_name='Stephenson'
        )
        self.user1.set_password('abc')
        self.user1.save()

    def login_helper(self, username, password):
        self.browser.visit('{}{}'.format(
            self.live_server_url, '/accounts/login/')
        )

        self.browser.fill('username', username)
        self.browser.fill('password', password)
        self.browser.find_by_value('Log in').first.click()

    def test_non_auth_profile_redirect(self):
        self.browser.visit('{}{}'.format(self.live_server_url, '/profile'))
        self.assertEqual(
            self.browser.url, '{}{}'.format(
                self.live_server_url, '/accounts/login/?next=/profile/'
            )
        )

    def test_non_auth_edit_profile_redirect(self):
        self.browser.visit('{}{}'.format(
            self.live_server_url, '/profile/edit')
        )
        self.assertEqual(
            self.browser.url, '{}{}'.format(
                self.live_server_url, '/accounts/login/?next=/profile/edit/'
            )
        )
