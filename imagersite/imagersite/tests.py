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
        self.client = Client()

    def test_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_home_photo(self):
        


class LoginTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.set_password('abc')
        self.user1.save()
        # self.profile1 = self.user1.profile


class RegTest(TestCase):
    def setUp(self):
        pass
