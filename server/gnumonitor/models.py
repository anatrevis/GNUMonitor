from django.db import models


class Chart(models.Model):
    xAxis_Name = models.CharField(max_length=264) # time
    yAxis_Name = models.CharField(max_length=264)
    title = models.CharField(max_length=264)
    parameter = models.CharField(max_length=264)

class Data_Chart(models.Model):
    chart_object = models.ForeignKey(Chart, on_delete=models.PROTECT)
    time = models.DateTimeField()
    value = models.FloatField()

class Data_Error(models.Model):
    chart_object = models.ForeignKey(Chart, on_delete=models.PROTECT)
    time = models.DateTimeField()
    error = models.CharField(max_length=264)
    type = models.CharField(max_length=264)
