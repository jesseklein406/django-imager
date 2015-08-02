#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from imager_images.models import Photo
import factory
from selenium.webdriver.firefox.webdriver import WebDriver
from django.core import mail
from django.test.utils import override_settings
from time import sleep


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email',)


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Photo
        django_get_or_create = (
            'user',
            'title',
            'photo',
            'description',
            'published',
        )


# Homepage client test for template used
class HomepageClientTest(TestCase):
    def test_home_template(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'index.html')


@override_settings(DEBUG=True)
class LiveServerTest(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super(LiveServerTest, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LiveServerTest, cls).tearDownClass()
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
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys(password)
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

    # These test for anonymous user cases

    def test_home_photo(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        home_photo = self.selenium.find_element_by_id("main-photo")
        home_photo_url = home_photo.get_attribute('src')
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/static/images/django_1024x768.png'),
            home_photo_url
        )

    def test_login_link(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        login_link = self.selenium.find_element_by_id("sign-in")
        login_link_href = login_link.get_attribute('href')
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/accounts/login/'),
            login_link_href
        )

    def test_register_link(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        register_link = self.selenium.find_element_by_id("sign-up")
        register_link_href = register_link.get_attribute('href')
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/accounts/register/'),
            register_link_href
        )

    # These test for logged in user

    def test_login_success(self):
        self.login_helper('john', 'abc')

        # make sure we end up home
        self.assertEqual(
            self.selenium.current_url,
            '%s%s%s%s' % (self.live_server_url, '/profile/', self.user1.id, '/')
        )
        sign_out = self.selenium.find_element_by_id("sign-out")
        self.assertEqual('Sign out', sign_out.text)   # Sign out is there
        user_name = self.selenium.find_element_by_id("user-name")
        self.assertEqual(self.user1.username, user_name.text)

    def test_logout_success(self):
        self.login_helper('john', 'abc')

        self.selenium.find_element_by_id("sign-out").click()

        self.assertEqual(
            self.selenium.current_url,
            '%s%s' % (self.live_server_url, '/accounts/logout/')
        )

    def test_first_photo_in_home(self):
        first_photo = PhotoFactory(
            user=self.user1,
            title='Neat title',
            photo='john.jpg',
            description='Neat photo',
            published='public'
        )
        first_photo.save()

        self.login_helper('john', 'abc')
        self.selenium.get('%s%s' % (self.live_server_url, '/'))

        home_photo = self.selenium.find_element_by_id("main-photo")
        home_photo_url = home_photo.get_attribute('src')
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/media/john.jpg'),
            home_photo_url
        )

    # This tests for registering user

    def test_registration(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/register/'))

        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('joseph')
        username_input = self.selenium.find_element_by_id("id_email")
        username_input.send_keys('joe@example.com')
        password_input = self.selenium.find_element_by_id("id_password1")
        password_input.send_keys('123')
        password_input = self.selenium.find_element_by_id("id_password2")
        password_input.send_keys('123')
        self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()

        self.assertEqual(
            self.selenium.current_url,
            '%s%s' % (self.live_server_url, '/accounts/register/complete/')
        )

        link_end = mail.outbox[0].body.split('days:')[1].split()[0][18:]
        link = '%s%s' % (self.live_server_url, link_end)
        self.selenium.get(link)
        self.assertEqual(
            self.selenium.current_url,
            '%s%s' % (self.live_server_url, '/accounts/activate/complete/')
        )
        self.login_helper('joseph', '123')
        user_name = self.selenium.find_element_by_id("user-name")
        self.assertEqual('joseph', user_name.text)
