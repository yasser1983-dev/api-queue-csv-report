import csv
from django.db import connection

BATCH_SIZE = 10000

def generate_reports_task(date_report):
    """
    Generates CSV reports for campaigns based on a specific date.

    This function uses stored procedures in the database to retrieve
    campaign information and their details, generating a CSV file for each campaign.

    Args:
        date_report (str): Report date in 'YYYY-MM-DD' format.

    Procedure:
        1. Retrieves all active campaigns for the provided date.
        2. For each campaign, generates a CSV file with campaign details.
        3. Processes data in batches to optimize memory usage.

    Generated files:
        - report_<camp_id>.csv: CSV file containing the campaign details.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_campaigns_by_date(%s)", [date_report])
        campaigns = cursor.fetchall()
    if not campaigns:
        # Exit early if no campaigns are found
        return

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
