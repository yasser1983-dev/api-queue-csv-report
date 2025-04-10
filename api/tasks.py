import csv
from django.db import connection

BATCH_SIZE = 10000

def get_campaigns(date_report):
    """
    Retrieves all campaigns for a given report date.

    Args:
        date_report (str): The date of the report in 'YYYY-MM-DD' format.

    Returns:
        list: A list of tuples containing campaign data retrieved from the database.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_campaigns_by_date(%s)", [date_report])
        return cursor.fetchall()

def get_campaign_details(camp_id, offset, batch_size):
    """
    Retrieves campaign details in batches for a specific campaign.

    Args:
        camp_id (int): The ID of the campaign.
        offset (int): The starting point for fetching records.
        batch_size (int): The number of records to fetch in each batch.

    Returns:
        list: A list of tuples containing campaign details.
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM get_campaign_details(%s, %s, %s)", [camp_id, offset, batch_size])
        return cursor.fetchall()

def write_campaign_csv(camp_id, data_generator):
    """
    Writes campaign details to a CSV file.

    Args:
        camp_id (int): The ID of the campaign.
        data_generator (generator): A generator that yields batches of campaign details.

    Creates:
        A CSV file named 'report_<camp_id>.csv' containing the campaign details.
    """
    filename = f'report_{camp_id}.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['mensaje', 'destinatario'])
        for batch in data_generator:
            if isinstance(batch, list) or isinstance(batch, tuple):
                writer.writerows(batch)  # batch debe ser iterable de filas


def generate_reports_task(date_report):
    """
    Generates CSV reports for all campaigns on a specific date.

    Args:
        date_report (str): The date of the report in 'YYYY-MM-DD' format.

    Procedure:
        1. Retrieves all campaigns for the given date.
        2. For each campaign, fetches details in batches using a generator.
        3. Writes the details to a CSV file for each campaign.

    Returns:
        None
    """
    campaigns = get_campaigns(date_report)
    if not campaigns:
        return
    for camp_id, _ in campaigns:
        def data_generator():
            """
            A generator function to fetch campaign details in batches.

            Yields:
                list: A batch of campaign details.
            """
            offset = 0
            while True:
                rows = get_campaign_details(camp_id, offset, BATCH_SIZE)
                if not rows:
                    break
                yield rows
                offset += BATCH_SIZE
        write_campaign_csv(camp_id, data_generator())