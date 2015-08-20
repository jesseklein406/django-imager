#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.core import mail
from django.test.utils import override_settings
import factory
from splinter import Browser
from imager_images.models import Photo


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

    @classmethod
    def setUpClass(cls):
        super(LiveServerTest, cls).setUpClass()
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(LiveServerTest, cls).tearDownClass()

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
        self.browser.visit('%s%s' % (self.live_server_url, '/accounts/login/'))

        self.browser.fill('username', username)
        self.browser.fill('password', password)
        self.browser.find_by_value('Log in').first.click()

    # These test for anonymous user cases

    def test_home_photo(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/'))
        home_photo = self.browser.find_by_id("main-photo")
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/static/images/django_1024x768.png'),
            home_photo['src']
        )

    def test_login_link(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/'))
        login_link = self.browser.find_by_id("sign-in")
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/accounts/login/'),
            login_link['href']
        )

    def test_register_link(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/'))
        register_link = self.browser.find_by_id("sign-up")
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/accounts/register/'),
            register_link['href']
        )

    # These test for logged in user

    def test_login_success(self):
        self.login_helper('john', 'abc')

        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/profile/')
        )
        sign_out = self.browser.find_by_id("sign-out")
        self.assertEqual('sign out', sign_out.text.lower())
        user_name = self.browser.find_by_id("user-name")
        self.assertEqual(self.user1.username, user_name.text)

    def test_logout_success(self):
        self.login_helper('john', 'abc')

        self.browser.find_by_id("sign-out").click()

        self.assertEqual(
            self.browser.url,
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
        self.browser.visit('%s%s' % (self.live_server_url, '/'))

        home_photo = self.browser.find_by_id("main-photo")
        self.assertEqual(
            '%s%s' % (self.live_server_url, '/media/john.jpg'),
            home_photo['src']
        )

    # This tests for registering user

    def test_registration(self):
        self.browser.visit('%s%s' % (self.live_server_url, '/accounts/register/'))

        self.browser.fill("username", "joseph")
        self.browser.fill("email", "joe@example.com")
        self.browser.fill("password1", "123")
        self.browser.fill("password2", "123")
        self.browser.find_by_value("Submit").first.click()

        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/accounts/register/complete/')
        )

        link_end = mail.outbox[0].body.split('days:')[1].split()[0][18:]
        link = '%s%s' % (self.live_server_url, link_end)
        self.browser.evaluate_script('document.location="%s"' % link)
        self.assertEqual(
            self.browser.url,
            '%s%s' % (self.live_server_url, '/accounts/activate/complete/')
        )
        self.login_helper('joseph', '123')
        user_name = self.browser.find_by_id("user-name")
        self.assertEqual('joseph', user_name.text)
