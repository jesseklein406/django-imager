#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        user1 = UserFactory()
        user1.set_password('abc')
        user1.save()

    # Test 1
    # Check that User works as we expect as base class
    def test_create_user(self):
        new = User.objects.all()[0]
        expected = [
            'badass',
            'badass@example.com'
        ]
        actual = [
            new.username,
            new.email
        ]
        self.assertEqual(actual, expected)
        self.assertIsInstance(new.profile, ImagerProfile)

    # Test 2
    # Check that an imagerProfile is created when user is created
    def test_create_imagerprofile(self):
        new = ImagerProfile.objects.all()[0]
        self.assertEqual(new.user.username, 'badass')

    # Test 3
    # Check that camera field can optionally hold data
    def test_camera_field(self):
        new = ImagerProfile.objects.all()[0]
        self.assertFalse(new.camera)
        new.camera = 'potato'
        self.assertEqual(new.camera, 'potato')

    # Test 4
    # Check that address field can optionally hold data
    def test_address_field(self):
        new = ImagerProfile.objects.all()[0]
        self.assertFalse(new.address)
        new.address = '123 Fake St'
        self.assertEqual(new.address, '123 Fake St')

    # Test 5
    # Check that web_url field can optionally hold data
    def test_web_url_field(self):
        new = ImagerProfile.objects.all()[0]
        self.assertFalse(new.web_url)
        new.web_url = 'example.com'
        self.assertEqual(new.web_url, 'example.com')

    # Test 6
    # Check that type_photography field can optionally hold data
    def test_type_photography_field(self):
        new = ImagerProfile.objects.all()[0]
        self.assertFalse(new.type_photography)
        new.web_url = 'astrophotography'
        self.assertEqual(new.web_url, 'astrophotography')

    # Test 7
    # Check that is_active property works as expected
    def test_is_active(self):
        new = ImagerProfile.objects.all()[0]
        self.assertIs(new.user.is_active, True)
        self.assertIs(new.is_active, True)

    # Test 8
    # Check that is_active can be changed
    def test_is_not_active(self):
        new = ImagerProfile.objects.all()[0]
        self.assertIs(new.is_active, True)
        new.user.is_active = False
        self.assertIs(new.is_active, False)

    # Test 9
    # Check that ActiveProfileManager works
    def test_active(self):
        new = ImagerProfile.objects.all()[0]
        self.assertIs(len(ImagerProfile.active.all()), 1)
        new.user.is_active = False
        new.user.save()
        self.assertFalse(ImagerProfile.active.all())

    # Test 10
    # Check that if user is killed, imagerProfile is killed
    def test_no_imagerprofile(self):
        new = User.objects.all()[0]
        self.assertIs(len(ImagerProfile.objects.all()), 1)
        new.delete()
        self.assertFalse(ImagerProfile.objects.all())

    # Test 11
    # Check that if imagerProfile is killed, user is killed
    def test_no_user(self):
        new = ImagerProfile.objects.all()[0]
        self.assertIs(len(User.objects.all()), 1)
        new.delete()
        self.assertFalse(User.objects.all())
