#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User
from imager_images import Photo
# from imager_profile.models import ImagerProfile
import factory


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


class HomepageTest(TestCase):
    def setUp(self):
        self.home_photo = PhotoFactory()
        self.response = Client().get('/')

    def test_home_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_home_photo(self):
        self.assertEqual(
            self.response.context['photo'].photo,
            self.home_photo.photo
        )
        self.assertInHTML('<div id="main-photo">', self.response.content)

    def test_login_link(self):
        self.assertInHTML('<a href="localhost/login/">', self.response.content)

    def test_register_link(self):
        self.assertInHTML(
            '<a href="http://localhost/register/">',
            self.response.content
        )


class LoginTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('abc')
        self.user1.save()
        self.client = Client()
        # self.profile1 = self.user1.profile

    def test_login_success(self):
        params = {'username': self.user1.username, 'password': 'abc'}
        response = self.client.post('/login/', params)
        self.assertRedirects(response, '/', target_status_code=200)
        self.assertInHTML(self.user1.username, response)

    def test_logout_success(self):
        self.client.login(username=self.user1.username, password='abc')
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/', target_status_code=200)
        self.assertNotIn(self.user1.username, response)


class RegTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration(self):
        params = {
            'username': 'joseph',
            'email': 'joe@example.com',
            'password1': '123',
            'password2': '123'}
        response = self.client.post('/accounts/register/', params)
        self.assertRedirects(
            response,
            '/accounts/register/complete/',
            target_status_code=200
        )
        self.assertEqual(len(User.objects.all()), 1)
