#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client, LiveServerTestCase
from django.contrib.auth.models import User
from imager_images.models import Photo
# from imager_profile.models import ImagerProfile
import factory
from selenium.webdriver.firefox.webdriver import WebDriver


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


class HomepageClientTest(TestCase):
    def setUp(self):
        self.response = Client().get('/')

    def test_home_template(self):
        self.assertTemplateUsed(self.response, 'index.html')


class HomepageLiveServerTest(LiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super(HomepageLiveServerTest, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(HomepageLiveServerTest, cls).tearDownClass()

    def test_home_photo(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        home_photo = self.selenium.find_element_by_id("main-photo")
        home_photo_url = home_photo.get_attribute('src')
        self.assertIn(
            'static/images/django_1024x768.png',
            home_photo_url
        )

    def test_login_link(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        login_link = self.selenium.find_element_by_id("sign-in")
        login_link_href = login_link.get_attribute('href')
        self.assertIn(
            'accounts/login',
            login_link_href
        )

    def test_register_link(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        register_link = self.selenium.find_element_by_id("sign-up")
        register_link_href = register_link.get_attribute('href')
        self.assertIn(
            'accounts/register',
            register_link_href
        )


class LoginLiveServerTest(LiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super(HomepageLiveServerTest, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(HomepageLiveServerTest, cls).tearDownClass()

    def setUp(self):
        self.user1 = UserFactory(
            username='john',
            email='john@example.com',
            first_name='John',
            last_name='Stephenson'
        )
        self.user1.set_password('abc')
        self.user1.save()

        self.home_photo = PhotoFactory(
            user=self.user1,
            title='Neat title',
            photo='john.jpg',
            description='Neat photo',
            published='public'
        )
        self.home_photo.save()

    def test_login_success(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.selenium.find_element_by_name("id_username")
        username_input.send_keys('john')
        password_input = self.selenium.find_element_by_name("id_password")
        password_input.send_keys('abc')
        self.selenium.find_element_by_xpath('//input[@value="Sign in"]').click()

        self.assertEqual(self.selenium.current_url, 'http://localhost:8081/')
        sign_out = self.selenium.find_element_by_id("sign-out")
        self.assertIn('Sign out', sign_out.text)
        user_name = self.selenium.find_element_by_id("user-name")
        self.assertIn(self.user1.first_name, user_name.text)

    def test_logout_success(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.selenium.find_element_by_name("id_username")
        username_input.send_keys('john')
        password_input = self.selenium.find_element_by_name("id_password")
        password_input.send_keys('abc')
        self.selenium.find_element_by_xpath('//input[@value="Sign in"]').click()

        self.selenium.find_element_by_id("sign-out").click()

        self.assertEqual(self.selenium.current_url, 'http://localhost:8081/')
        sign_in = self.selenium.find_element_by_id("sign-in")
        self.assertIn('Sign in', sign_in.text)

    def test_first_image_in_home(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))

        username_input = self.selenium.find_element_by_name("id_username")
        username_input.send_keys('john')
        password_input = self.selenium.find_element_by_name("id_password")
        password_input.send_keys('abc')
        self.selenium.find_element_by_xpath('//input[@value="Sign in"]').click()

        home_photo = self.selenium.find_element_by_id("main-photo")
        home_photo_url = home_photo.get_attribute('src')
        self.assertIn(
            'static/images/john.jpg',
            home_photo_url
        )


class RegTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_registration(self):
        params = {
            'username': 'joseph',
            'email': 'joe@example.com',
            'password1': '123',
            'password2': '123'
        }
        response = self.client.post('/accounts/register/', params)
        self.assertRedirects(
            response,
            '/accounts/register/complete/',
            target_status_code=200
        )
        self.assertEqual(len(User.objects.all()), 1)
