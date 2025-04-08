import unittest
from unittest.mock import patch
import csv
from api.tasks import generate_reports_task

BATCH_SIZE = 100  # Valor que tengas en tu código


class GenerateReportsTaskTest(unittest.TestCase):

    @patch('api.tasks.connection.cursor')  # Simula el cursor de la base de datos
    @patch('builtins.open', new_callable=unittest.mock.mock_open)  # Simula la apertura de archivos
    def test_generate_reports_task(self, mock_open, mock_cursor):
        # Datos simulados que devuelve la consulta `get_campaigns_by_date`
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = [
            (1, 'Campaign 1'),
            (2, 'Campaign 2'),
        ]

        # Simulamos el resultado de la consulta `get_campaign_details`
        mock_cursor.return_value.__enter__.return_value.execute.return_value = None
        mock_cursor.return_value.__enter__.return_value.fetchall.side_effect = [
            [('mensaje1', 'destinatario1'), ('mensaje2', 'destinatario2')],  # Campaña 1
            [('mensaje3', 'destinatario3')]  # Campaña 2
        ]

        # Llamamos a la función que estamos probando
        date_report = '2025-04-08'  # Ejemplo de fecha de informe
        generate_reports_task(date_report)

        # Verificar que `cursor.execute` haya sido llamado correctamente
        mock_cursor.return_value.__enter__.return_value.execute.assert_any_call(
            "SELECT * FROM get_campaigns_by_date(%s)", ['2025-04-08']
        )

        # Verificar que se abrió un archivo CSV para cada campaña
        mock_open.assert_any_call('report_1.csv', 'w', newline='')
        mock_open.assert_any_call('report_2.csv', 'w', newline='')

        # Verificar que se escribieron los encabezados en el CSV
        handle = mock_open()
        writer = csv.writer(handle)
        writer.writerow.assert_any_call(['mensaje', 'destinatario'])

        # Verificar que los datos fueron escritos en el archivo
        writer.writerows.assert_any_call([('mensaje1', 'destinatario1'), ('mensaje2', 'destinatario2')])
        writer.writerows.assert_any_call([('mensaje3', 'destinatario3')])

    @patch('api.tasks.connection.cursor')
    def test_no_campaigns(self, mock_cursor):
        # Simula que no se encuentran campañas en la base de datos
        mock_cursor.return_value.__enter__.return_value.fetchall.return_value = []

        # Llamamos a la función
        date_report = '2025-04-08'
        result = generate_reports_task(date_report)

        # Verificar que no se generaron archivos ni consultas adicionales
        mock_cursor.return_value.__enter__.return_value.execute.assert_called_once_with(
            "SELECT * FROM get_campaigns_by_date(%s)", ['2025-04-08']
        )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
