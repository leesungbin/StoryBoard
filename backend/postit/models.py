from django.db import models

# Create your models here.


class Card(models.Model):
    states = ["will", "now", "fin"]
    colors = ["blue", "yellow", "red", "green"]
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=20, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    state = models.CharField(max_length=20, default=states[0])
    importance = models.IntegerField(default=1)
    color = models.CharField(max_length=20, default=colors[0])

    # position
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)

    def __str__(self):
        return self.title
