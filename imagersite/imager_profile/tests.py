#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Photo, Album
from .models import ImagerProfile
import factory


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        user1 = User()
        user1.username = 'badass'
        user1.email = 'badass@badass.com'
        user1.set_password('abc')

        user1.save()

    def test_create_user(self):
        new = User.objects.all()[0]
        expected = [
            'badass',
            'badass@badass.com'
        ]
        actual = [
            new.username,
            new.email
        ]
        self.assertEqual(actual, expected)
