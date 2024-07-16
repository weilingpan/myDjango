import django_rq
from rq.job import Job
from rq.registry import FinishedJobRegistry

def get_all_jobs():
    queue = django_rq.get_queue('default')
    job_ids = queue.job_ids # 取所有任務的id
    jobs = [Job.fetch(job_id, connection=queue.connection) for job_id in job_ids]
    return jobs

def get_finished_jobs():
    queue = django_rq.get_queue('default')
    finished_job_registry = FinishedJobRegistry(queue=queue)
    job_ids = finished_job_registry.get_job_ids()
    # jobs = [Job.fetch(job_id, connection=queue.connection) for job_id in job_ids]
    return job_ids
