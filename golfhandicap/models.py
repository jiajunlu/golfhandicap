from django.db import models

TEE_CHOICES = (
    ('w', 'White'),
    ('u', 'Blue'),
    ('b', 'Black'),
    ('r', 'Red'),
    ('g', 'Gold'),
)


class Course(models.Model):
    name = models.CharField(max_length=201, unique=True)

    def __unicode__(self):
        return str(self.name)


class Player(models.Model):
    first_name = models.CharField(max_length=200, blank=True, default='')
    last_name = models.CharField(max_length=200, blank=True, default='')
    nick_name = models.CharField(max_length=200, unique=True, default='')
    email = models.CharField(max_length=200, blank=True, default='')

    def full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def __unicode__(self):
        return str(self.nick_name)


class Game(models.Model):
    course = models.ForeignKey(Course)
    tee = models.CharField(max_length=1, choices=TEE_CHOICES)
    course_handicap = models.FloatField(default=0)
    course_slope = models.IntegerField(default=0)
    game_date = models.DateField()
    game_index = models.IntegerField(default=0)        # in case multiple rounds at the same day
#    game_type = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.game_date) + " " + str(self.course) + " tee: " + self.get_tee_display()


class Score(models.Model):
    player = models.ForeignKey(Player)
    score = models.IntegerField(default=0)
    adjusted_score = models.IntegerField(default=0)
    game = models.ForeignKey(Game)

    def __unicode__(self):
        return str(self.player) + "--" + str(self.score)
