from django.db import models


class Chart(models.Model):
    # id_chart = models.IntegerField(unique=True)
    xAxis_Name = models.CharField(max_length=264) # time
    yAxis_Name = models.CharField(max_length=264)
    title = models.CharField(max_length=264)
    interval = models.IntegerField()
    comandline = models.CharField(max_length=264)

class Data_Chart(models.Model):
    id_chart = models.ForeignKey(Chart, on_delete=models.PROTECT)
    time = models.DateTimeField()
    value = models.FloatField()
