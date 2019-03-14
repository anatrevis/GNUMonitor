from django.db import models

class MonitorData(models.Model):
    time = models.DateTimeField()
    #seconds = time.
    throughput = models.FloatField()

    # def __str__(self):
    #
    #     return str(self.time)

    #def getSeconds():
    #    return 10
