#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.test import TestCase
from django.contrib.auth.models import User
from .models import ImagerProfile
import factory


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = 'badass'
    email = factory.LazyAttribute(
        lambda a: '{}@example.com'.format(a.username).lower()
    )


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
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
        self.assertEqual(str(self.profile1), 'badass')
