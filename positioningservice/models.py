import os
import urllib
import json
import uuid
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save

from .signals import update_index


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def content_file_name(filename):
    file_name, ext = os.path.splitext(filename)
    new_name = uuid.uuid4()
    return '/'.join(['pictures', new_name.hex + ext])


class Position(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "[%s, %s]" % (self.longitude, self.latitude)


class Tag(models.Model):
    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AUTH_USER_MODEL)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('api-v1:tag-detail', kwargs={'pk': self.id})


class Coffee(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=content_file_name, default='media/pictures/no-image.jpg', max_length=10000000)
    longitude = models.FloatField()
    latitude = models.FloatField()
    #position = models.ForeignKey(Position)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     """
    #     Creates a position bonded to a coffeehouse
    #     Creates only on coffee-creation.
    #     """
    #     if self.pk is None:
    #         geo = json.loads(self.get_lat_lon(self.address))
    #         position = Position()
    #         if geo['status'] == "OK":
    #             position.latitude = geo['results'][0]['geometry']['location']['lat']
    #             position.longitude = geo['results'][0]['geometry']['location']['lng']
    #         position.save()
    #         self.position = position
    #     super().save(*args, **kwargs)

    # def get_lat_lon(self, address):
    #     """
    #     Fetches the latitude and longitude from an address
    #     from Google's API
    #     """
    #     address = urllib.parse.quote_plus(address)
    #     geo = urllib.request.urlopen(
    #         "https://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % address)
    #     return geo.readall().decode('utf-8')

    @property
    def rating(self):
        """
        Rating calculated from all the reviews
        for this coffeehouse
        """
        average = self.review.all().aggregate(Avg('rating'))['rating__avg']
        if not average:
            return 0
        return average


class Review(models.Model):
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    coffee = models.ForeignKey(Coffee, related_name='review')
    description = models.TextField()
    user = models.ForeignKey(AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.rating

# Update our indexes when a new coffeehouse is created
post_save.connect(update_index, sender=Coffee)