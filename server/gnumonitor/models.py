from django.db import models

class Sys_Report(models.Model):
    time = models.DateTimeField()
    description = models.CharField(max_length=264)
    etype = models.CharField(max_length=264)

class Host(models.Model):
    name = models.CharField(max_length=264)
    ip = models.CharField(max_length=264)

class Host_Data(models.Model):
    host_object = models.ForeignKey(Host, on_delete=models.PROTECT)
    time = models.DateTimeField()
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    disk_percent = models.FloatField()

class Host_Report(models.Model):
    host_object = models.ForeignKey(Host, on_delete=models.PROTECT)
    time = models.DateTimeField()
    description = models.CharField(max_length=264)
    etype = models.CharField(max_length=264)

class Chart(models.Model):
    host_object = models.ForeignKey(Host, on_delete=models.PROTECT)
    xAxis_Name = models.CharField(max_length=264) # time
    yAxis_Name = models.CharField(max_length=264)
    title = models.CharField(max_length=264)
    parameter = models.CharField(max_length=264)

class Chart_Data(models.Model):
    chart_object = models.ForeignKey(Chart, on_delete=models.PROTECT)
    time = models.DateTimeField()
    value = models.FloatField()

class Chart_Report(models.Model):
    chart_object = models.ForeignKey(Chart, on_delete=models.PROTECT)
    time = models.DateTimeField()
    description = models.CharField(max_length=264)
    etype = models.CharField(max_length=264) #Success (green), Error (red), Info (blue), Warning (Yellow)
