# coding: utf-8
import sys

from django.test import TestCase
from django.conf import settings
from django.core.management.base import CommandError

from jobs.management.commands import run_job
from jobs.models import Job


def call_run_job_cmd():
    run_job.Command().handle()


class JobProcessorTest(TestCase):

    def setUp(self):
        try:
            self.JOB_PROCESSOR = settings.JOB_PROCESSOR
            del settings.JOB_PROCESSOR
        except AttributeError:
            pass

    def tearDown(self):
        try:
            settings.JOB_PROCESSOR = self.JOB_PROCESSOR
        except AttributeError:
            pass

    def test_job_processor_not_configured(self):
        try:
            settings.JOB_PROCESSOR
            self.fail()
        except AttributeError:
            pass

        try:
            call_run_job_cmd()
            self.fail()
        except CommandError as ce:
            self.assertEqual(ce.args[0], "The JOB_PROCESSOR module is not configured in settings.")

    def test_job_processor_not_found(self):
        settings.JOB_PROCESSOR = 'blah'
        try:
            call_run_job_cmd()
            self.fail()
        except CommandError as ce:
            self.assertEqual(ce.args[0], "The JOB_PROCESSOR module configured in settings was not found.")

    def test_run_one_job(self):
        # mock do job_processor
        def run_mock(job):
            job.info = 'mbti'
            job.save()

        current_module = sys.modules[__name__]
        current_module.run = run_mock
        settings.JOB_PROCESSOR = __name__

        job_before_cmd = Job.objects.create(info='tri')

        call_run_job_cmd()

        self.assertEqual(job_before_cmd.status, 'PENDING')
        self.assertEqual(job_before_cmd.info, 'tri')

        job_after_cmd = Job.objects.get(pk=job_before_cmd.pk)
        self.assertEqual(job_before_cmd.timestamp, job_after_cmd.timestamp)
        self.assertEqual(job_after_cmd.status, 'DONE')
        self.assertEqual(job_after_cmd.info, 'mbti')
