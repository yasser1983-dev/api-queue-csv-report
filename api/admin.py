from django.contrib import admin
from django_rq import get_queue
from rq.job import Job
import redis

from api.models import VirtualRQJob


def get_job_status(job_id):
    job = Job.fetch(job_id, connection=redis.Redis())
    state = job.get_status()
    return state

def get_failure_information(job_id):
    try:
        r = redis.Redis()
        job = Job.fetch(job_id, connection=r)
        return job.exc_info
    except redis.exceptions.ConnectionError as e:
        print(f"Error de conexión a Redis: {e}")
        return None
    except Exception as e:
        print(f"Error al obtener la información de fallo: {e}")
        return None


class RQJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'failure', 'created_at', 'enqueued_at', 'started_at', 'ended_at')
    search_fields = ('id', 'status')

    def get_queryset(self, request):
        queue = get_queue('default')
        jobs = queue.jobs
        job_data = []
        for job in jobs:
            job_data.append({
                'id': job.id,
                'status': get_job_status(job.id),
                'failure': get_failure_information(job.id),
                'created_at': job.created_at,
                'enqueued_at': job.enqueued_at,
                'started_at': job.started_at,
                'ended_at': job.ended_at,
            })
        return job_data


admin.site.register(VirtualRQJob, RQJobAdmin)
