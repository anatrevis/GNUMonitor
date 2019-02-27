import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

#import random
from gnumonitor.models import MonitorData
from faker import Faker

fakegen = Faker()

def populate(N=5):
    for entry in range(N):

        # Create the fake data for that entry
        fake_time = fakegen.date_time()
        fake_throughput = fakegen.random_number()

        # Create a Monitor Data
        data = MonitorData.objects.get_or_create(time=fake_time, throughput=fake_throughput)[0]

if __name__ == '__main__':
    print("Populating script!")
    populate(20)
    print("...Populating complete.")
