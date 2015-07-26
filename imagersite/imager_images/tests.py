from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.test import TestCase
import factory
from faker import Faker

from .models import Album, Photo

# Create your tests here.
fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Create a fake user."""
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()


class PhotoFactory(factory.django.DjangoModelFactory):
    """Create a fake photo."""
    class Meta:
        model = Photo

    photo = factory.django.ImageField()
    title = fake.sentence()
    description = fake.text()
    user = factory.SubFactory(UserFactory)


class AlbumFactory(factory.django.DjangoModelFactory):
    """Create a fake album."""
    class Meta:
        model = Album

    title = fake.sentence()
    description = fake.text()
    user = factory.SubFactory(UserFactory)


class PhotoTestCase(TestCase):
    """docstring for PhotoTestCase"""
    @classmethod
    def setUp(cls):
        user = UserFactory()
        user.set_password('secret')
        user.save()
        
