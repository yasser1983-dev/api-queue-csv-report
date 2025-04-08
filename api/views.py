from datetime import datetime

from django_rq import get_queue
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.tasks import generate_reports_task


class ReportViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def generate_reports(self, request):
        """
        Handles the GET request to generate reports.

        This method validates the provided date, enqueues the report generation
        task using django_rq, and returns a response indicating the status.

        Args:
            request (Request): The HTTP request object containing the date in the body.

        Returns:
            Response: A JSON response indicating success or an error message.
        """
        date_report = request.query_params.get("fecha")

        # Validate date format
        try:
            datetime.strptime(date_report, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD"}, status=400)

        # Enqueue asynchronous tasks with django_rq
        queue = get_queue('default')  # o el nombre que uses en settings.py
        #queue.enqueue(generate_reports_task, date_report)
        generate_reports_task(date_report)

        return Response({"mensaje": "Generación de reportes"})