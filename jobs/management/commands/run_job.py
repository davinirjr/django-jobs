import importlib

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction

from jobs.models import Job


def run_one_job(job_processor):
    candidate_jobs = Job.objects.filter(status='PENDING')
    job = lock_one_job_from_list(candidate_jobs)
    if job:
        job_processor.run(job)
        job.status = 'DONE'
        job.save()


def lock_one_job_from_list(jobs):
    for job in jobs:
        _job = attempt_lock_job(job.id)
        if _job:
            return _job


@transaction.commit_on_success
def attempt_lock_job(id):
    j = Job.objects.select_for_update(id=id)[0]  # wait until you get a write lock for that record
    if j.status == 'PENDING':
        j.status = 'RUNNING'
        j.save()
        return j


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            job_processor = importlib.import_module(settings.JOB_PROCESSOR)
            run_one_job(job_processor)
        except ImportError as e:
            print e
            raise CommandError("The JOB_PROCESSOR module configured in settings was not found.")
        except AttributeError as e:
            print e
            raise CommandError("The JOB_PROCESSOR module is not configured in settings.")
