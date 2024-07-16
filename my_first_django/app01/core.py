import django_rq
from rq.job import Job
from rq.registry import FinishedJobRegistry

"""
django_rq 的一些用法
"""
# scheduler = django_rq.get_scheduler()

def get_finished_jobs():
    queue = django_rq.get_queue('default')
    finished_job_registry = FinishedJobRegistry(queue=queue)
    job_ids = finished_job_registry.get_job_ids()
    jobs = [Job.fetch(job_id, connection=queue.connection) for job_id in job_ids]
    return job_ids, jobs
