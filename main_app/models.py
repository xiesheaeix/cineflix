from django.db import models

RATINGS = (
    ('1'),
    ('2'),
    ('3'),
    ('4'),
    ('5'),
    ('6'),
    ('7'),
    ('8'),
    ('9'),
    ('10'),
)

class Movie(models.Model):
    imdbId = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    genres = models.CharField(max_length=200, null=True)
    rating = models.IntegerField(
        # choices=RATINGS,
        null=True
    )

    def __str__(self):
        return f'{self.title} ({self.id})'