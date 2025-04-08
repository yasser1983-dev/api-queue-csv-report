from datetime import datetime

from django_rq import get_queue
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.tasks import generate_reports_task


class ReportViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def generate_reports(self, request):
        date_report = request.data.get("fecha")

        # Validar formato de fecha
        try:
            datetime.strptime(date_report, "%Y-%m-%d")
        except ValueError:
            return Response({"error": "Formato de fecha inválido. Usa YYYY-MM-DD"}, status=400)

        # Encolar tarea asíncrona con django_rq
        queue = get_queue('default')  # o el nombre que uses en settings.py
        #queue.enqueue(generate_reports_task, date_report)
        generate_reports_task(date_report)

        return Response({"mensaje": "Generación de reportes"})