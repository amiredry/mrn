from django.db import models

# Create your models here.


class mrnStream(models.Model):
    story_id = models.CharField(max_length=255, unique=False)
    price = models.CharField(max_length=255)

    def __unicode__(self):
        return self.story_id