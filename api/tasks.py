import csv
from django.db import connection

BATCH_SIZE = 10000

def generate_reports_task(date_report):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_campaigns_by_date(%s)", [date_report])
        campaigns = cursor.fetchall()

    for camp_id, camp_name in campaigns:
        filename = f'report_{camp_id}.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['mensaje', 'destinatario'])

            offset = 0
            while True:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM get_campaign_details(%s, %s, %s)",
                                   [camp_id, offset, BATCH_SIZE])
                    rows = cursor.fetchall()
                    if not rows:
                        break
                    writer.writerows(rows)
                    offset += BATCH_SIZE
