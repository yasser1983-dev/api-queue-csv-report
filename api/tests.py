import csv
import unittest
from unittest.mock import patch

from api.tasks import get_campaigns, get_campaign_details, write_campaign_csv


class TestTasks(unittest.TestCase):

    @patch('api.tasks.connection.cursor')
    def test_get_campaigns(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [(1, 'Campaña')]
        result = get_campaigns('2025-04-08')
        self.assertEqual(result, [(1, 'Campaña')])
        mock_cursor.return_value.__enter__.return_value.execute.assert_called_with(
            "SELECT * FROM get_campaigns_by_date(%s)", ['2025-04-08']
        )

    @patch('api.tasks.connection.cursor')
    def test_get_campaign_details(self, mock_cursor):
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [('mensaje', 'destinatario')]
        result = get_campaign_details(1, 0, 100)
        self.assertEqual(result, [('mensaje', 'destinatario')])
        mock_cursor.return_value.__enter__.return_value.execute.assert_called_with(
            "SELECT * FROM get_campaign_details(%s, %s, %s)", [1, 0, 100]
        )

    @patch('api.tasks.csv.writer')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_write_campaign_csv(self, mock_open, mock_csv_writer):
        mock_writer_instance = unittest.mock.MagicMock()
        mock_csv_writer.return_value = mock_writer_instance

        camp_id = 1
        rows = [('mensaje1', 'destinatario1'), ('mensaje2', 'destinatario2')]
        write_campaign_csv(camp_id, rows)

        # Verifica que se abre el archivo correctamente
        mock_open.assert_called_with('report_1.csv', 'w', newline='')

        # Verifica que se escribió el encabezado
        mock_writer_instance.writerow.assert_called_with(['mensaje', 'destinatario'])

        # Verifica que se escribieron las filas
        mock_writer_instance.writerows.assert_called_with(rows)
