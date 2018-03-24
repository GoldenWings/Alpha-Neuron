import os
from django.db import models

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
from trainer.models import Trainer


class Agent(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()
    accuracy = models.IntegerField()

    def __str__(self):
        return str(self.accuracy)
