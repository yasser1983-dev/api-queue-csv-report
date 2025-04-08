import os
import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apitest.settings')
django.setup()

from api.models import TASMSMAESTRO, TASMSDETALLE

fake = Faker()

def populate_db(num_campaigns=1000, details_per_campaign=100):
    for _ in range(num_campaigns):
        campaign = TASMSMAESTRO.objects.create(
            name=fake.company(),
            date=fake.date_this_year()
        )
        details = [
            TASMSDETALLE(
                campaign=campaign,
                message=fake.text(max_nb_chars=160),
                receiver=fake.phone_number()
            )
            for _ in range(details_per_campaign)
        ]
        TASMSDETALLE.objects.bulk_create(details)
    print(f"{num_campaigns} campañas creadas con {details_per_campaign} detalles cada una.")

if __name__ == "__main__":
    populate_db()
