from django.db import models

# Create your models here.


class Card(models.Model):
    states = ["will", "now", "fin", "meet"]
    colors = ["blue", "yellow", "red", "green"]
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=20, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=20, default=states[0])
    importance = models.IntegerField(default=1)
    color = models.CharField(max_length=20, default=colors[0])

    # position
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def __str__(self):
        return self.title
