"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from gnumonitor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('', views.errors, name='index'),
    path('chart_form/', views.add_chart_form, name='chart_form'),
    path('datalist/', views.chartlist, name='datalist'),
    path('gnumonitor/', include('gnumonitor.urls')),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#     path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
