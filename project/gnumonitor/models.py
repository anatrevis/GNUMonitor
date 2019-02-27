from django.db import models

class MonitorData(models.Model):
    time = models.DateTimeField()
    throughput = models.FloatField()

    def __str__(self):
        return str(self.time)
