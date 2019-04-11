import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

#import random
from gnumonitor.models import Data_Chart, Chart
from faker import Faker

fakegen = Faker()

def populate(N=5):
    for id in range(8):
        for entry in range(N):

            # Create the fake data for that entry
            chart_list = Chart.objects.order_by('pk')
            id_chart_1 = chart_list[id+1]
            fake_time = fakegen.date_time()
            fake_throughput = fakegen.random_number()

            # Create a Monitor Data
            data = Data_Chart.objects.get_or_create(id_chart=id_chart_1,time=fake_time, value=fake_throughput)[0]

if __name__ == '__main__':
    print("Populating script!")
    populate(20)
    print("...Populating complete.")
