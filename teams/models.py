from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=300, blank=True)
    tagline = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.IntegerChoices):
        DRAFT = 1, "Draft"
        ACTIVE = 2, "Active"
        RETIRED = 3, "Retired"

    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT)

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, models.PROTECT, related_name="members")
    user = models.ForeignKey(User, models.PROTECT, related_name="teams")

    class Role(models.IntegerChoices):
        MENTOR = 1, "Mentor"
        MENTEE = 2, "Mentee"
        VIEWER = 100, "Viewer"

    role = models.IntegerField(choices=Role.choices)
