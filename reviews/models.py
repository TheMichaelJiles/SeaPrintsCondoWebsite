from django.db import models

class Review(models.Model):
    name = models.CharField(max_length=10)
    in_date = models.DateField()
    rating = models.IntegerField()
    review_text = models.TextField()
    publish_date = models.DateField()

    def __str__(self):
        return f'{self.name}: left rating of {self.rating}'


# Create your models here.
