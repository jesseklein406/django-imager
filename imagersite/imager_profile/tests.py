#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from .models import ImagerProfile
import factory


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        user1 = ImagerProfile.add(
            fav_camera='unknown',
            address='5j34bekrj',
            web_url='http://www.fakeaddress.com',
            type_photography='badass'
        )
        user1.save()

    def test_create_imager(self):
        new = ImagerProfile.objects[0]
        expected = [
            'unknown',
            '5j34bekrj',
            'http://www.fakeaddress.com',
            'badass'
        ]
        actual = [
            new['fav_camera'],
            new['address'],
            new['web_url'],
            new['type_photography']
        ]
        self.assertEqual(actual, expected)
