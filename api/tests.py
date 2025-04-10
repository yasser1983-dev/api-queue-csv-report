import csv
import os
import tempfile
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

    def test_get_campaigns_real_db(self):
        # Estos valores deben existir en tu base de datos de pruebas
        date_report = '2025-04-08'
        result = get_campaigns(date_report)

        # Asegurar de que devuelva una lista
        self.assertIsInstance(result, list)

        # Si hay datos, que sean tuplas
        if result:
            self.assertIsInstance(result[0], tuple)

    def test_get_campaign_details_real_db(self):
        # Estos valores deben existir en tu base de datos de pruebas
        camp_id = 1
        offset = 0
        batch_size = 100

        result = get_campaign_details(camp_id, offset, batch_size)

        # Asegúrar que devuelva una lista
        self.assertIsInstance(result, list)

        # Si hay datos, que sean tuplas
        if result:
            self.assertIsInstance(result[0], tuple)

    @patch('api.tasks.csv.writer')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_write_campaign_csv(self, mock_open, mock_csv_writer):
        mock_writer_instance = unittest.mock.MagicMock()
        mock_csv_writer.return_value = mock_writer_instance

        camp_id = 1

        # Generador devuelve un único lote (una lista de tuplas)
        def mock_data_gen():
            yield [('mensaje1', 'destinatario1'), ('mensaje2', 'destinatario2')]

        write_campaign_csv(camp_id, mock_data_gen())

        mock_open.assert_called_with('report_1.csv', 'w', newline='')

        mock_writer_instance.writerow.assert_called_with(['mensaje', 'destinatario'])

        # ✅ Aquí debe coincidir con lo que generaste
        mock_writer_instance.writerows.assert_called_with([
            ('mensaje1', 'destinatario1'),
            ('mensaje2', 'destinatario2')
        ])

    def test_write_campaign_csv_real_file(self):
        camp_id = 1

        # Generador con datos reales
        def data_gen():
            yield [('mensaje1', 'destinatario1'), ('mensaje2', 'destinatario2')]

        with tempfile.TemporaryDirectory() as temp_dir:
            # Cambia el working directory temporalmente para guardar el archivo ahí
            current_dir = os.getcwd()
            os.chdir(temp_dir)

            try:
                write_campaign_csv(camp_id, data_gen())

                expected_file = f'report_{camp_id}.csv'
                self.assertTrue(os.path.exists(expected_file))

                # Validamos el contenido del archivo CSV
                with open(expected_file, newline='') as f:
                    reader = list(csv.reader(f))
                    self.assertEqual(reader[0], ['mensaje', 'destinatario'])
                    self.assertEqual(reader[1:], [
                        ['mensaje1', 'destinatario1'],
                        ['mensaje2', 'destinatario2']
                    ])
            finally:
                # Volvemos al directorio original
                os.chdir(current_dir)

