import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from teams.models import Team, TeamMember
from users.models import UserRank, UserProfile

from faker import Faker

RANKS = {
    "S": ("Senior", 200),
    "M": ("Mid Level", 100),
    "J": ("Junior", 50),
    "N": ("Non Developer", 10),
}


def create_chain(u1, u2, u3, viewer):
    t1 = Team.objects.create()


class Command(BaseCommand):
    help = "Generate fake Dojo data."

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, num, *args, **options):
        def create_user(rank):
            u = User.objects.create_user(
                fake.user_name(),
                fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
            UserProfile.objects.create(
                user=u,
                rank=rank,
            )
            return u

        def create_team(mentor, mentee, viewers):
            tname = " ".join(
                fake.words(min(1, int(random.normalvariate(3, 1))))
            ).title()
            t = Team.objects.create(
                name=tname,
                tagline=fake.sentence(),
                status=random.choice(list(Team.Status)),
            )
            t.members.create(user=mentor, role=TeamMember.Role.MENTOR)
            t.members.create(user=mentee, role=TeamMember.Role.MENTEE)
            for v in viewers:
                t.members.create(user=v, role=TeamMember.Role.VIEWER)
            return t

        fake = Faker()

        self.stdout.write(f"Creating {num} chains.")

        ranks = {
            k: UserRank.objects.get_or_create(
                ordinal=ordinal,
                title=title,
            )[0]
            for k, (title, ordinal) in RANKS.items()
        }

        # create aur user
        try:
            aur = User.objects.create_user("aur")
            UserProfile.objects.get_or_create(
                user=aur,
                defaults={
                    "rank": ranks["S"],
                },
            )
        except IntegrityError:
            aur = User.objects.get(username="aur")

        for i in range(num):
            u1 = create_user(ranks["S"])
            u2 = create_user(ranks["M"])
            u3 = create_user(ranks["J"])
            t1 = create_team(u1, u2, [aur])
            t2 = create_team(u2, u3, [aur, u1])
            print(f"Chain {i+1}/{num}", u1, u2, u3, t1, t2)
