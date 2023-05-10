from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    """Tournament table"""
    LEAGUE = 'Лига'
    SINGLE = 'Олимпийская система'
    DOUBLE = 'Двойной отбор'

    COMPETITION_TYPES = [
        (LEAGUE, 'Лига'),
        (SINGLE, 'Олимпийская система'),
        (DOUBLE, 'Двойной отбор'),
    ]

    name = models.CharField(max_length=20)
    competition_type = models.CharField(max_length=30, choices=COMPETITION_TYPES)
    number_of_points_for_a_win = models.PositiveSmallIntegerField(default=3)
    logotype = models.ImageField(upload_to='media', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    privacy = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Participant(models.Model):
    """Tournament participants"""
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    participant = models.CharField(max_length=50)
    wins = models.PositiveSmallIntegerField(default=0, blank=True)
    draws = models.PositiveSmallIntegerField(default=0, blank=True)
    defeats = models.PositiveSmallIntegerField(default=0, blank=True)
    total_games = models.PositiveSmallIntegerField(default=0, blank=True)
    points = models.PositiveSmallIntegerField(default=0, blank=True)

    def __str__(self):
        return self.participant
