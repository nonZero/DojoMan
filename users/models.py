from django.contrib.auth.models import User
from django.db import models


class UserRank(models.Model):
    ordinal = models.IntegerField(default=100)
    title = models.CharField(max_length=100)


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.PROTECT)
    rank = models.ForeignKey(UserRank, models.PROTECT)
