#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User
from imager_images.models import Photo
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
        self.response = Client().get('/')

    def test_home_template(self):
        self.assertTemplateUsed(self.response, 'index.html')

    def test_home_photo(self):
        self.assertInHTML(
            '<img src="static/images/django_1024x768.png">',
            self.response.content
        )

    def test_login_link(self):
        self.assertInHTML('<a href="localhost/login/">', self.response.content)

    def test_register_link(self):
        self.assertInHTML(
            '<a href="http://localhost/register/">',
            self.response.content
        )


class LoginTest(TestCase):
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

        self.client = Client()

    def test_login_success(self):
        params = {'username': self.user1.username, 'password': 'abc'}
        response = self.client.post('/login/', params)
        self.assertRedirects(response, '/', target_status_code=200)
        self.assertInHTML(self.user1.first_name, response.content)

    def test_logout_success(self):
        self.client.login(username=self.user1.username, password='abc')
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/', target_status_code=200)
        self.assertNotIn(self.user1.username, response.content)

    def test_first_image_in_home(self):
        self.client.login(username=self.user1.username, password='abc')
        response = self.client.get('/')
        self.assertEqual(
            response.context['photo'].photo,
            self.home_photo.photo
        )
        self.assertInHTML('<img src="john.jpg">', response.content)


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
